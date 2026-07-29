# Reproducible code-review example

This synthetic Python module demonstrates the evidence format used by the
fixed-scope code-review service. It contains five intentional defects, a
corrected implementation, a reproduction script, and regression tests.

No client code or client claims are represented here.

## Run the evidence

```console
python reproduce_findings.py
python -m unittest -q
```

The first command must report five `true` results. The second command must
report seven passing tests.

## Files

- `sample_before.py` — synthetic review target with five intentional defects
- `REPORT.md` — severity, exact file:line evidence, impact, and remediation
- `reproduce_findings.py` — dependency-free reproduction of all five findings
- `fixed_after.py` — corrected implementation
- `test_fixed_after.py` — regression coverage for the corrected behavior
