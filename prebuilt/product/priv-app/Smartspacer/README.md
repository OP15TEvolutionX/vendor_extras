# Smartspacer ROM integration

Source: https://github.com/KieronQuinn/Smartspacer at 6d51a7c (1.11.3).
Apply `rom-integration.patch` to that revision. It includes the existing ROM
changes that remove the Shizuku requirement, plus direct Google ASI input.
The upstream application is GPL-3.0; SDK modules retain their Apache-2.0 licenses.

The framework overlay routes launcher/system UI sessions to Smartspacer.
The app must therefore read Google targets by binding directly to
`com.google.android.as/com.google.android.apps.miphone.aiai.app.AiAiSmartspaceService`.
Reading the overridden default component would connect Smartspacer to itself.
The required smartspacer-sysconfig.xml adds Smartspacer to the ASI association
allowlist, otherwise ActivityManager rejects the binding before checking permissions.
The privileged branch uses the granted MANAGE_SMARTSPACE permission and does
not require Shizuku. The original Shizuku binding remains for unprivileged use.

Build with Java 21, Android SDK platform 37, Linux build-tools 36.0.0 and
`./gradlew :app:assembleRelease`. Set sdk.dir and MAPS_API_KEY in the ignored
local.properties. Firebase is optional for local builds without google-services.json.
The unsigned release APK is imported by Android.bp and signed with the ROM
platform key. Keep the privapp permission allowlist and the Smartspace overlay.

Runtime checks: filter logcat by SmartspacerUpstream. Expect a connection to
Google ASI and incoming `home`/`lockscreen` target counts, without feedback-loop
warnings. Removing/restarting ASI must not route incoming sessions back to
Smartspacer. Date-only content can mean Google has no contextual cards currently.

## Validation on 2026-10-02

Gradle release assembly and release lint passed (0 errors).
EvolutionX `m Smartspacer smartspacer-sysconfig.xml -j8` completed successfully;
both the platform-signed APK and the sysconfig XML are installed in product staging.
The APK was signed with the same platform certificate as the installed build
and installed successfully with existing app data preserved.
On the current user build, ActivityManager rejected the direct ASI binding:
`association not allowed between packages com.kieronquinn.app.smartspacer and com.google.android.as`.
ASI is exported and requires MANAGE_SMARTSPACE, which Smartspacer has.
The added sysconfig allowlist is required in the next ROM build and is read
at boot. End-to-end Google target delivery remains to be verified after that
ROM is installed. The original APK was restored on the connected phone.

## System background integration (2026-10-03)

Version 9.99.99, versionCode 1000000. Application update checks are
compiled off, including the settings switch; plugin updates remain independent.
The persistent system application runs ordinary services without foreground
notifications. Non-system installation retains the foreground-service fallback.
HOME and AccessibilityService registrations are removed. Foreground package
tracking uses ActivityTaskManager and MANAGE_ACTIVITY_TASKS/REAL_GET_TASKS.
Updated system APKs need the signature-permission allowlist until the factory
APK includes the new permission. Reboot into the updated ROM is required.
Sysconfig grants power-save and data-save exemptions. Both Settings variants
force unrestricted battery mode and disable changing that system exemption.
Runtime APK test: Google ASI connected and delivered home/lockscreen targets;
no Smartspacer notifications were active. Full ROM behavior needs flash/reboot.

Full EvolutionX OTA build succeeded in 08:57 on 2026-10-03.
EvolutionX-17.0-20261003-fairlady-12.2-Unofficial.zip
SHA256: 3a461418ec355e4c3320df42b3054d7432025e4f3ae75c3f4f19534a2f8c5819
Verified product payload hash, ZIP CRC, device metadata, and extracted APK/XML
against staging. Extracted APK is 9.99.99 / 1000000. Compiled SettingsGoogle
resource includes Smartspacer in config_force_battery_unrestrict_mode_apps.
OTA has not been flashed; runtime task permission and immutable battery mode
still need verification after installation.

## Locked mode controls (2026-10-03)

The updated prebuilt retains versionName 9.99.99 and uses versionCode 1000001.
Native and enhanced mode switches are checked and disabled. Their ViewModel
handlers cannot disable integration, the native repository stays enabled, and
saved enhanced mode is enabled when preferences load. Other switches keep their
normal behavior. Source changes are included in rom-integration.patch.
This APK supersedes the one in the OTA documented above; that already-built
ZIP remains the previous build and must be rebuilt to include these controls.

## Hidden controls and opt-in runtime permissions (2026-10-04)

APK versionName 9.99.99 / versionCode 1000002 hides both mode switches while
keeping native/enhanced integration enabled. The accompanying frameworks/base
DefaultPermissionGrantPolicy exception skips automatic runtime grants for
Smartspacer and removes previous SYSTEM_FIXED/GRANTED_BY_DEFAULT flags. Previous
automatic grants are revoked unless user/policy decisions exist. Signature and
privileged integration permissions remain. A newly built ROM is required for
the permission policy; replacing only the APK cannot change existing grants.
