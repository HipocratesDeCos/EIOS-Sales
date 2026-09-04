import json
from decimal import Decimal, InvalidOperation

import streamlit as st

from eios_core import evaluate_operation, new_trace_id, validate_profile
from snapshot_adapter import load_articulos, load_clientes


st.set_page_config(page_title="EIOS-Sales", page_icon=":material/point_of_sale:", layout="wide")


def parse_decimal(value: str) -> float | None:
    value = value.strip().replace(",", ".")
    if not value:
        return None
    try:
        return float(Decimal(value))
    except InvalidOperation:
        return None


def parse_integer(value: str) -> int | None:
    parsed = parse_decimal(value)
    return int(parsed) if parsed is not None and parsed.is_integer() else None


for key, default in {"trace_id": None, "revision": -1, "evaluation": None, "decision": None}.items():
    st.session_state.setdefault(key, default)

st.title("EIOS-Sales v3.0")
st.caption("Soporte a la decisión comercial. EIOS informa; el comercial autorizado decide y cierra.")

with st.sidebar:
    st.subheader("Perfil de empresa")
    uploaded_profile = st.file_uploader("Perfil aprobado en formato JSON", type=["json"], key="profile_upload")
    if uploaded_profile:
        try:
            profile = json.load(uploaded_profile)
            profile_errors = validate_profile(profile)
        except (json.JSONDecodeError, UnicodeDecodeError):
            profile, profile_errors = None, ["El archivo no es un JSON válido."]
    else:
        profile, profile_errors = None, ["Carga un perfil empresarial aprobado para evaluar una operación."]
    if profile_errors:
        st.warning("Perfil no disponible para evaluación.")
    else:
        st.success(f"Perfil {profile['parameter_set_id']} · versión {profile['version']}")
        st.caption(f"Prioridad: {profile['parameters']['current_priority']}")

    st.divider()
    st.subheader("Datos SNAPSHOT (Excel)")
    st.caption("Carga clientes.xlsx y articulos.xlsx con el formato de la plantilla para rellenar la operación con datos reales.")

    clientes_file = st.file_uploader("clientes.xlsx", type=["xlsx"], key="clientes_upload")
    if clientes_file:
        clientes_result = load_clientes(clientes_file)
        st.session_state.clientes_result = clientes_result
        if clientes_result.errors:
            with st.expander(f"⚠️ {len(clientes_result.errors)} filas de clientes con error", expanded=False):
                for err in clientes_result.errors:
                    st.write(f"- {err}")
        if clientes_result.records:
            st.success(f"{len(clientes_result.records)} clientes cargados · snapshot {clientes_result.data_snapshot_id}")
    clientes_result = st.session_state.get("clientes_result")

    articulos_file = st.file_uploader("articulos.xlsx", type=["xlsx"], key="articulos_upload")
    if articulos_file:
        articulos_result = load_articulos(articulos_file)
        st.session_state.articulos_result = articulos_result
        if articulos_result.errors:
            with st.expander(f"⚠️ {len(articulos_result.errors)} filas de artículos con error", expanded=False):
                for err in articulos_result.errors:
                    st.write(f"- {err}")
        if articulos_result.records:
            st.success(f"{len(articulos_result.records)} artículos cargados · snapshot {articulos_result.data_snapshot_id}")
    articulos_result = st.session_state.get("articulos_result")

    st.divider()
    if st.button("Nueva negociación", icon=":material/add:"):
        st.session_state.trace_id = None
        st.session_state.revision = -1
        st.session_state.evaluation = None
        st.session_state.decision = None
        st.rerun()

st.subheader("Operación comercial")
st.caption("Los campos vacíos producen ⚪. No se usan valores estimados ni fuentes externas en este prototipo.")

if clientes_result and clientes_result.records:
    def _apply_cliente() -> None:
        chosen = st.session_state.get("cliente_pick")
        record = next((r for r in clientes_result.records if f"{r['customer_id']} · {r['nombre_cliente']}" == chosen), None)
        if record:
            st.session_state.customer = record["nombre_cliente"]
            st.session_state.customer_status = record["estado"]
            st.session_state.risk_status = record["riesgo"]
            if record["plazo_pago_dias"] is not None:
                st.session_state.payment_days = str(record["plazo_pago_dias"])

    st.selectbox(
        "Cliente (desde clientes.xlsx)",
        [f"{r['customer_id']} · {r['nombre_cliente']}" for r in clientes_result.records],
        index=None, placeholder="Selecciona un cliente cargado, o escribe uno manualmente abajo",
        key="cliente_pick", on_change=_apply_cliente,
    )

if articulos_result and articulos_result.records:
    def _apply_articulo() -> None:
        chosen = st.session_state.get("articulo_pick")
        record = next((r for r in articulos_result.records if f"{r['product_id']} · {r['descripcion']}" == chosen), None)
        if record:
            st.session_state.product = record["descripcion"]
            st.session_state.unit_cost = str(record["coste_unitario"])
            st.session_state.currency = record["moneda"]

    st.selectbox(
        "Producto o servicio (desde articulos.xlsx)",
        [f"{r['product_id']} · {r['descripcion']}" for r in articulos_result.records],
        index=None, placeholder="Selecciona un artículo cargado, o escribe uno manualmente abajo",
        key="articulo_pick", on_change=_apply_articulo,
    )

