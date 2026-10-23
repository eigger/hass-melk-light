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

Check the diagnostic entities on the device page.

- **Bluetooth connection**: the live BLE link state. Off after the normal 30-second idle disconnect does not mean the lamp is powered off, and differs from advertisement reception.
- **Command duration**: seconds for the latest completed command, with blesession report attributes. Updates after success or failure; a failed idle disconnect also updates it with `operation: disconnect`.
- **Last failure**: the failure timestamp and retained report. A later success does not erase it. Unknown until the first failure.
- **Error count**: failed commands and idle disconnect failures since this entry loaded. Resets to zero on reload/restart; it is not a lifetime statistic. Normal idle disconnects, cancelled commands and unload do not count. Unexpected link loss updates connection status; it counts as an error when it causes a command to fail.

Reports include collected values such as `error`, `failed_stage`, `failed_detail`, `likely_cause`, `likely_cause_key`, `connect_s`, `transfer_s`, `duration_s`, `via`, `via_type`, `rssi` and `paths`. With `via_unconfirmed: true`, `via` is an estimate from advertisement reception rather than a confirmed connection route; a different advertising receiver appears as `advertised_via`. Check `unreachable` (lookup), `connect`, `transfer` (write) and `disconnect` failure stages. No diagnostic download is provided; use entity attributes, HA command errors and logs.

 Temporarily set `custom_components.melk_light` and `blesession` to `debug` under `logger.logs` in configuration.yaml, restart, reproduce, then remove those entries and restart to disable. Remove Bluetooth addresses, device names, proxy identifiers and other private data before sharing. Advertisement reception alone does not prove a working connection path.

## If the problem persists

Use this integration's [existing Issues or issue template](https://github.com/eigger/hass-melk-light/issues). Follow its existing reporting instructions.

Include the available HA, integration, ESPHome and blesession versions; light/proxy models and revisions; adapter or proxy connection method; occurrence time and failing step; reproduction steps and sanitized logs. Mark unknown versions or unverified hardware conditions explicitly.
