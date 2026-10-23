# Adoption plan (2026-10-23)

Base: 3dabcba755a5d3c41d29a8fb14d6f1b9603777e1 after squash-merging reviewed HACS ZIP PR #4. Standards: 26946e9075503633c16fb1b0f7380d0101ed7b45, confirmed against remote main before implementation.

1. Preserve domain, unique IDs, config-entry schema, protocol packets, effect names, minimum HA 2025.11.0, existing image table/body order and HACS Custom ZIP distribution.
2. Replace manual BLE opening/reconnection with public blesession sessions, keep the 30-second reuse policy and repeated writes. Serialize command blocks and cleanup; resolve HA routes under the lock. Expose service failures without claiming failed writes succeeded.
3. Add actual HA flow/setup/platform/service/unload tests and BLE failure/concurrency/cancellation regression tests. Verify exact minimum/current HA and blesession floor in separate environments.
4. Render bilingual managed README sections and standard workflows with central renderers. Add translations, device troubleshooting, environment documentation and category evidence. No imagespec/payload, coordinator or new entity platforms are needed.
5. Run central static checks, lint, remote HACS/Hassfest/HA CI and independent review under GOV-05. Record evidence and update only this repository's central status. Merge only after actionable findings are fixed and required checks pass.
