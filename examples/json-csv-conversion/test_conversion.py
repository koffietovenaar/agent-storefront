import csv
import json
from pathlib import Path
import tempfile
import unittest

import convert_json_to_csv as converter


ROOT = Path(__file__).resolve().parent


class ConversionTests(unittest.TestCase):
    def test_deep_get_reads_nested_values_and_defaults(self) -> None:
        record = {"customer": {"name": "Ada"}}
        self.assertEqual(converter.deep_get(record, "customer.name"), "Ada")
        self.assertEqual(converter.deep_get(record, "customer.email", ""), "")

    def test_supported_transforms_are_deterministic(self) -> None:
        self.assertEqual(converter.transform("ADA@EXAMPLE.COM", "lower"), "ada@example.com")
        self.assertEqual(converter.transform(19.5, "decimal_2"), "19.50")
        self.assertEqual(converter.transform(True, "boolean"), "true")
        self.assertEqual(converter.transform(["new", "priority"], "join_pipe"), "new|priority")

    def test_unknown_transform_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsupported"):
            converter.transform("value", "execute_code")

    def test_conversion_reconciles_rows_and_columns(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output.csv"
            manifest = Path(directory) / "manifest.json"
            result = converter.convert(
                ROOT / "input.json", ROOT / "mapping.json", output, manifest
            )
            self.assertEqual(result["input_rows"], 4)
            self.assertEqual(result["output_rows"], 4)
            self.assertEqual(result["mapped_column_count"], 6)
            self.assertEqual(result["unaccounted_rows"], 0)
            self.assertEqual(result["empty_output_cells"], 2)

    def test_csv_preserves_unicode_and_escapes_commas(self) -> None:
        with (ROOT / "output.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(rows[2]["customer_name"], "Chloë de Vries")
        self.assertEqual(rows[3]["customer_name"], "Smith, Alice")
        self.assertEqual(rows[3]["tags"], "gift|follow-up")

    def test_checked_in_manifest_matches_checked_in_output(self) -> None:
        manifest = json.loads((ROOT / "reconciliation.json").read_text(encoding="utf-8"))
        self.assertEqual(
            manifest["sha256"]["output.csv"], converter.sha256(ROOT / "output.csv")
        )
        self.assertEqual(
            manifest["sha256"]["mapping.json"], converter.sha256(ROOT / "mapping.json")
        )


if __name__ == "__main__":
    unittest.main()
