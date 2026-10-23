# 문제 해결

[README](../README.ko.md) | [English](troubleshooting.md) | **한국어**

## 공통 문제 해결

먼저 [공통 Bluetooth 문제 해결](https://github.com/eigger/blesession/blob/main/docs/troubleshooting.ko.md)을 확인하세요. 프록시 선택·펌웨어·Home Assistant 등록은 [Bluetooth proxy 안내](https://github.com/eigger/blesession/blob/main/docs/bluetooth.ko.md)를 따르세요.

## 기기별 확인 사항

MELK 조명의 전원을 켜고 연결 가능한 Bluetooth 어댑터 또는 활성 ESPHome 프록시 범위에 두세요. 다시 시도하기 전 다른 제어 앱의 연결을 종료하세요. 동시 앱 연결은 실물 검증하지 않았습니다. 검색은 `MELK-`로 시작하는 이름과, 광고에 있을 경우 MELK 서비스 UUID를 확인합니다. 이 통합에는 페어링·인증 UI가 없습니다. 절전·깨우기 조건과 펌웨어별 차이는 미검증입니다. FFF3에 응답 없는 쓰기를 100ms 간격으로 두 번 보내므로 성공 표시는 기기의 수신 확인이 아닌 추정 상태입니다. 마지막 명령 후 30초 동안 연결을 재사용합니다.

## 증상과 조치

| 증상 | 실패 단계 | 확인 사항 | 조치 |
|---|---|---|---|
| 조명이 검색되지 않음 | 검색 | 전원, `MELK-` 이름과 광고 서비스 | 전원을 켜고 HA Bluetooth의 연결 가능한 광고를 확인하세요. |
| 연결 전 명령 실패 | Unreachable / connect | 연결 가능한 무선 경로, 거리, 다른 앱 | 다른 앱 연결을 종료하고 프록시를 확인한 뒤 재시도하세요. |
| 전송 중 명령 실패 | 쓰기 / 연결 끊김 | 기기 전원과 프록시 연결 | 경로 복구 후 재시도하세요. 실패한 쓰기는 해당 명령의 성공 상태로 반영하지 않습니다. |
| HA 상태와 실제 조명이 다름 | 수신 확인 없음 | 물리 전원 변경 또는 응답 없는 쓰기의 패킷 유실 | 원하는 상태를 다시 보내세요. 실제 기기 상태 피드백은 없습니다. |

## 진단 및 로그

진단 센서·세션 보고 엔티티·진단 다운로드 기능은 없습니다. HA에 표시되는 명령 오류의 예외 상세와 로그를 확인하세요. configuration.yaml의 `logger.logs` 아래 `custom_components.melk_light`와 `blesession`을 일시적으로 `debug`로 지정하고 재시작해 재현한 뒤, 항목을 제거하고 재시작해 해제하세요. 공유 전 Bluetooth 주소·기기 이름·프록시 식별자 등 개인정보를 지우세요. 광고 수신만으로 실제 연결 경로가 동작한다고 판단할 수 없습니다.

## 문제가 계속되는 경우

이 통합의 [기존 Issues 또는 이슈 템플릿](https://github.com/eigger/hass-melk-light/issues)을 이용하세요. 기존 제보 안내를 따라주세요.

확인 가능한 HA·통합·ESPHome·blesession 버전, 조명·프록시 모델과 리비전, 어댑터 또는 프록시 연결 방식, 발생 시각과 실패 단계, 재현 절차와 개인정보를 지운 로그를 함께 알려주세요. 알 수 없는 버전이나 미검증 하드웨어 조건은 명시해 주세요.
