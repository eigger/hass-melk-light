"""Packet builders for MELK LED bar protocol (9 bytes fixed)."""

from __future__ import annotations

from .constants import FOOTER, HEADER, PAD


def _build_packet(
    length: int,
    cmd: int,
    d0: int = PAD,
    d1: int = PAD,
    d2: int = PAD,
    d3: int = PAD,
    d4: int = 0x00,
) -> bytes:
    return bytes([HEADER, length, cmd, d0, d1, d2, d3, d4, FOOTER])


def packet_power(on: bool) -> bytes:
    v = 0x01 if on else 0x00
    return _build_packet(0x04, 0x04, v, 0x00, v, PAD, 0x00)


def packet_rgbw_status(flags: int, light_mode: int, value: int) -> bytes:
    """RGBW Status (CMD 0x04) used by the reference app.

    Byte3: flags (bitfield), Byte4: light_mode, Byte5: value.
    Remaining bytes are padding.
    """
    return _build_packet(0x04, 0x04, flags & 0xFF, light_mode & 0xFF, value & 0xFF, PAD, 0x00)


def packet_brightness(brightness: int, light_mode: int = 0xFF) -> bytes:
    brightness = max(0, min(255, int(brightness)))
    return _build_packet(0x04, 0x01, brightness, light_mode, PAD, PAD, 0x00)


def packet_color(r: int, g: int, b: int) -> bytes:
    return _build_packet(0x07, 0x05, 0x03, r & 0xFF, g & 0xFF, b & 0xFF, 0x10)


def packet_color_temperature(warm: int, cold: int) -> bytes:
    return _build_packet(0x06, 0x05, 0x02, warm & 0xFF, cold & 0xFF, PAD, 0x08)


def packet_single_color(value: int) -> bytes:
    """Single-color (W) value.

    The reference app sends a 0..100 value here (derived from palette degree/percent)
    for devices/channels that use "single color" instead of RGB/CT.
    """
    value = max(0, min(255, int(value)))
    return _build_packet(0x05, 0x05, 0x01, value & 0xFF, PAD, PAD, 0x08)


def packet_mode(mode: int) -> bytes:
    return _build_packet(0x05, 0x03, mode & 0xFF, 0x06, PAD, PAD, 0x00)


def packet_mode_speed(speed: int) -> bytes:
    speed = max(0, min(255, int(speed)))
    return _build_packet(0x04, 0x02, speed, PAD, PAD, PAD, 0x00)


def packet_scene(scene: int) -> bytes:
    return _build_packet(0x05, 0x31, scene & 0xFF, 0x07, PAD, PAD, 0x01)


def packet_mic_onoff(on: bool) -> bytes:
    v = 0x01 if on else 0x00
    return _build_packet(0x04, 0x07, v, PAD, PAD, PAD, 0x00)


def packet_mic_sensitivity(sensitivity: int) -> bytes:
    return _build_packet(0x04, 0x06, int(sensitivity) & 0xFF, PAD, PAD, PAD, 0x00)


def packet_mic_eq_mode(eq_mode: int) -> bytes:
    # 0..7 -> 0x80..0x87
    return _build_packet(0x07, 0x03, (int(eq_mode) + 0x80) & 0xFF, 0x04, PAD, PAD, 0x00)

