#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later
"""Encode readable panel-mipi-dbi initialization commands."""

import argparse
import hashlib
from pathlib import Path

MAGIC = b"MIPI DBI" + b"\x00" * 7 + b"\x01"


def encode(source: str):
    firmware = bytearray(MAGIC)
    records = []
    for number, line in enumerate(source.splitlines(), 1):
        words = line.split("#", 1)[0].split()
        if not words:
            continue
        try:
            values = [int(value, 0) for value in words[1:]]
        except ValueError as exc:
            raise ValueError(f"invalid number on line {number}") from exc
        if any(value < 0 or value > 255 for value in values):
            raise ValueError(f"byte out of range on line {number}")
        if words[0] == "delay" and len(values) == 1:
            command, params = 0, bytes(values)
        elif words[0] == "command" and values:
            command, params = values[0], bytes(values[1:])
        else:
            raise ValueError(f"invalid record on line {number}")
        if len(params) > 255:
            raise ValueError(f"too many parameters on line {number}")
        firmware.extend((command, len(params)))
        firmware.extend(params)
        records.append((command, params))
    return bytes(firmware), records


def decode(firmware: bytes):
    if firmware[:16] != MAGIC:
        raise ValueError("invalid header")
    position, records = 16, []
    while position < len(firmware):
        if position + 2 > len(firmware):
            raise ValueError("truncated command header")
        command, length = firmware[position:position + 2]
        position += 2
        if position + length > len(firmware):
            raise ValueError("truncated command parameters")
        records.append((command, firmware[position:position + length]))
        position += length
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    arguments = parser.parse_args()
    firmware, expected = encode(arguments.source.read_text(encoding="utf-8"))
    if decode(firmware) != expected:
        raise ValueError("command round-trip mismatch")
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_bytes(firmware)
    decoded = []
    for command, params in expected:
        if command == 0 and len(params) == 1:
            decoded.append(f"delay {params[0]}")
        else:
            decoded.append(
                f"command 0x{command:02x}" +
                "".join(f" 0x{value:02x}" for value in params)
            )
    arguments.output.with_suffix(".decoded.txt").write_text(
        "\n".join(decoded) + "\n", encoding="utf-8"
    )
    checksum = hashlib.sha256(firmware).hexdigest()
    arguments.output.with_suffix(".sha256").write_text(
        f"{checksum}  {arguments.output.name}\n", encoding="ascii"
    )
    print(f"{len(firmware)} bytes, {len(expected)} records, SHA256 {checksum}")


if __name__ == "__main__":
    main()
