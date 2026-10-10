# SPDX-License-Identifier: GPL-2.0-or-later
"""Check the tested firmware bytes and reject malformed command records."""

import hashlib
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from generate_firmware import MAGIC, decode, encode

PANEL = ROOT / "panels" / "dfrobot,unihiker-m10-display"
DIGEST = "50412ae6d29c5bbfb7fac585528a761fb249d7944011a1b19c5e0f80a0418e5f"


class FirmwareTests(unittest.TestCase):
    def test_verified_firmware(self):
        binary, records = encode((PANEL / "commands.txt").read_text(encoding="utf-8"))
        self.assertEqual(len(binary), 132)
        self.assertEqual(len(records), 25)
        self.assertEqual(binary, (PANEL / "dfrobot,unihiker-m10-display.bin").read_bytes())
        self.assertEqual(hashlib.sha256(binary).hexdigest(), DIGEST)
        self.assertEqual(decode(binary), records)
        self.assertIn((0x36, b"\x48"), records)
        self.assertIn((0x3a, b"\x55"), records)

    def test_bad_source(self):
        for invalid in ("delay 256", "command 0x100", "command", "foo 3", "delay"):
            with self.subTest(source=invalid):
                with self.assertRaises(ValueError):
                    encode(invalid)

    def test_bad_binary(self):
        for invalid in (b"", MAGIC[:-1], MAGIC + b"\x36", MAGIC + b"\x36\x02\x48"):
            with self.subTest(binary=invalid):
                with self.assertRaises(ValueError):
                    decode(invalid)


if __name__ == "__main__":
    unittest.main()
