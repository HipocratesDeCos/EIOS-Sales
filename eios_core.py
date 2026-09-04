"""Reglas deterministas y auditables del prototipo EIOS-Sales."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


ALLOWED_PRIORITIES = {"MARGIN", "SALES", "STOCK", "LIQUIDITY", "RISK", "GROWTH"}


@dataclass(frozen=True)
class Evaluation:
    trace_id: str
    revision: int
    traffic_light: str
    commercial_outcome: str
    reasons: list[str]
    limitations: list[str]
    facts: dict[str, Any]
    parameter_set_id: str
    profile_version: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def validate_profile(profile: dict[str, Any]) -> list[str]:
    """Devuelve los defectos que impiden usar un perfil de empresa."""
    required_top = {"parameter_set_id", "company_id", "version", "effective_from", "approved_by", "parameters"}
    required_params = {
        "minimum_margin",
        "target_margin",
        "max_discount_without_approval",
        "target_payment_days",
        "maximum_payment_days",
        "current_priority",
    }
    errors = [f"Falta el campo {key}." for key in sorted(required_top - profile.keys())]
    params = profile.get("parameters")
    if not isinstance(params, dict):
        return errors + ["parameters debe ser un objeto."]
    errors.extend(f"Falta el parámetro {key}." for key in sorted(required_params - params.keys()))
    for key in {"minimum_margin", "target_margin", "max_discount_without_approval"}:
        if key in params and not isinstance(params[key], (int, float)):
            errors.append(f"{key} debe ser numérico.")
    for key in {"target_payment_days", "maximum_payment_days"}:
        if key in params and (not isinstance(params[key], int) or isinstance(params[key], bool)):
            errors.append(f"{key} debe ser un número entero.")
    if params.get("current_priority") not in ALLOWED_PRIORITIES:
        errors.append("current_priority no es un valor permitido.")
    if isinstance(params.get("minimum_margin"), (int, float)) and isinstance(params.get("target_margin"), (int, float)):
        if params["minimum_margin"] > params["target_margin"]:
            errors.append("minimum_margin no puede superar target_margin.")
    if isinstance(params.get("target_payment_days"), int) and isinstance(params.get("maximum_payment_days"), int):
        if params["target_payment_days"] > params["maximum_payment_days"]:
            errors.append("target_payment_days no puede superar maximum_payment_days.")
    return errors


def new_trace_id() -> str:
    return f"EIOS-SALES-{datetime.now(timezone.utc):%Y%m%d}-{uuid4().hex[:8].upper()}"


def evaluate_operation(
    operation: dict[str, Any], profile: dict[str, Any], trace_id: str, revision: int
) -> Evaluation:
    """Evalúa una operación sin acceder a ERP, CRM ni fuentes externas."""
    profile_errors = validate_profile(profile)
    if profile_errors:
        return _white(trace_id, revision, profile, profile_errors, operation)

    required = {
        "product": "producto o servicio",
        "customer": "cliente",
        "currency": "moneda",
        "quantity": "cantidad",
        "unit_price": "precio unitario",
        "unit_cost": "coste unitario",
        "payment_days": "plazo de pago",
    }
    limitations = [f"Falta {label}." for field, label in required.items() if operation.get(field) in (None, "")]
    if operation.get("customer_status") == "PENDING":
        limitations.append("No se ha comprobado el estado del cliente.")
    if operation.get("risk_status") == "PENDING":
        limitations.append("No se ha comprobado el riesgo o tesorería del cliente.")
    if limitations:
        return _white(trace_id, revision, profile, limitations, operation)

    quantity = float(operation["quantity"])
    unit_price = float(operation["unit_price"])
    unit_cost = float(operation["unit_cost"])
    payment_days = int(operation["payment_days"])
    if quantity <= 0 or unit_price <= 0 or unit_cost < 0 or payment_days < 0:
        return _white(trace_id, revision, profile, ["Cantidad, precio y plazo deben ser válidos; el coste no puede ser negativo."], operation)

    revenue = round(quantity * unit_price, 2)
    total_cost = round(quantity * unit_cost, 2)
    margin = round(((revenue - total_cost) / revenue) * 100, 2)
    facts = {
        **operation,
        "revenue": revenue,
        "total_cost": total_cost,
        "margin_percent": margin,
        "calculated_at": datetime.now(timezone.utc).isoformat(),
    }
    params = profile["parameters"]
    reasons: list[str] = []

    if operation.get("customer_status") == "INACTIVE":
        reasons.append("El cliente figura como inactivo o de baja.")
    if operation.get("risk_status") == "CRITICAL":
        reasons.append("Existe una alerta crítica de riesgo o tesorería.")
    if margin < float(params["minimum_margin"]):
        reasons.append(f"El margen calculado ({margin:.2f}%) está por debajo del mínimo configurado ({params['minimum_margin']}%).")
    if operation.get("concession_type") != "NONE" and not operation.get("counterpart"):
        reasons.append("La concesión no tiene una contrapartida verificable.")
    if reasons:
        return _result(trace_id, revision, "RED", "WALK_AWAY", reasons, [], facts, profile)

    conditions: list[str] = []
    if margin < float(params["target_margin"]):
        conditions.append(f"El margen ({margin:.2f}%) cumple el mínimo, pero no alcanza el objetivo ({params['target_margin']}%).")
    if payment_days > int(params["maximum_payment_days"]):
        return _result(trace_id, revision, "RED", "WALK_AWAY", [f"El plazo de pago ({payment_days} días) supera el máximo configurado ({params['maximum_payment_days']} días)."], [], facts, profile)
    if payment_days > int(params["target_payment_days"]):
        conditions.append(f"El plazo de pago ({payment_days} días) supera el objetivo ({params['target_payment_days']} días).")
    if operation.get("concession_type") != "NONE":
        conditions.append(f"La concesión requiere la contrapartida registrada: {operation['counterpart']}.")
    if conditions:
        return _result(trace_id, revision, "YELLOW", "CONDITIONED_OFFER", conditions, [], facts, profile)

    outcome = "ACCEPTED_WITH_CONCESSION" if operation.get("concession_type") != "NONE" else "TARGET_ACCEPTED"
    return _result(trace_id, revision, "GREEN", outcome, ["La operación cumple los límites configurados y no presenta bloqueos declarados."], [], facts, profile)


def _white(trace_id: str, revision: int, profile: dict[str, Any], limitations: list[str], facts: dict[str, Any]) -> Evaluation:
    return _result(trace_id, revision, "WHITE", "INSUFFICIENT_INFORMATION", [], limitations, facts, profile)


def _result(trace_id: str, revision: int, light: str, outcome: str, reasons: list[str], limitations: list[str], facts: dict[str, Any], profile: dict[str, Any]) -> Evaluation:
    return Evaluation(
        trace_id=trace_id,
        revision=revision,
        traffic_light=light,
        commercial_outcome=outcome,
        reasons=reasons,
        limitations=limitations,
        facts=facts,
        parameter_set_id=str(profile.get("parameter_set_id", "NO_DISPONIBLE")),
        profile_version=str(profile.get("version", "NO_DISPONIBLE")),
    )
