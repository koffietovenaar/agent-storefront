# OpenAPI 3.1 documentation proof

This owned, synthetic example shows the delivery shape of the fixed-scope
OpenAPI documentation service. It is portfolio work, not a client deliverable
or production API claim.

## Included files

- `openapi.yaml` - OpenAPI 3.1 contract for three operations
- `endpoint-reference.md` - readable endpoint guide with requests and responses
- `sample-requests.http` - copyable request examples
- `.spectral.yaml` - lint configuration extending Spectral's OpenAPI rules

## Validate

From this directory, with Spectral CLI 6.16.2 installed:

```powershell
spectral lint openapi.yaml --ruleset .spectral.yaml
```

Expected result:

```text
No results with a severity of 'error' found!
```

The validation command checks the public contract itself. The example server is
illustrative and is not called by the test.
