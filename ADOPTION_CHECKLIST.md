# Standards adoption checklist

## 2026-10-23 Connection/error diagnostics follow-up (in progress)

User requested blesession connection/error diagnostic entities after release0.2.0. Base11d581f3bd8a8a86c547bec9c5af386565685b63; reviewed standards SHA stays26946e9075503633c16fb1b0f7380d0101ed7b45. Earlier18-test adoption results below are historical and do not validate this new change.

- HA-05/07/08/09/10/11, TEST-01/06/07/09: add one diagnostic connectivity binary sensor plus command duration, last failure timestamp/report and reload-scoped error count sensors. Existing light/device IDs unchanged; new stable suffix IDs share its device. Push listeners use HA APIs and are removed on unload; no polling, new scans or extra connections.
- Public blesession SessionTrace/SessionReports/build_report plus injected HA radio_facts; no new dependency or support-minimum change. Error count retains failures across successes; cancellation/normal idle/unload are excluded, idle disconnect errors included. Actual radio facts and via_unconfirmed are preserved; exceptions redact the configured device address. Public sharing still requires removing device/proxy names and other identifying data as documented.
- DOC-01/02/07: EN/KO README feature addition and troubleshooting sensor meaning/lifetime/route uncertainty updated; names translated in strings/en/ko. No diagnostic file download is claimed.
- New actual HA test_sensor/test_binary_sensor cover initial state, report values, timestamp retention, count/recovery, unreachable errors, unexpected drop callback before is_connected catches up, same-device registry metadata, listener unload and reload reset. test_device adds reuse/radio facts/disconnect-error report and cancellation non-recording assertions. Existing transport/lifecycle tests retained.
- Four distinct existing WSL environments each26 passed plus pip check: current and exact-floor with Python3.14.7/HA2026.10.2/plugin0.13.373/bleak3.0.2/connector4.7.1; minimum current and exact-floor with Python3.13.15/HA2025.11.0/plugin0.13.294/bleak1.0.1/connector4.4.3. All actually install blesession0.9.0 (current resolver and exact floor coincide). No skip/xfail/deselect. Logs `/home/eigger/.cache/melk-adoption-20261023/diagnostics-{current,current-floor,minimum,minimum-current}.log`. Commands: each environment's `python -m pytest tests/components/melk_light/ -q --timeout 30`, `python -m pip check`, and installed-version print. Sensor/binary_sensor component manifests contain no extra Python requirements or mandatory dependencies; existing HA component install contract remains sufficient.
- GOV-05 independent_review inspected runtime/new platforms and independently ran current26PASS/2.84s, minimum26PASS/0.68s. No confirmed runtime defects; old no-sensor documentation was flagged and is now replaced bilingually. Final commit review and remote CI pending.
- Central start updated at7ca368648cbd419fb942766eb609758c87379f20. Final PR/merge/status evidence pending. Physical lamp/proxy transfer is not verified; no new release/tag is created in this follow-up.

## Current adoption — 2026-10-23

- Repository: eigger/hass-melk-light, master, domain melk_light, profile integration/ha.
- Reviewed central SHA: `26946e9075503633c16fb1b0f7380d0101ed7b45`; [STANDARDS.md](STANDARDS.md), [implementation plan](docs/adoption-plan.md), PR #5.
- Implementer: root. Independent reviewer: independent_review under GOV-05 for lifecycle/actions and CI input changes.
- Reviewed implementation: `2e7fa7aff0fb6601c0810044a6941b7d98c85888`; validator/docs follow-up `199f1e118a6d9b3475b155241da67b58adfe440e`. Subsequent translated-error and metadata changes rechecked below.
- Minimum support before/after: HA2025.11.0 from hacs.json, preserved. Current tests HA2026.10.2 are not a support-minimum change.
- Status: implementation and applicable automated checks complete; PR #5 awaits the final documentation commit checks and authorized squash merge. No approved exceptions. Central status is updated before/after merge; physical limitations below remain.

## Rule-by-rule review (central template rows)

