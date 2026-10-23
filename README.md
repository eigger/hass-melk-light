# hass-melk-light

<!-- hass-standards:badges:start -->
[![Release](https://img.shields.io/github/v/release/eigger/hass-melk-light?style=flat)](https://github.com/eigger/hass-melk-light/releases)
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5?style=flat)](#installation)
[![Home Assistant minimum](https://img.shields.io/badge/HA-%E2%89%A5%202025.11.0-41BDF5?style=flat)](hacs.json)
[![License](https://img.shields.io/github/license/eigger/hass-melk-light?style=flat)](LICENSE)
[![Downloads](https://img.shields.io/github/downloads/eigger/hass-melk-light/total?style=flat&color=41BDF5&label=Downloads)](https://github.com/eigger/hass-melk-light/releases)
<!-- hass-standards:badges:end -->

Home Assistant custom integration for **MELK Light Bar** (`melk_light`).

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

## Installation

- Install with HACS (custom repository), or copy `custom_components/melk_light` into your HA config directory.
- Restart Home Assistant.
- Add the integration: **Settings → Devices & Services → Add Integration → MELK Light Bar**

## Notes

- BLE is best with an ESPHome Bluetooth proxy for stability/range.

## Where to buy

- [AliExpress (150cm)](https://ko.aliexpress.com/item/1005009699069006.html)


