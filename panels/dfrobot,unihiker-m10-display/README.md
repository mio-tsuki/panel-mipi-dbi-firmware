# DFRobot UNIHIKER M10 V1.2 display

This configuration targets the integrated 240 × 320 RGB565 SPI
display on UNIHIKER M10 V1.2. Its module was marked
`HSD028309 D6` and the controller was ILI9341-compatible.
No other module or board revision has been verified with these bytes.

## Origin and licensing

The readable commands follow the sequence in Linux
`drivers/staging/fbtft/fb_ili9341.c`. The sequence includes settings
from `init_display()`, MADCTL from `set_var()`, and the gamma values
from `set_gamma()`. Copying only `init_display()` would omit the
tested color-order and gamma settings.

That Linux source names Christian Vogelgsang as a copyright holder
and credits earlier work by Noralf Trønnes. Its license is
GPL-2.0-or-later. This command file and the 132-byte derived binary
are distributed under the same license, with readable source and
a reproducible encoder. The independent project does not claim
manufacturer authorization.

## Hardware tests

The exact binary was checked on one UNIHIKER M10 V1.2 on 2026-10-10.
Solid RGB fills, color bars, corners, checkerboard, full and partial
updates, cold/warm initialization, three forced reinitializations,
15 display disable/enable cycles, and backlight control worked.
Using `MADCTL=0x48` corrected the red/blue channel order.

The SPI controller input clock read 100 MHz with `BAUDR=2`,
consistent with 50 MHz pixel transfers; no oscilloscope measurement
was made. Suspend/resume was not tested. The physical active area
was estimated at roughly 44 × 57 mm with a ruler; there is no
confirmed HSD028309 D6 manufacturer dimension sheet.

The Linux `panel-mipi-dbi` driver controls the hardware reset pin.
The GPIO polarity and SPI/PWM settings still need to match the M10
V1.2 device tree. Installing this firmware file does not by itself
provide the kernel DT configuration.

This firmware has not been accepted into the upstream
`linux-firmware` repository.
