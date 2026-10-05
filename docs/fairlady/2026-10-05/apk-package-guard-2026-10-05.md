# APK duplicate guard
Added a required audit of compiled APK package names in completed target-files, before internal OTA generation and final Evolution X ZIP. Duplicate base APKs, malformed APKs, empty/missing snapshots fail closed. Valid split sets are permitted. Diagnostics name each conflicting path. 15 unit tests (including real Ninja no-op/duplicate blocking cases) and a real SettingsGoogle APK duplicate fixture passed. Generated Ninja graph confirms order-only guard dependencies on both OTA and final ZIP.
Fixed WallpaperPicker2PixelOverlay package identity. Fixed ClockFontPoppinsSourceOverlay package and category to match clock-font overlays; removed its system-font overrides so it only changes the clock.
Full m evolution succeeded in 08:20. Build log apk-package-guard-build.log contains APK package audit OK: 483 APKs, 483 packages before OTA creation. ZIP CRC OK; device OP64DDL1. No device installation performed.
ZIP: /home/ivan/evolutionX/out/target/product/fairlady/EvolutionX-17.0-20261005-fairlady-12.2-Unofficial.zip
Bytes: 5145666954
SHA256: ae9163d605fdd208b468398e04692559efa571c2a6ae1d65630ce54f3d3a4e12
