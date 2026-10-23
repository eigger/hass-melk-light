# Scoped adoption checklist


## 2026-10-23 HACS ZIP and Downloads (scoped)

- Target base: `a7824588015ecbd86dc001bc63062b2f0bf4b874`; reviewed release central: `fd4162c0b93fbe8e109f99c787773ae09ba157e1`.
- Scope: HACS-04/CI-11 release ZIP and DOC-03/05 Downloads replacing Analytics Usage. No release is created during this update.
- Local scoped validation: PASS — canonical badge check, no Analytics Usage, release metadata/caller contract, actionlint 1.7.12, native git diff --check, unchanged tracked integration/manifest/dependencies/tests.
- Actual archive build: PASS at `8a34113c2dc0d29fa0fdb0efa0304180698d5068`; `melk_light.zip`, 14 files, SHA256 `81fdd3e1239038afb2c4dc9c874b19693920abbe9c23f1b42c21c78d884173f2`. All archive members matched checkout bytes; manifest.json and __init__.py are at ZIP root. Final documentation-only follow-up preserves this integration tree. Windows Python 3.14.6; validation WSL Python 3.14.4/PyYAML 6.0.3/packaging 26.0.
- Full central integration checker: FAIL (pre-existing or unadopted contracts outside this scoped update; not treated as PASS). Findings:

```text
DOC-01 .hass-standards.json: readmes must be [README.md, README.ko.md]
HA-02 custom_components/melk_light/manifest.json: Actual manifest issue_tracker is required
HA-02 custom_components/melk_light/manifest.json: categories requires 1–3 actual product categories (HA-02 project policy)
HA-11 custom_components/melk_light/translations/ko.json: Required contract file is missing
TEST-08 tests/components/melk_light/test_init.py: Required contract file is missing
TEST-08 tests/components/melk_light/test_config_flow.py: Required contract file is missing
TEST-08 tests/components/melk_light/test_light.py: Required contract file is missing
HA-13 custom_components/__init__.py: Required contract file is missing
HA-11 custom_components/melk_light/translations/ko.json: [Errno 2] No such file or directory: '/mnt/d/Source/Github/.hacs-custom-zip/hass-melk-light/custom_components/melk_light/translations/ko.json'
TEST-08 tests/__init__.py: must exist and be empty
TEST-08 tests/components/__init__.py: must exist and be empty
TEST-08 tests/components/melk_light/__init__.py: must exist and be empty
TEST-03 tests/conftest.py: must match the central template exactly
TEST-08 tests/components/melk_light/conftest.py: [Errno 2] No such file or directory: '/mnt/d/Source/Github/.hacs-custom-zip/hass-melk-light/tests/components/melk_light/conftest.py'
TEST-08 tests/components/melk_light/test_init.py: real HA lifecycle tests are required
CI-01 .github/workflows/validate.yml: required common workflow missing
CI-01 .github/workflows/tests.yml: required common workflow missing
```

- Existing CI workflows are preserved, except hass-kocom-smarthome where matching reviewed central references are synchronized. Existing support minimum and prior exceptions remain.
- Independent review and remote CI: tracked in this branch's pull request; merge requires resolved actionable findings and successful applicable checks. No real release upload, device or new real HA runtime validation is claimed by these local packaging checks.

## 2026-10-23 Full adoption verification (in progress)

Implementation plan: [docs/adoption-plan.md](docs/adoption-plan.md). Standards 26946e9075503633c16fb1b0f7380d0101ed7b45. Minimum HA remains 2025.11.0; no support-policy exceptions. Original protocol packets and stable identifiers are preserved. Full rule-by-rule completion evidence is being collected in this PR.

Independent reviewer independent_review examined the working tree against base 3dabcba; no confirmed runtime blockers. DOC-07 report-information omission fixed in both languages. Final commit review and remote CI pending.

Current/local library floor: 16 tests passed on HA 2026.10.2, Python 3.14.7, plugin0.13.373, blesession0.9.0, pip check PASS in separate environments. Minimum HA hardware setup boundary fixture fixed, 16 tests passed on HA2025.11.0/Python3.13.15/plugin0.13.294/blesession0.9.0; full four-environment final rerun pending.

Physical device/ESPHome transfer, HACS installation and release upload remain unverified. No release/tag has been created. Original packaging evidence above is historical, not current runtime evidence.
