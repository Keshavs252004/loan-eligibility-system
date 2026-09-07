import operator as op
from sqlalchemy.orm import Session
from .models import BRERule

OPS = {
    ">=": op.ge,
    "<=": op.le,
    ">": op.gt,
    "<": op.lt,
    "==": op.eq,
}

def evaluate_bre(db: Session, lead_data: dict):
    """
    lead_data must contain keys like: age, monthly_income, credit_score,
    loan_amount, property_value
    Returns: (status, list_of_rejection_reasons)
    """
    rules = db.query(BRERule).filter(BRERule.active == True).all()
    reasons = []

    for rule in rules:
        field = rule.field_name
        operator_symbol = rule.operator
        raw_value = rule.value

        if operator_symbol not in OPS:
            continue

        try:
            if "property_value" in raw_value and field == "loan_amount":
                threshold = 0.8 * lead_data.get("property_value", 0)
            else:
                threshold = float(raw_value)
        except ValueError:
            continue

        actual_value = lead_data.get(field)
        if actual_value is None:
            continue

        passed = OPS[operator_symbol](actual_value, threshold)

        if not passed:
            reason = rule.description or f"{field} failed rule {operator_symbol} {raw_value}"
            reasons.append(reason)

    status = "Eligible" if len(reasons) == 0 else "Not Eligible"
    return status, reasons