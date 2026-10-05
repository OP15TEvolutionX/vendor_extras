# Settings search: confirmed cause and rebuilt OTA
ADB: active Settings.apk expects com.android.settings.intelligence; installed Google provider is enabled. Setup completed. Previous image had both Settings and SettingsGoogle. Direct module tests left base Settings APK in staging.
m installclean then m evolution (evolution_fairlady-userdebug): success, 11:08. Image now contains only SettingsGoogle/SystemUIGoogle. SettingsGoogle search resource points to com.google.android.settings.intelligence. Latest single-scan Idle Manager DEX marker confirmed. OTA CRC OK, OP64DDL1.
APK audit: 483 APKs, 481 unique packages, two remaining RRO collisions: WallpaperPicker2 variants and Poppins system/clock fonts. These source conflicts are not fixed in this OTA. check-apk-duplicates.py is manual and not yet hooked into the build.
PixelOS uses base Settings/SystemUI and GoogleSettingsOverlay for the search provider.
ZIP: /home/ivan/evolutionX/out/target/product/fairlady/EvolutionX-17.0-20261005-fairlady-12.2-Unofficial.zip
Bytes: 5145666726
SHA256: 814d1bb64bf972b271dd75d448b5666314d00474a4ad5216999495be75467e82
No device installation or modification performed.
