<!-- hass-standards:header:start -->
# hass-melk-light

**MELK Light Bar** (`melk_light`)용 Home Assistant 커스텀 통합입니다.

[English](README.md) | **한국어**

<!-- hass-standards:badges:start -->
[![Release](https://img.shields.io/github/v/release/eigger/hass-melk-light?style=flat)](https://github.com/eigger/hass-melk-light/releases)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5?style=flat)](#설치)
[![Home Assistant minimum](https://img.shields.io/badge/HA-%E2%89%A5%202025.11.0-41BDF5?style=flat)](hacs.json)
[![Tests](https://img.shields.io/github/actions/workflow/status/eigger/hass-melk-light/tests.yml?branch=master&style=flat&label=Tests)](https://github.com/eigger/hass-melk-light/actions/workflows/tests.yml)
[![Validate](https://img.shields.io/github/actions/workflow/status/eigger/hass-melk-light/validate.yml?branch=master&style=flat&label=Validate)](https://github.com/eigger/hass-melk-light/actions/workflows/validate.yml)
[![License](https://img.shields.io/github/license/eigger/hass-melk-light?style=flat)](LICENSE)
[![Downloads](https://img.shields.io/github/downloads/eigger/hass-melk-light/total?style=flat&color=41BDF5&label=Downloads)](https://github.com/eigger/hass-melk-light/releases)
<!-- hass-standards:badges:end -->
<!-- hass-standards:header:end -->

<table>
  <tr>
    <td align="center" valign="bottom">
      <img width="270"
           alt="기기 켜기 예시"
           src="https://raw.githubusercontent.com/eigger/hass-melk-light/master/docs/images/image1.jpg" />
    </td>
    <td align="center" valign="bottom">
      <img width="360"
           alt="조명 켜기 예시"
           src="https://raw.githubusercontent.com/eigger/hass-melk-light/master/docs/images/image2.png" />
    </td>
  </tr>
</table>

## 기능

- Home Assistant Bluetooth를 통한 BLE 검색
- 조명 제어: 켜기/끄기, 밝기, RGB, 효과(모드)
- 진단 엔티티: Bluetooth 연결, 명령 소요 시간, 마지막 실패와 오류 횟수

## 설치

<!-- hass-standards:installation:start -->
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=eigger&repository=hass-melk-light&category=integration)
<!-- hass-standards:installation:end -->

- HACS를 먼저 설치·설정한 뒤 사용자 지정 저장소로 설치하거나, HA 설정 폴더에 `custom_components/melk_light`를 복사하세요.
- Home Assistant를 재시작하세요.
- **설정 → 기기 및 서비스 → 통합구성요소 추가 → MELK Light Bar**에서 추가하세요.

## 참고

- 안정성과 수신 범위를 위해 ESPHome Bluetooth 프록시를 권장합니다. [Bluetooth 프록시 설정](https://github.com/eigger/blesession/blob/main/docs/bluetooth.ko.md)과 [문제 해결](docs/troubleshooting.ko.md)을 참고하세요.
- 명령 전 조명 전원을 켜고 다른 제어 앱의 연결을 종료하세요. 기기는 명령 수신 확인을 보내지 않으므로, 표시 상태는 성공한 쓰기를 바탕으로 추정합니다.
- 마지막 명령 후 30초 동안 연결을 재사용합니다. 명령 실패는 오류로 표시되며 Bluetooth 경로를 확인한 뒤 다시 시도하세요.

## 구매처

- [AliExpress (150cm)](https://ko.aliexpress.com/item/1005009699069006.html)

## 개발

실제 HA 테스트 환경과 명령은 [CONTRIBUTING.md (영어)](CONTRIBUTING.md)을 참고하세요.

<!-- hass-standards:support:start -->
## 지원

- [Issues](https://github.com/eigger/hass-melk-light/issues): 버그를 신고하거나 기능을 요청하세요.
- [Discussions](https://github.com/eigger/hass-melk-light/discussions): 질문하고 사용 경험을 공유하세요.
<!-- hass-standards:support:end -->

<!-- hass-standards:related-projects:start -->
## 관련 프로젝트

- [blesession](https://github.com/eigger/blesession): 이 통합에서 사용하는 공용 BLE 세션과 Bluetooth 프록시 안내입니다.
<!-- hass-standards:related-projects:end -->

<!-- hass-standards:license:start -->
## 라이선스

[MIT License](LICENSE) 라이선스로 배포됩니다.
<!-- hass-standards:license:end -->
