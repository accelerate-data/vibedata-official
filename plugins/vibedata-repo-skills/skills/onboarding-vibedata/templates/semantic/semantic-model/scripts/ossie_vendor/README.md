# Vendored Apache Ossie validation sources

Pinned to upstream commit `c5cb931d72029dc523a5dd18d267f083403786f2`
(2026-10-14, `apache/ossie`). Do not edit either file: `ossie.py`
imports `validate.py` and reads `ossie-schema.json` as-is.

Canonical definitions (upstream source of truth; these files are copies):
- Spec: https://github.com/apache/ossie/blob/main/core-spec/spec.md
- Machine schema: https://github.com/apache/ossie/blob/main/core-spec/ossie-schema.json
- Pinned schema: https://github.com/apache/ossie/blob/c5cb931d72029dc523a5dd18d267f083403786f2/core-spec/ossie-schema.json
- Pinned validator: https://github.com/apache/ossie/blob/c5cb931d72029dc523a5dd18d267f083403786f2/validation/validate.py

To re-pin: download both files at the new commit, update this note, and
run the mapped semantic regression checks. In the distributing marketplace, run
`python3 -m unittest discover -s tests -p test_onboarding_semantic.py`. A customer
repository must retain its own applicable semantic tests; do not invent a local
`tests/test_ossie_validate.py` path. Review upstream behavior changes explicitly.

- `validate.py` — `validation/validate.py` (Apache-2.0, header intact)
- `ossie-schema.json` — `core-spec/ossie-schema.json`, spec `0.2.0.dev0`
