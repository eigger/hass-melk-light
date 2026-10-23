# Changelog

## 0.2.0 — 2026-10-23

- Adopt shared HA standards, bilingual documentation/translations, real HA tests and common CI without raising the HA 2025.11.0 minimum.
- Use blesession>=0.9.0 to open/reuse BLE links. Keep two writes at 100 ms spacing and 30-second idle reuse. Serialize command blocks and clean up cancellation/unload safely.
- Report command failures through HA errors instead of silently claiming successful state. State remains assumed: the light does not acknowledge commands or report physical changes. Manifest now describes this as assumed_state.
- Configure HACS Custom ZIP assets and a Downloads badge (PR #4); applies from the next published release. Existing releases are unchanged.

No config-entry or identifier migration is required.
