# Troubleshooting

[README](../README.md) | **English** | [한국어](troubleshooting.ko.md)

## Common troubleshooting

Start with the [common Bluetooth troubleshooting](https://github.com/eigger/blesession/blob/main/docs/troubleshooting.md). For proxy selection, firmware and Home Assistant registration, use the [Bluetooth proxy guide](https://github.com/eigger/blesession/blob/main/docs/bluetooth.md).

## Device-specific checks

Power the MELK light bar on and keep it within a connectable Bluetooth adapter or active ESPHome proxy's range. Disconnect other controlling apps before retrying; simultaneous app connections have not been hardware tested. Discovery accepts names starting with `MELK-` and, when present, the MELK service UUID. There is no pairing or authentication UI in this integration. Device sleep/wake and firmware variants are unverified. Writes use FFF3 without response, repeated twice at 100 ms intervals; a successful write is an assumed state, not device acknowledgement. Connections are reused for 30 seconds after the last command.

## Symptoms and actions

| Symptom | Failing stage | Checks | Action |
|---|---|---|---|
| Light not discovered | Discovery | Power, `MELK-` name and advertised service | Power on and check connectable advertisements in HA Bluetooth. |
| Command fails before connecting | Unreachable / connect | Connectable radio, range and other app connections | Disconnect the other app, check the proxy, then retry. |
| Command fails during transfer | Write / link loss | Device power and proxy connection | Restore the path and retry; failed writes do not mark that command successful. |
| HA state differs from the lamp | No acknowledgement | Physical power changes or lost write-without-response packets | Send the desired state again; hardware state feedback is unavailable. |

## Diagnostics and logs

No diagnostic sensors, session-report entities or diagnostic download are provided. HA displays a command error; its exception details and logs are the available evidence. Temporarily set `custom_components.melk_light` and `blesession` to `debug` under `logger.logs` in configuration.yaml, restart, reproduce, then remove those entries and restart to disable. Remove Bluetooth addresses, device names, proxy identifiers and other private data before sharing. Advertisement reception alone does not prove a working connection path.

## If the problem persists

Use this integration's [existing Issues or issue template](https://github.com/eigger/hass-melk-light/issues). Follow its existing reporting instructions.

Include the available HA, integration, ESPHome and blesession versions; light/proxy models and revisions; adapter or proxy connection method; occurrence time and failing step; reproduction steps and sanitized logs. Mark unknown versions or unverified hardware conditions explicitly.
