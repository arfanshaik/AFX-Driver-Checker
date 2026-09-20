import json
import tempfile
import unittest
from pathlib import Path
from app.exporter import export_csv, export_json

class TestExporter(unittest.TestCase):
    def test_json_export(self):
        rows = [{
            "device_name": "GPU",
            "version": "1.0",
            "provider": "Vendor",
            "driver_date": "2026-01-01",
            "device_class": "DISPLAY",
            "manufacturer": "Vendor",
            "signed": True,
            "health": "OK",
            "reason": "Fine",
        }]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.json"
            export_json(rows, path)
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data[0]["device_name"], "GPU")

    def test_csv_export(self):
        rows = [{
            "device_name": "GPU",
            "version": "1.0",
            "provider": "Vendor",
            "driver_date": "2026-01-01",
            "device_class": "DISPLAY",
            "manufacturer": "Vendor",
            "signed": True,
            "health": "OK",
            "reason": "Fine",
        }]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.csv"
            export_csv(rows, path)
            self.assertTrue(path.exists())
            self.assertIn("device_name", path.read_text(encoding="utf-8-sig"))

if __name__ == "__main__":
    unittest.main()
