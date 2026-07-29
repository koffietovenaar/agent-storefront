# Runnable Python automation proof

This synthetic example demonstrates the delivery shape of the fixed-scope
single-file Python automation service. It inventories a directory and writes a
deterministic JSON report containing file paths, byte counts, extensions, and
SHA-256 checksums.

It is portfolio work on owned synthetic files, not a client deliverable or a
performance claim.

## Included files

- `summarize_files.py` - stdlib-only command-line script
- `test_summarize_files.py` - three pytest tests
- `sample-input/` - three small synthetic files
- `sample-output.json` - output produced by the documented command

## Reproduce the sample

From this directory:

```powershell
python summarize_files.py sample-input --output reproduced-output.json
```

Expected summary:

```text
Wrote 3 files / 115 bytes to ...\reproduced-output.json
```

The JSON content should match `sample-output.json` apart from the output
filename printed to the terminal.

## Run the tests

```powershell
python -m pip install pytest
python -m pytest -q test_summarize_files.py
```

Validated result on Python 3.13:

```text
3 passed
```

The script uses only Python's standard library, performs no network requests,
and excludes hidden files unless `--include-hidden` is supplied.
