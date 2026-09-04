"""Adaptador SNAPSHOT: traduce clientes.xlsx y articulos.xlsx al contrato canónico EIOS.

Cumple el modo SNAPSHOT descrito en Contrato_Integracion_Datos_EIOS.md: cada registro
conserva sistema de origen, fila de origen, momento de carga y un data_snapshot_id común
para toda la carga. Este módulo NO calcula margen ni decide nada; solo entrega objetos
canónicos (Cliente, Producto/servicio) al resto de la aplicación.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from io import BytesIO
from typing import Any

import pandas as pd

ESTADOS_CLIENTE = {"ACTIVE", "INACTIVE", "PENDING"}
ESTADOS_RIESGO = {"CLEAR", "CRITICAL", "PENDING"}

CLIENTES_COLUMNAS = {
    "customer_id": "customer_id",
    "nombre_cliente": "nombre_cliente",
    "estado": "estado",
    "riesgo": "riesgo",
    "plazo_pago_dias": "plazo_pago_dias",
}
ARTICULOS_COLUMNAS = {
    "product_id": "product_id",
    "descripcion": "descripcion",
    "coste_unitario": "coste_unitario",
    "moneda": "moneda",
}


@dataclass(frozen=True)
class SnapshotLoadResult:
    data_snapshot_id: str
    retrieved_at: str
    source_system: str
    records: list[dict[str, Any]]
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors and bool(self.records)


def _new_snapshot_id(file_bytes: bytes, source_system: str) -> str:
    digest = sha256(file_bytes).hexdigest()[:10].upper()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"SNAP-{source_system}-{stamp}-{digest}"


def _read_excel(uploaded_file) -> tuple[pd.DataFrame | None, list[str], bytes]:
    raw = uploaded_file.getvalue()
    try:
        df = pd.read_excel(BytesIO(raw), dtype=str)
    except Exception as exc:  # noqa: BLE001 - se traduce a mensaje de negocio
        return None, [f"No se pudo leer el archivo Excel: {exc}"], raw
    df.columns = [str(c).strip().lower() for c in df.columns]
    return df, [], raw


def load_clientes(uploaded_file, source_system: str = "CLIENTES_XLSX") -> SnapshotLoadResult:
    """Lee clientes.xlsx y devuelve objetos Cliente canónicos."""
    df, errors, raw = _read_excel(uploaded_file)
    retrieved_at = datetime.now(timezone.utc).isoformat()
    if df is None:
        return SnapshotLoadResult("", retrieved_at, source_system, [], errors)

    missing_cols = [c for c in CLIENTES_COLUMNAS if c not in df.columns]
    if missing_cols:
        return SnapshotLoadResult(
            "", retrieved_at, source_system, [],
            [f"Faltan columnas obligatorias en clientes.xlsx: {', '.join(missing_cols)}."],
        )

    snapshot_id = _new_snapshot_id(raw, source_system)
    records: list[dict[str, Any]] = []
    row_errors: list[str] = []
    for idx, row in df.iterrows():
        excel_row = idx + 2  # cabecera en fila 1
        customer_id = str(row.get("customer_id", "")).strip()
        nombre = str(row.get("nombre_cliente", "")).strip()
        estado = str(row.get("estado", "")).strip().upper()
        riesgo = str(row.get("riesgo", "")).strip().upper()
        plazo = row.get("plazo_pago_dias")
        if not customer_id or not nombre:
            row_errors.append(f"Fila {excel_row}: falta customer_id o nombre_cliente.")
            continue
        if estado not in ESTADOS_CLIENTE:
            row_errors.append(f"Fila {excel_row} ({nombre}): estado '{estado}' no permitido (use ACTIVE, INACTIVE o PENDING).")
            continue
        if riesgo not in ESTADOS_RIESGO:
            row_errors.append(f"Fila {excel_row} ({nombre}): riesgo '{riesgo}' no permitido (use CLEAR, CRITICAL o PENDING).")
            continue
        try:
            plazo_dias = int(float(plazo)) if plazo not in (None, "", "nan") else None
        except (TypeError, ValueError):
            row_errors.append(f"Fila {excel_row} ({nombre}): plazo_pago_dias debe ser numérico.")
            continue
        records.append({
            "customer_id": customer_id,
            "nombre_cliente": nombre,
            "estado": estado,
            "riesgo": riesgo,
            "plazo_pago_dias": plazo_dias,
            "source_system": source_system,
            "source_record_id": f"row:{excel_row}",
            "retrieved_at": retrieved_at,
            "data_snapshot_id": snapshot_id,
        })
    return SnapshotLoadResult(snapshot_id, retrieved_at, source_system, records, row_errors)


def load_articulos(uploaded_file, source_system: str = "ARTICULOS_XLSX") -> SnapshotLoadResult:
    """Lee articulos.xlsx y devuelve objetos Producto/servicio canónicos."""
    df, errors, raw = _read_excel(uploaded_file)
    retrieved_at = datetime.now(timezone.utc).isoformat()
    if df is None:
        return SnapshotLoadResult("", retrieved_at, source_system, [], errors)

    missing_cols = [c for c in ARTICULOS_COLUMNAS if c not in df.columns]
    if missing_cols:
        return SnapshotLoadResult(
            "", retrieved_at, source_system, [],
            [f"Faltan columnas obligatorias en articulos.xlsx: {', '.join(missing_cols)}."],
        )

    snapshot_id = _new_snapshot_id(raw, source_system)
    records: list[dict[str, Any]] = []
    row_errors: list[str] = []
    for idx, row in df.iterrows():
        excel_row = idx + 2
        product_id = str(row.get("product_id", "")).strip()
        descripcion = str(row.get("descripcion", "")).strip()
        coste = row.get("coste_unitario")
        moneda = str(row.get("moneda", "")).strip().upper()
        if not product_id or not descripcion:
            row_errors.append(f"Fila {excel_row}: falta product_id o descripcion.")
            continue
        try:
            coste_unitario = float(str(coste).replace(",", "."))
        except (TypeError, ValueError):
            row_errors.append(f"Fila {excel_row} ({descripcion}): coste_unitario debe ser numérico.")
            continue
        if coste_unitario < 0:
            row_errors.append(f"Fila {excel_row} ({descripcion}): coste_unitario no puede ser negativo.")
            continue
        if not moneda:
            row_errors.append(f"Fila {excel_row} ({descripcion}): falta moneda.")
            continue
        records.append({
            "product_id": product_id,
            "descripcion": descripcion,
            "coste_unitario": coste_unitario,
            "moneda": moneda,
            "source_system": source_system,
            "source_record_id": f"row:{excel_row}",
            "retrieved_at": retrieved_at,
            "data_snapshot_id": snapshot_id,
        })
    return SnapshotLoadResult(snapshot_id, retrieved_at, source_system, records, row_errors)
