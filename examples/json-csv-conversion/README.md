# Reproducible JSON-to-CSV conversion

This synthetic example demonstrates the delivery shape of the fixed-scope data
conversion service. A nested JSON array is flattened into a standards-compliant
UTF-8 CSV using a declarative mapping file.

No client data or client-result claim is represented here.

## Reproduce the output

```console
python convert_json_to_csv.py input.json mapping.json reproduced.csv --manifest reproduced-reconciliation.json
python -m unittest -q
```

The converter uses only Python's standard library. The reconciliation manifest
records input/output row counts, mapped columns, empty cells, unaccounted rows,
and SHA-256 checksums for the input, mapping, and output.

## Files

- `input.json` — four synthetic nested order records
- `mapping.json` — six explicit source-path-to-column rules
- `output.csv` — generated UTF-8 CSV with quoting and Unicode preserved
- `reconciliation.json` — row/column counts and checksums
- `convert_json_to_csv.py` — reusable standard-library converter
- `test_conversion.py` — six deterministic tests
