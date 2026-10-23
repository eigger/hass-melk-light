# Development

Implementation follows the HA Core module roles under `custom_components/melk_light`; tests use the real HA loader and fixtures under `tests/components/melk_light`. Only external Bluetooth communication is mocked. The protocol package has no Home Assistant imports; `blesession.hass` is used by the integration layer. Discovery does not connect or poll the lamp.

| Environment | Python | HA | pytest HA plugin | blesession |
|---|---|---|---|---|
| Current | 3.14 | 2026.10.2 | 0.13.373 | current resolver and exact 0.9.0 |
| Minimum | 3.13 | 2025.11.0 | 0.13.294 | current resolver and exact 0.9.0 |

HA minimum remains 2025.11.0 as declared before adoption. These are environment contracts; executed results and versions are in [ADOPTION_CHECKLIST.md](ADOPTION_CHECKLIST.md). Use Linux/WSL for HA tests. Physical devices and HACS installation need separate verification.

Create a virtual environment with the matching Python and pip, then install the test pair and packaging. From the repository root run the pinned central `actions/python-environment/install.py` with `INPUT_DOMAIN=melk_light`, `INPUT_REQUIREMENTS=requirements_test.txt`, `INPUT_TEST_PROFILE=ha`, `INPUT_EXPECTED_HA_VERSION=2026.10.2`, `INPUT_HA_COMPONENTS="bluetooth bluetooth_adapters usb"`, and a writable `RUNNER_TEMP`. The installer resolves manifest, test and actual HA component requirements together, then runs `pip check`. Use `requirements_test_min.txt` and expected HA 2025.11.0 in a separate Python 3.13 environment. For the exact library floor, set `INPUT_DEPENDENCY_MODE=minimum` and `INPUT_MINIMUM_PACKAGES='["blesession"]'` in separate environments.

```bash
python -m pip install -r requirements_lint.txt
python -m ruff check .
python -m ruff format --check .
python -m pytest tests/components/melk_light/ -q
python -m pip check
```

Runtime dependencies belong in manifest.json; HA domains belong in dependencies; test/lint packages belong in their requirements files. New APIs must pass the current and exact minimum environments. Shared CI is pinned to the reviewed standards SHA in STANDARDS.md. The updater selects only blesession and proposes a PR; no automatic major updates or support-minimum changes are authorized. Dependabot groups the current HA/plugin pair and excludes historical minimum requirements.
