from pathlib import Path
import tempfile
import unittest

import fixed_after


class FixedAfterTests(unittest.TestCase):
    def test_destination_stays_inside_base(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory) / "exports"
            base.mkdir()
            self.assertEqual(
                fixed_after.destination_for(str(base), "report.csv"),
                (base / "report.csv").resolve(),
            )

    def test_destination_rejects_parent_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory) / "exports"
            base.mkdir()
            with self.assertRaisesRegex(ValueError, "escapes"):
                fixed_after.destination_for(str(base), "../outside.txt")

    def test_remember_tag_does_not_share_default_state(self) -> None:
        self.assertEqual(fixed_after.remember_tag("alpha"), ["alpha"])
        self.assertEqual(fixed_after.remember_tag("beta"), ["beta"])

    def test_completion_rate_for_positive_total(self) -> None:
        self.assertEqual(fixed_after.completion_rate(3, 4), 0.75)

    def test_completion_rate_rejects_zero_total(self) -> None:
        with self.assertRaisesRegex(ValueError, "greater than zero"):
            fixed_after.completion_rate(0, 0)

    def test_parse_quantity_rejects_negative_values(self) -> None:
        self.assertEqual(fixed_after.parse_quantity("3"), 3)
        with self.assertRaisesRegex(ValueError, "must not be negative"):
            fixed_after.parse_quantity("-2")

    def test_format_csv_row_escapes_commas(self) -> None:
        self.assertEqual(
            fixed_after.format_csv_row(["Smith, Alice", 3]),
            '"Smith, Alice",3',
        )


if __name__ == "__main__":
    unittest.main()
