import unittest
from datetime import date
from app.analyzer import analyze_driver, driver_age_years

class TestAnalyzer(unittest.TestCase):
    def test_recent_driver_ok(self):
        driver = {
            "device_name": "Example Device",
            "version": "1.0",
            "driver_date": "2025-01-01",
            "signed": True,
            "status": "OK",
        }
        result = analyze_driver(driver, today=date(2026, 1, 1))
        self.assertEqual(result["health"], "OK")

    def test_old_driver_flag(self):
        driver = {
            "device_name": "Example Device",
            "version": "1.0",
            "driver_date": "2020-01-01",
            "signed": True,
            "status": "OK",
        }
        result = analyze_driver(driver, today=date(2026, 1, 1))
        self.assertEqual(result["health"], "Potentially Old")

    def test_unsigned_driver_problem(self):
        driver = {
            "device_name": "Example Device",
            "version": "1.0",
            "driver_date": "2025-01-01",
            "signed": False,
            "status": "OK",
        }
        result = analyze_driver(driver, today=date(2026, 1, 1))
        self.assertEqual(result["health"], "Problem")

if __name__ == "__main__":
    unittest.main()