with st.form("operation_form", border=True):
    left, right = st.columns(2)
    with left:
        product = st.text_input("Producto o servicio", key="product")
        quantity = st.text_input("Cantidad", key="quantity", placeholder="Ejemplo: 100")
        customer = st.text_input("Cliente", key="customer")
        currency = st.text_input("Moneda", key="currency", placeholder="Ejemplo: EUR")
        unit_price = st.text_input("Precio unitario ofrecido", key="unit_price", placeholder="Ejemplo: 12.50")
    with right:
        unit_cost = st.text_input("Coste unitario trazable", key="unit_cost", placeholder="Ejemplo: 8.00")
        payment_days = st.text_input("Plazo de pago en días", key="payment_days", placeholder="Ejemplo: 30")
        customer_status = st.selectbox("Estado del cliente", ["PENDING", "ACTIVE", "INACTIVE"], format_func={"PENDING": "Pendiente de comprobar", "ACTIVE": "Activo", "INACTIVE": "Inactivo o de baja"}.get, key="customer_status")
        risk_status = st.selectbox("Riesgo y tesorería", ["PENDING", "CLEAR", "CRITICAL"], format_func={"PENDING": "Pendiente de comprobar", "CLEAR": "Sin alerta crítica", "CRITICAL": "Alerta crítica"}.get, key="risk_status")
        concession_type = st.selectbox("Concesión", ["NONE", "DISCOUNT", "PAYMENT_TERM", "FREIGHT", "GIFT", "OTHER"], format_func={"NONE": "Sin concesión", "DISCOUNT": "Descuento", "PAYMENT_TERM": "Ampliación de pago", "FREIGHT": "Portes", "GIFT": "Regalo", "OTHER": "Otra"}.get, key="concession_type")
    counterpart = st.text_input("Contrapartida del cliente", key="counterpart", placeholder="Obligatoria si hay concesión")
    submitted = st.form_submit_button("Evaluar operación", type="primary", icon=":material/analytics:")

if submitted:
    if profile_errors:
        st.error("No se puede evaluar: carga un perfil empresarial válido y aprobado.")
    else:
        if st.session_state.trace_id is None:
            st.session_state.trace_id = new_trace_id()
            st.session_state.revision = 0
        else:
            st.session_state.revision += 1
        operation = {
            "product": product.strip(), "quantity": parse_decimal(quantity), "customer": customer.strip(),
            "currency": currency.strip().upper(), "unit_price": parse_decimal(unit_price),
            "unit_cost": parse_decimal(unit_cost), "payment_days": parse_integer(payment_days),
            "customer_status": customer_status, "risk_status": risk_status,
            "concession_type": concession_type, "counterpart": counterpart.strip(),
            "customer_data_snapshot_id": clientes_result.data_snapshot_id if clientes_result and clientes_result.records else None,
            "product_data_snapshot_id": articulos_result.data_snapshot_id if articulos_result and articulos_result.records else None,
        }
        st.session_state.evaluation = evaluate_operation(operation, profile, st.session_state.trace_id, st.session_state.revision)

evaluation = st.session_state.evaluation
if evaluation:
    labels = {"GREEN": "🟢 Verde — viable", "YELLOW": "🟡 Amarillo — viable con condiciones", "RED": "🔴 Rojo — no viable o riesgo", "WHITE": "⚪ Blanco — información insuficiente"}
    outcome_labels = {"TARGET_ACCEPTED": "Oferta aceptada (objetivo)", "ACCEPTED_WITH_CONCESSION": "Oferta aceptada con concesión", "CONDITIONED_OFFER": "Oferta condicionada", "WALK_AWAY": "No vender (Walk-Away)", "INSUFFICIENT_INFORMATION": "Información insuficiente"}
    st.subheader("Resultado de la evaluación")
    st.info(f"{labels[evaluation.traffic_light]} · {outcome_labels[evaluation.commercial_outcome]}")
    with st.container(border=True):
        st.write(f"**Trace ID:** {evaluation.trace_id} · revisión {evaluation.revision}")
        if evaluation.traffic_light != "WHITE":
            facts = evaluation.facts
            one, two, three = st.columns(3)
            one.metric("Ingresos", f"{facts['revenue']:,.2f} {facts['currency']}")
            two.metric("Coste total", f"{facts['total_cost']:,.2f} {facts['currency']}")
            three.metric("Margen", f"{facts['margin_percent']:.2f}%")
        for reason in evaluation.reasons:
            st.write(f"- {reason}")
        for limitation in evaluation.limitations:
            st.write(f"- {limitation}")
    with st.expander("Auditoría técnica"):
        st.json(evaluation.as_dict())

    st.subheader("Decisión humana")
    decision = st.selectbox("Decisión del comercial autorizado", ["Sin registrar", "Presentar oferta", "Aceptar oferta", "Seguir negociando", "No vender", "Cancelar operación"], key="human_decision")
    decision_reason = st.text_input("Motivo de la decisión", key="decision_reason")
    if st.button("Registrar decisión en esta sesión", icon=":material/how_to_reg:"):
        if decision == "Sin registrar" or not decision_reason.strip():
            st.warning("Indica una decisión y su motivo. EIOS no decide por el comercial.")
        else:
            st.session_state.decision = {"decision": decision, "reason": decision_reason.strip()}
            st.success("Decisión humana registrada en la sesión.")

    audit_export = evaluation.as_dict() | {"human_decision": st.session_state.decision}
    st.download_button("Descargar registro de evaluación", json.dumps(audit_export, ensure_ascii=False, indent=2), file_name=f"{evaluation.trace_id}-R{evaluation.revision}.json", mime="application/json", icon=":material/download:")
