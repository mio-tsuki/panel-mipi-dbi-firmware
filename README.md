# Panel MIPI DBI firmware

This repository contains readable initialization commands for Linux's
`panel-mipi-dbi` DRM driver. The firmware files can be reproduced with
Python 3 and do not need proprietary build tools.

The first configuration is for the integrated 240 × 320 SPI display on
**DFRobot UNIHIKER M10 V1.2**, with an ILI9341-compatible controller and
the observed panel marking `HSD028309 D6`. It has not been tested with
other M10 revisions or ILI9341 panels.

## Download and install

Download `dfrobot-unihiker-m10-display.tar.gz` from the
[latest Release](https://github.com/mio-tsuki/panel-mipi-dbi-firmware/releases/latest).
The archive keeps the comma in the binary filename expected by Linux:

```sh
tar -xzf dfrobot-unihiker-m10-display.tar.gz
sha256sum -c SHA256SUMS
sudo install -Dm644 dfrobot,unihiker-m10-display.bin \
  /lib/firmware/dfrobot,unihiker-m10-display.bin
```

GitHub may change the comma in the separately uploaded binary's asset
name to a dot. If you download that asset rather than the archive,
restore the filename when installing.

The Linux device tree identifies this panel using:

```dts
compatible = "dfrobot,unihiker-m10-display", "panel-mipi-dbi-spi";
```

The driver requests `dfrobot,unihiker-m10-display.bin`. If it probes
before the root filesystem is mounted, include the file in the initramfs
or compile it into the kernel using `CONFIG_EXTRA_FIRMWARE`.

## Build from source

Python 3 is the only dependency. From the repository root:

```sh
python3 tools/generate_firmware.py \
  panels/dfrobot,unihiker-m10-display/commands.txt \
  dist/dfrobot,unihiker-m10-display.bin
(cd dist && sha256sum -c ../panels/dfrobot,unihiker-m10-display/SHA256SUMS)
python3 -m unittest discover -s tests -v
```

The generator also writes a decoded command listing and checksum file.
CI checks the output against the tested binary committed to Git.

The M10 V1.2 firmware contains **132 bytes and 25 records**, with SHA-256:

```text
50412ae6d29c5bbfb7fac585528a761fb249d7944011a1b19c5e0f80a0418e5f
```

Read the [panel notes](panels/dfrobot,unihiker-m10-display/README.md)
for the sources of the command sequence, physical test results, and
features that have not been tested.

## License and contributions

The command sequence is derived from the GPL-2.0-or-later Linux
`fb_ili9341.c` driver. Authorship and source functions are noted in
the panel record. The project is distributed under GPL-2.0-or-later;
see [LICENSE](LICENSE).

This is an independent community project; it is not an official DFRobot
firmware release. Configurations for other panels need a separate
compatible string, an identified source and licensing information,
and actual hardware test results. A shared controller model does not
establish that two panels need the same initialization sequence.
