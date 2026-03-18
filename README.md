# hass-melk-light

Home Assistant custom integration for **MELK Light Bar** (`melk_light`).

## Features

- BLE discovery via Home Assistant Bluetooth
- Light control: on/off, brightness, RGB, effect(mode)

## Installation

- Install with HACS (custom repository), or copy `custom_components/melk_light` into your HA config directory.
- Restart Home Assistant.
- Add the integration: **Settings → Devices & Services → Add Integration → MELK Light Bar**

## Notes

- BLE is best with an ESPHome Bluetooth proxy for stability/range.

