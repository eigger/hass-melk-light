<!-- hass-standards:header:start -->
# hass-melk-light

Home Assistant custom integration for **MELK Light Bar** (`melk_light`).

**English** | [한국어](README.ko.md)

<!-- hass-standards:badges:start -->
[![Release](https://img.shields.io/github/v/release/eigger/hass-melk-light?style=flat)](https://github.com/eigger/hass-melk-light/releases)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5?style=flat)](#installation)
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
           alt="Turn on device demo"
           src="https://raw.githubusercontent.com/eigger/hass-melk-light/master/docs/images/image1.jpg" />
    </td>
    <td align="center" valign="bottom">
      <img width="360"
           alt="Turn on light demo"
           src="https://raw.githubusercontent.com/eigger/hass-melk-light/master/docs/images/image2.png" />
    </td>
  </tr>
</table>

## Features

- BLE discovery via Home Assistant Bluetooth
- Light control: on/off, brightness, RGB, effect(mode)
- Diagnostic entities: Bluetooth connection, command duration, last failure and error count

## Installation

<!-- hass-standards:installation:start -->
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=eigger&repository=hass-melk-light&category=integration)
<!-- hass-standards:installation:end -->

- Install and configure HACS first, then install with HACS (custom repository), or copy `custom_components/melk_light` into your HA config directory.
- Restart Home Assistant.
- Add the integration: **Settings → Devices & Services → Add Integration → MELK Light Bar**

## Notes

- BLE is best with an ESPHome Bluetooth proxy for stability/range. See [Bluetooth proxy setup](https://github.com/eigger/blesession/blob/main/docs/bluetooth.md) and [troubleshooting](docs/troubleshooting.md).
- Turn on the light bar and disconnect other controlling apps before sending commands. State is assumed from successful writes; the device does not acknowledge commands.
- Connections are reused for 30 seconds after the last command. Failed commands raise an error; retry after checking the Bluetooth path.

## Where to buy

- [AliExpress (150cm)](https://ko.aliexpress.com/item/1005009699069006.html)

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for the real HA test environments and commands.

<!-- hass-standards:support:start -->
## Support

- [Issues](https://github.com/eigger/hass-melk-light/issues): Report bugs or request features.
- [Discussions](https://github.com/eigger/hass-melk-light/discussions): Ask questions and share your experience.
<!-- hass-standards:support:end -->

<!-- hass-standards:related-projects:start -->
## Related Projects

- [blesession](https://github.com/eigger/blesession): Shared BLE sessions and Bluetooth proxy guidance used by this integration.
<!-- hass-standards:related-projects:end -->

<!-- hass-standards:license:start -->
## License

Released under the [MIT License](LICENSE).
<!-- hass-standards:license:end -->