| Rule | Check | Status | Evidence / remaining work |
|---|---|---|---|
| GOV-01, GOV-02 | `STANDARDS.md`에 표준 SHA·profile·실제 기본 브랜치·예외 기록, workflow/action은 검토 SHA로 고정 | PASS | STANDARDS.md: reviewed SHA, integration/ha profile, master branch, no approved exceptions. Generated callers pinned to reviewed SHA; release action has separate documented reviewed SHA. |
| GOV-03 | 새 표준 채택 변경의 영향·이관 방법과 명시적 채택 PR 확인. 규칙 자체를 변경하면 공통 CHANGELOG 기록 | PASS | Explicit adoption PR #5, docs/adoption-plan.md and CHANGELOG.md; central rules are not changed. |
| GOV-04 | 중앙 표에 작업 시작·종료·의미 있는 상태 변화 상태, 담당·적용 내용·검증/리뷰 근거 링크·남은 작업 갱신, 타 리포 기록 보존 | PASS | Central start d023678a3016ea441b0f556524882ba03ca81c6c and verified-progress df4458459816caf5b0ee19d1a0af526aae4a0067 update only this repository row; final merge is reflected in the linked central status after squash. |
| GOV-05 | 자체/독립 리뷰 방식·선택 근거 기록, 큰 구조·HA 동작·공용 CI 실행 로직 변경의 독립 리뷰, 지적 수정·영향 검사 재실행 | PASS | Independent review of2e7fa7a and199f1e1: no remaining actionable findings. DOC-07 reporting details fixed; translated-error follow-up5bcbad7 independently reviewed with no runtime findings; trailing document blank line fixed. |
| HA-01, HA-13 | `custom_components/<domain>/`와 domain 일치, 필요한 모듈·공개 API·생명주기는 Core 대응 구조 | PASS | custom_components/melk_light plus empty custom_components/__init__.py; config_flow/entity/light and separate protocol package; actual HA loader tests. |
| HA-02 | manifest 필드·정렬·동작 선언, 실제 제품 categories 1–3개·주 분류 순서·공식 slug·선택 근거·categories_review 일치 또는 entity/system/virtual 키 생략 이유, 공식 품질 등급 자가 표기 없음 | PASS | Manifest domain/name then sorted fields; issue_tracker, requirements, categories=[lighting]. Physical RGB light bar use, not platform inference; matching categories_review. assumed_state matches write-only state. No quality claim. |
| HA-03 (권장) | 공통 상수·설정·갱신·플랫폼 역할 및 프로토콜 경계에 맞게 모듈 구성 | PASS | Existing module roles preserved; no unnecessary coordinator or platform added. |
| HA-04, HA-08 | UI 설정·중복·안정적 식별 및 기능별 options/reauth/reconfigure, entity 의미·registry 영향 확인 | PASS | Real flow manager tests: manual selection, Bluetooth confirm, unsupported/no devices, duplicate abort. Stable MAC-based unique IDs and registry identifiers preserved. No authentication/options API exists; broken unused reauth removed. |
| HA-01, HA-04, HA-08, REL-01, REL-03 | domain·unique ID·entry schema·상태/통계 계약 변경 시 migration 테스트와 사용자 조치 안내 | N/A | No domain/unique-ID/config-entry schema or data format change. No migration required; CHANGELOG and STANDARDS record user-visible command errors. |
| HA-05, HA-06 | setup 실패 구분, unload/reload·부분 실패의 task/listener/연결 정리, async·timeout·취소 처리 | PASS | test_init real setup/unload/reload and failed-platform cleanup/failed-unload; test_device serializes commands, cancellation before/after handoff, bounded disconnect and idle cleanup. No connection I/O during setup; no auth/setup connection errors to classify. |
| HA-07 | 중복 polling·property I/O 방지, push 보존, unavailable/unknown·실패 후 복구 | PASS | No polling or property I/O; assumed_state explicitly declared. HA service failure retains last successful packet state; failure/recovery covered by test_light. |
| HA-11, HA-12 | 번역·action/schema 일치, 로그/diagnostics/fixture 비식별화와 제공 시 redaction 테스트 | PASS | English/Korean config and command_failed translation keys; no secrets or diagnostics collection; synthetic AA:BB:CC:DD:EE:FF fixtures. User troubleshooting requests sanitized logs. |
| TEST-08 | `tests/components/<domain>/`에 구현과 대응하는 테스트·domain fixture 배치, discovery·CI 경로 일치 | PASS | Central empty init files, exact root conftest, managed domain fixture block plus mock_config_entry/mock_client; tests map to init/config_flow/light and device. |
| TEST-02, TEST-03, DEP-07 | 실제 HA·호환 플러그인과 `hass`/`enable_custom_integrations` fixture 사용, HA core stub/복사본/`--no-deps`로 대체하지 않음 | PASS | Real hass/enable_custom_integrations and MockConfigEntry, no fake HA modules or --no-deps. Four separate WSL environments and actual package versions below. |
| TEST-09 | 실제 loader·config entry manager로 setup/플랫폼 로딩, HA 상태·registry·service/action으로 결과 검증 | PASS | test_init/config_flow/light use HA entry manager/loader, states, light service calls and real platform unload/reload; mock only radio lookup/establish/GATT boundary. |
| TEST-01, TEST-06, TEST-07 | 구현 기능별 성공·실패·중복·migration·unload·복구 회귀 검증, 외부 통신 경계만 mock, skip 사유 | PASS | 18 tests include success/failure/duplicate/unload/recovery, link loss, serial command blocks, stale idle task, cancellation before/after settle, connect failure and disconnect timeout. No skips. Migration/auth N/A: no schema/auth feature. |
| TEST-04, HACS-01 | 변경 전 지원 최소·current·각 Python/플러그인 분리, 선언한 정확한 최소 검증, 상향 시 비호환 근거·명시적 승인 확인 | PASS | hacs.json retains exact2025.11.0 minimum; HA2025.11.0+plugin0.13.294/Python3.13 and current HA2026.10.2+plugin0.13.373/Python3.14. No minimum raise. |
| TEST-05, HA-10, DEP-02, DEP-05 | imagespec·blesession 등 최소/현재 라이브러리 별도 환경, 실제 HA 테스트·정확한 설치값·API 경계 검증 | PASS | blesession>=0.9.0 minimum verified exactly, separate current/floor environments for both HA versions; resolver currently selects0.9.0 in current too. Public ble_session/still_up/ble_device_or_raise only. |
| DEP-01, DEP-06 | Python runtime은 manifest requirements, HA domain은 dependencies/after_dependencies, 테스트·린트 requirements는 별도 | PASS | Runtime blesession in manifest; Bluetooth HA domains in dependencies; test and lint packages in separate requirements. Removed unused BluetoothData inheritance rather than relying on undeclared transitive package. |
| DEP-07, CI-06 | 실제 사용하는 HA 구성요소의 requirements·필수 재귀 의존성·선택 로딩 경로 설치, resolver·`pip check` 통과 | PASS | Pinned central installer resolves manifest/test requirements with actual installed HA bluetooth/bluetooth_adapters/usb recursive requirements, pip check PASS. Minimum pycares<5 compatibility constraint documented. |
| DEP-02, DEP-03, DEP-08 | 의존성 추가/변경의 버전·extras·marker·선언 위치·지원 플랫폼·라이선스 검토, 실제 HA 테스트와 문서 갱신 | PASS | blesession0.9.0 PyPI metadata: Python>=3.13, bleak>=0.22, bleak-retry-connector>=3.6, MIT; matches minimum HA Python. Internal >= contract backed by exact floor CI; no extras/markers introduced. |
| HACS-01, HACS-02 | 루트 README/LICENSE/hacs.json, 검증한 최소 HA, 실제 배포 구조와 필요한 옵션 일치 | PASS | README/LICENSE/hacs.json, unchanged support minimum/version0.1.3, custom_components structure and melk_light.zip contract preserved. |
| HACS-03, HACS-05 | Default 여부는 목록 근거로 확인, [로컬 brand/icon.png 또는 원격 brands 근거](https://github.com/eigger/hass-repo-standards/blob/main/docs/hacs.md)와 HACS/Hassfest 실제 실행, ignore는 이유·해제 조건 기록 | PASS | HACS Custom; local original256x256 brand/icon.png inspected and licensed. Remote HACS and full official source-built Hassfest PASS at5bcbad7 in run39914626140; published-image failure recorded below without suppressing validation. |
| HACS-06 (권장) | description·topics·issue 경로·brands 및 사용하는 HACS 필드 지원 확인 | PASS | gh repo read confirms description/topics/Issues/Discussions; no repository setting changed. Local original icon metadata in brand/README.md; older HA UI display unverified. |
| CI-01, CI-02 | Validate/Tests 공통화, 확장 job 유지, 공용 파일명·표시 이름·PR 대상 제한 없는 기본 이벤트·실제 기본 브랜치 push·dispatch·기존 schedule, 전용 CI 명명 형식 | PASS | Canonical Validate/Tests/Update dependencies filenames/events rendered from central templates; actual master push, unrestricted PR, dispatch and schedules; existing Release workflow preserved. |
| CI-03, CI-05, CI-08 | 최소 권한·checkout 자격증명 비보존·timeout·concurrency, full SHA·갱신 관리, 비신뢰 입력·secrets 경계 | PASS | Central reusable jobs preserve read permissions, timeout and credential-free checkout; full reviewed SHAs. Only updater/release jobs have write permissions. actionlint1.7.12 PASS. |
| CI-04, CI-07, CI-12 | 실패를 숨기지 않는 실제 `ha` 필수 테스트, 버전별 환경·cache·Ruff 설정과 required checks 이름 확인 | PASS | Actual ha jobs and four environment matrix PASS at5bcbad7 in run39914626173, no continue-on-error; ruff0.17.1 lint+format PASS. Branch protection API returns404 Branch not protected; no protection settings changed. |
| DEP-03, DEP-04, CI-09 | updater의 선택 package·연산자/extras/marker 보존, 안정 버전·major 정책, 실제 기본 브랜치·단일 bot branch·PR만 제안 | PASS | Updater selects only blesession; dry-run: Requirements are current; no change. Reviewed shared action preserves operator/extras/markers, rejects major/downgrade and uses one bot branch. |
| CI-09, CI-10, DEP-08 | 변경 tree의 새 하한·실제 HA 검증 후 PR 동기화, 실패 시 중단·변경 없음 시 기존 PR 정리, 후속 required checks 충족 방식 확인 | PASS | Shared updater validates actual changed manifest/floor with HA tests before PR sync. GITHUB_TOKEN follow-up CI limitation documented in central CI-10; no automatic merging. No package update available, so no update PR generated or workflow manually dispatched. |
| DOC-01, DOC-02, DOC-06 | 중앙 header/support/related-projects/license 관리 영역의 정확한 형식, 기존 공통 내용·고지 보존, 영역 밖 순서·제목·본문 유지, 양언어 같은 구조·내용·상호 링크, 번역 의미·누락 리뷰(GOV-05), 실제 활성 지원 링크·실제 라이선스 | PASS | Central renderer managed blocks; original image table/body order/features/install/notes/buy link retained, complete Korean counterpart. English CONTRIBUTING linked in both; remote Issues/Discussions verified. MIT license preserved; independent bilingual review. |
| DOC-03, DOC-04, DOC-05 | 언어 링크 다음 중첩 배지 관리 블록, flat·Release/HACS/HA minimum/Tests/Validate/License/Downloads(Default 또는 ZIP 배포)·Usage(ZIP 미배포 Custom) 순서·실제 조건·고유 배지 보존, 실제 기본 브랜치·상태별 필수 동적 집계 배지·양언어 설치 절의 실제 저장소 My HACS 배지·미집계와 0 설치 구분 | PASS | Canonical flat Release/HACS/HA minimum/Tests/Validate/License/Downloads; Usage removed by merged#4. My HACS owner/repository/category installation badges in both languages. Downloads counts all release assets, not installations. |
| HA-09, HA-10 | BLE 사용 시 HA Bluetooth API·라이브러리 공개 경계, 지원한 proxy 경로·재연결·취소·서비스 변경 검증 | PASS | HA connectable route lookup under command lock and repeat reconnect, real blesession at installed0.9.0; no direct scanner/client class cache. Reconnect writes UUID anew, not cached GATT objects. Physical adapter/ESPHome transfer and firmware/service changes unverified. |
| DOC-07 | blesession 사용 여부(manifest requirement extras·operator·marker/실제 import) 확인. 사용 통합은 중앙 양언어 docs/troubleshooting 템플릿의 고정 제목·순서·증상 표·실제 진단/로그·기존 Issues 연결, README와 로컬 문서의 언어별 상호/공통 blesession 원본 링크·placeholder 제거·공용 Validate 검사. 기존 본문/기기안내 보존, 새 제보 양식 금지. 프록시만 지원하면 기존 기기 조건·사용자 안내를 수동 확인 | PASS | Bilingual exact H2/template structure, symptom tables, actual no-diagnostics/log evidence, power/app/transfer constraints and same-language common guides/README links; report details fixed after independent review. |
| DOC-08 | imagespec 사용 여부·양언어 docs/payload 여섯 절·언어별 README/공통 원본/상호 링크·실제 액션/대상/전체 YAML·기기 출력/지원/제한·기존 예제/본문 보존·기존 지원 연결, 모든 로컬 연결 예제의 payload.examples 등록·실제 경로/payload_format(list 또는 yaml)/크기/모델 색상 | N/A | No imagespec requirement/import, payload renderer or payload service exists. No examples/adapters/scaffold introduced. |
| DOC-08, TEST-02, TEST-05, TEST-09 | 정확한 중앙 test_payload_examples scaffold·실제 HA entry/등록 action schema·production 준비 context/함수·기기 전송 없는 installed imagespec.validate/render 비교·각 예제 크기/색상, current/정확한 하한 실제 버전·pip check·명령/CI 결과, exact pin 재사용 근거·adapter 리뷰(GOV-05) | N/A | No imagespec requirement/import, payload renderer or payload service exists. No examples/adapters/scaffold introduced. |
| DOC-08, CI-05, CI-07, DEP-08 | 공용 Tests/updater의 standards-ref와 reusable full SHA 일치·caller checkout 보존·도구 별도 checkout·resolver 후 패키지 변경 없음·지원 최소 보존·미실행/skip/xfail/deselect를 PASS로 처리하지 않음 | N/A | No imagespec requirement/import, payload renderer or payload service exists. No examples/adapters/scaffold introduced. |
| DOC-07, HA-12 | 기기별 깨우기·인증·타 앱 연결·전송 제약, 실제 검증 경로와 미검증 범위, 공개 문제 로그 비식별화 | PASS | No hardware claims: sleep/wake/firmware and concurrent phone-app conditions explicitly unverified. Actual error/log path, redaction guidance and report details documented; no new issue form. |
| HACS-04, REL-01, REL-02, REL-03, CI-11 | 통합 릴리스 시 같은 검증 commit/tag·manifest 버전·산출물·권한, 사용자 영향·지원 변경·제한 안내 | PASS | Existing0.1.3 version retained; CHANGELOG Unreleased covers behavior and migration impact. Reviewed#4 ZIP contract preserved, next release separate. No existing release/tag/asset modified. |
| REL-04 | 이전/중단 시 README 상단 경로·유지보수 상태·재등록 여부, 자동 이전으로 오인하지 않는 안내 | N/A | Repository is not moved or discontinued; no migration notice applicable. |
| REL-05 (권장) | 의존성/HA API 변경과 기능 변경 분리, 표준 변경은 명시적 채택 PR로 반영 | PASS | HACS ZIP separated in#4; explicit standards+BLE adoption#5. Dependency updater creates its own future update PRs. |
| HACS-04, CI-11 | zip_release/filename·ZIP 루트·추적 파일만 포함·태그/manifest/checkout 일치·동일 SHA 중앙 release action·published 후 asset 첨부·기존 asset 보존·immutable 설정 확인 | PASS | PR#4 squash3dabcba; zip_release true/filename melk_light.zip; central release action validates clean tracked checkout and version/tag, no overwrite. Actual local archive test before merge; no release upload in adoption scope. |

## Executed environments

Each separate environment used the central `actions/python-environment/install.py`, actual installed HA component manifests (bluetooth, bluetooth_adapters, usb and recursive dependencies), then `python -m pytest tests/components/melk_light/ -q --timeout 30` and `python -m pip check`. Exact minimum mode uses INPUT_MINIMUM_PACKAGES=["blesession"]. No skipped/xfail/deselected tests. Current and floor happen to resolve the same blesession version; they were still tested separately.

| Environment | Python / HA / pytest HA plugin | blesession / bleak / connector / pycares | Result |
|---|---|---|---|
| current | 3.14.7 /2026.10.2 /0.13.373 | 0.9.0 /3.0.2 /4.7.1 /5.2.1 |18 passed, pip check PASS |
| current exact floor |3.14.7 /2026.10.2 /0.13.373 |0.9.0 /3.0.2 /4.7.1 /5.2.1 |18 passed, pip check PASS |
| minimum HA current packages |3.13.15 /2025.11.0 /0.13.294 |0.9.0 /1.0.1 /4.4.3 /4.11.0 |18 passed, pip check PASS |
| minimum HA exact floor |3.13.15 /2025.11.0 /0.13.294 |0.9.0 /1.0.1 /4.4.3 /4.11.0 |18 passed, pip check PASS |

Logs: WSL `/home/eigger/.cache/melk-adoption-20261023/{current,current-floor,minimum-current,minimum}.log`, at implementation2e7fa7a (same runtime tree as199f1e1). All four environments were rerun after the translated HA exception and assumed_state metadata follow-up at5bcbad7:18 passed each and pip check PASS. Installed versions remain as tabulated above; logs at the same paths now refer to5bcbad7.

Initial minimum setup failed because HA's aiodns3.x imports result types removed in pycares5. The resolver compatibility constraint pycares<5 fixes that without changing runtime requirements or HA minimum. The old minimum HA test plugin also mocks an older BlueZ import path: the domain fixture additionally mocks only `habluetooth.channels.bluez.MGMTBluetoothCtl.setup` (hardware management socket); real HA manager/setup remains active. Failed runs were not treated as PASS.

## Static and packaging checks

- Pinned central checker from clean Linux LF checkout at reviewed26946: `scripts/check_integration.py .` PASS. The sibling Windows central checkout has CRLF templates, so byte-exact checks use the clean LF checkout. Repository-managed files are LF.
- Ruff0.17.1 check and format31 Python files PASS; actionlint1.7.12 PASS; git diff --check PASS.
- Updater dry-run selects blesession and reports current requirements, no change; no manual workflow dispatch or update PR created.
- Original256x256 PNG icon authored for this repository; no external artwork. Visually inspected; source/license notes in brand/README.md.
- Branch protection API:404 Branch not protected. Existing required checks/settings are not modified.
- Actual clean5bcbad7 archive:17 files at ZIP root, byte-for-byte checkout match, integrity PASS; SHA256 `5ee93225cac058f7b690a1939ce55ebfb273308b58093069a4f156d704e8fce7`. Output `C:/Users/eigger/AppData/Local/Temp/melk-adoption-5bcbad7/melk_light.zip`. No release/tag/upload is authorized by adoption alone.

## Independent review and remaining scope

Independent review of2e7fa7a: no remaining actionable findings after DOC-07 report details were fixed; verified all four18-pass logs and pip check. Review of199f1e1: supported full-SHA official Hassfest source path and active bilingual Discussions links accepted, no new findings. Reviewer also confirmed assumed_state is the accurate IoT class for this write-only lamp. Independent review of5bcbad7 also found no runtime/translation/metadata issues. Its sole formatting note (extra final document blank) is fixed in this evidence-only follow-up. All nine PR checks at5bcbad7 passed, including HACS, full official source Hassfest, central contracts, two lint jobs and four HA/library jobs.

Physical lamp/ESPHome transfer, real HACS installation, firmware/service-change behavior and actual release upload are unverified. These are disclosed limitations, not automated CI success claims. There are no approved template/support-policy exceptions. No imagespec/payload or authentication/migration coverage is applicable because those features are absent.

Central start status d023678a3016ea441b0f556524882ba03ca81c6c and verified-progress df4458459816caf5b0ee19d1a0af526aae4a0067 are recorded; the [central status](https://github.com/eigger/hass-repo-standards/blob/main/docs/adoption-status.md) records the eventual squash merge. The official published Hassfest image rejected categories in run39914054037. The supported reviewed Core source path then passed full remote builds/validation at199f1e1 and5bcbad7 without changing the integration manifest for validation.

## Remote evidence for5bcbad7654b6b8017d05f2156d2cf2e9f245d892

- [Tests: all four HA/library jobs and both lint jobs PASS](https://github.com/eigger/hass-melk-light/actions/runs/39914626173). Each environment ran18 tests, no skips.
- [Validate: HACS, official source-built Hassfest and central template compliance PASS](https://github.com/eigger/hass-melk-light/actions/runs/39914626140).
- [PR #5 final checks](https://github.com/eigger/hass-melk-light/pull/5/checks): the subsequent evidence-only commit reruns the same required checks before merge. Its integration/test/CI tree is unchanged from5bcbad7; earlier results are attributed only to their exact target commit.
- Final local central checker, actionlint1.7.12, ruff0.17.1 and base-to-head git diff --check PASS after the document trailing blank fix.

## Historical scoped ZIP adoption (PR #4)

The following original scoped evidence is retained for its own target commit; it is not current runtime evidence.

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
