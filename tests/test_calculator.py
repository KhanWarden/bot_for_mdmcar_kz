import unittest
from datetime import datetime
from app.methods.calculate import Calculator, RecyclingFee, FirstRegistrationFee


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.kzt_rate = 500
        Calculator.KZT = self.kzt_rate

    def test_calculate_transit(self):
        expected = int((2200 + 750 + 10000) * self.kzt_rate)
        self.assertEqual(Calculator._calculate_transit(car_price=10000), expected)

    def test_calculate_customs(self):
        sum_from_table = 4430  # USD
        expected_customs = Calculator._calculate_customs(sum_from_table)
        self.assertIsInstance(expected_customs, int)
        self.assertGreater(expected_customs, 0)

    def test_convert_usd_to_kzt(self):
        usd_amount = 100
        expected = int(usd_amount * self.kzt_rate)
        self.assertEqual(Calculator._convert_usd_to_kzt(usd_amount), expected)


class TestRecyclingFee(unittest.TestCase):
    def test_recycling_fee(self):
        self.assertEqual(RecyclingFee.calculate(900), 294900)
        self.assertEqual(RecyclingFee.calculate(1500), 688100)
        self.assertEqual(RecyclingFee.calculate(2500), 983000)
        self.assertEqual(RecyclingFee.calculate(3500), 2260900)
        self.assertEqual(RecyclingFee.calculate(500), 294900)


class TestFirstRegistrationFee(unittest.TestCase):
    def test_first_registration_fee(self):
        current_year = datetime.now().year
        self.assertEqual(FirstRegistrationFee.calculate(current_year - 1), 196600)
        self.assertEqual(FirstRegistrationFee.calculate(current_year - 2), 196600)
        self.assertEqual(FirstRegistrationFee.calculate(current_year), 983)
        self.assertEqual(FirstRegistrationFee.calculate(current_year - 4), 1966000)


if __name__ == "__main__":
    unittest.main()
