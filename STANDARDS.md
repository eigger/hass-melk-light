# Standards adoption

- Reviewed standards SHA: `ca740d88b32fa5dcbc94c41fce2908450c76ed50`
- Standard: https://github.com/eigger/hass-repo-standards/tree/ca740d88b32fa5dcbc94c41fce2908450c76ed50
- Profile: integration / ha; repository eigger/hass-melk-light; default branch master; domain melk_light.
- Scope and implementation plan: [docs/adoption-plan.md](docs/adoption-plan.md).
- Evidence and completion status: [ADOPTION_CHECKLIST.md](ADOPTION_CHECKLIST.md). No approved exceptions.
- Minimum HA remains 2025.11.0. Current tests use HA 2026.10.2 independently of support policy.
- blesession>=0.9.0 uses public session APIs and keeps the 30-second idle reuse policy. Both current and exact floor modes run in each HA environment. Minimum HA constrains pycares<5 because its aiodns 3.x requires result types removed in pycares 5; this does not raise support minimum.
- Product category: lighting, based on the physical RGB MELK light bar and its lighting controls. Category evidence is in .hass-standards.json; no category is inferred merely from platform names.
- Domain, config-entry data/schema, device identifiers and entity unique IDs remain unchanged. No data migration is needed. Failed writes now surface as service errors; successful writes still represent assumed state without hardware acknowledgement.
- HACS remains Custom. PR #4 was reviewed and squash merged at 3dabcba755a5d3c41d29a8fb14d6f1b9603777e1. Downloads counts all release assets. ZIP deployment starts with the next separately requested release; no release/tag was created for this adoption.
- Reviewed release standards SHA: `ca740d88b32fa5dcbc94c41fce2908450c76ed50`
- Release action retains reviewed release standards SHA fd4162c0b93fbe8e109f99c787773ae09ba157e1 from PR #4; it is scoped independently of the full adoption SHA.
- No imagespec, payload examples, polling coordinator, authentication, options flow or custom services exist; these conditional requirements are N/A.

## Hassfest schema compatibility

The published official Hassfest image (digest sha256:2dce3c5423a600e7965e5a3d5a95e0707e8452fb001ab2b5d0602099bbecba92) rejected the official categories key in PR #5 run 39914054037. The central supported hassfest-core-ref input now selects reviewed Core ec18d8b25d1ee39aa8b85a72a170e42bee33228c, whose manifest validator supports custom categories. Shared CI builds and runs that commit's unmodified official Dockerfile/entrypoint and full validator against the original caller checkout. No manifest key or validation is removed. This selects a validator, not the HA runtime or support minimum. Remove the override only after the official published image passes the same manifest. Initial source review confirms categories support and the official build path; remote build/result is tracked in the checklist.

## Connection and failure diagnostics follow-up

User follow-up after0.2.0 requests connection/error diagnostics. Add binary_sensor and sensor platforms under the existing device/identifiers. Use public blesession SessionTrace, SessionReports and build_report; HA-layer radio_facts injection keeps the protocol package HA-independent. Connection callbacks never initiate I/O; report/connection listeners are removed on unload. Keep minimum HA2025.11.0 and blesession>=0.9.0. Counts reset on entry reload and cancellation/normal idle/unload are not counted as failed commands. This is a separate functional change; prior adoption PASS results do not validate it. New evidence is in the checklist's follow-up section.

## 2026-10-25 중앙 검사기 갱신

- 검토한 중앙 main: `1863343638014adb8a4001afc8fddc1a27dc500f` (git ls-remote 확인). 이전 기본 기준 `26946e9075503633c16fb1b0f7380d0101ed7b45`의 채택 이력은 위 기록을 보존합니다.
- 모든 중앙 workflow/action pin과 reusable workflow의 standards-ref를 같은 검토 SHA로 맞춥니다. HACS-04는 actions/*의 full SHA 고정을 유지하면서 SHA 값 차이를 허용합니다.
- 통합 코드·런타임 의존성·지원 최소·배포 버전은 이번 변경 대상이 아닙니다. 기존 채택 범위를 전체 완료로 바꾸지 않으며 실제 검증 결과와 남은 항목은 ADOPTION_CHECKLIST.md의 같은 날짜 기록을 참조합니다.


### 2026-10-25 Standards 파일·표시 이름 분리

- 기존 Validate의 중앙 검사 job을 `standards.yml`로 옮기고 workflow/job 표시 이름을 `Standards`로 줄였습니다. Validate의 HACS/Hassfest, 검사 항목·통과 기준·실행 단계·조건·권한은 유지합니다.
- 위치 인식과 중앙 명명 안내를 맞춘 검토 소스: `ca740d88b32fa5dcbc94c41fce2908450c76ed50` ([중앙 PR #24](https://github.com/eigger/hass-repo-standards/pull/24), 현재 이 PR의 의존 변경). 이전 기준 `1863343638014adb8a4001afc8fddc1a27dc500f`의 검증 이력은 앞 기록으로 보존합니다. 모든 중앙 pin·standards-ref는 같은 새 검토 소스로 맞춥니다.
