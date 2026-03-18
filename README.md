# hass-melk-light
[![HACS](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?logo=home-assistant)](https://hacs.xyz/)
[![GitHub Release](https://img.shields.io/github/release/eigger/hass-melk-light.svg)](https://github.com/eigger/hass-melk-light/releases)
[![License](https://img.shields.io/github/license/eigger/hass-melk-light)](https://github.com/eigger/hass-melk-light/blob/main/LICENSE)
![integration usage](https://img.shields.io/badge/dynamic/json?color=41BDF5&logo=home-assistant&label=integration%20usage&suffix=%20installs&cacheSeconds=15600&url=https://analytics.home-assistant.io/custom_integrations.json&query=%24.melk_light.total)

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


