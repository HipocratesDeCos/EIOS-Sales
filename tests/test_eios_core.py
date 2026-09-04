import unittest

from eios_core import evaluate_operation, validate_profile


PROFILE = {
    "parameter_set_id": "TEST-PARAM-001", "company_id": "TEST", "version": "1.0",
    "effective_from": "2026-09-04T00:00:00Z", "approved_by": "TEST",
    "parameters": {"minimum_margin": 15, "target_margin": 25, "max_discount_without_approval": 5, "target_payment_days": 30, "maximum_payment_days": 60, "current_priority": "MARGIN"},
}


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.operation = {"product": "Producto", "quantity": 10, "customer": "Cliente", "currency": "EUR", "unit_price": 20, "unit_cost": 10, "payment_days": 30, "customer_status": "ACTIVE", "risk_status": "CLEAR", "concession_type": "NONE", "counterpart": ""}

    def test_profile_is_valid(self):
        self.assertEqual(validate_profile(PROFILE), [])

    def test_green_when_limits_are_met(self):
        result = evaluate_operation(self.operation, PROFILE, "TEST", 0)
        self.assertEqual(result.traffic_light, "GREEN")

    def test_walk_away_below_minimum_margin(self):
        operation = self.operation | {"unit_cost": 18}
        result = evaluate_operation(operation, PROFILE, "TEST", 0)
        self.assertEqual(result.traffic_light, "RED")
        self.assertEqual(result.commercial_outcome, "WALK_AWAY")

    def test_missing_risk_is_white(self):
        operation = self.operation | {"risk_status": "PENDING"}
        result = evaluate_operation(operation, PROFILE, "TEST", 0)
        self.assertEqual(result.traffic_light, "WHITE")

    def test_concession_without_counterpart_is_red(self):
        operation = self.operation | {"concession_type": "DISCOUNT", "counterpart": ""}
        result = evaluate_operation(operation, PROFILE, "TEST", 0)
        self.assertEqual(result.traffic_light, "RED")


if __name__ == "__main__":
    unittest.main()
