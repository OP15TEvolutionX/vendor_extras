# Fairlady local work and verification — 2026-10-05

These are chronological engineering notes, not guarantees of device behavior.
Read power-review first, then power-fixes, settings-search-fix, and finally
apk-package-guard. Later notes supersede earlier build results and diagnoses.
The final build includes the single-scan Idle Manager, post-boot restoration fix,
LOW_POWER/DEVICE_IDLE support, gesture sensor lifecycle fixes, Google Settings/UI
selection after installclean, unique wallpaper/Poppins overlays, and the mandatory
APK collision audit. Battery gains and vendor perf behavior still require device
measurements. The device was inspected through ADB for the search diagnosis; the
last OTA was not installed by the agent.

All 1317 checked repositories had clean worktrees and no remaining source changes
before this documentation archive. Current commits in the maintained GitHub forks
were verified against live remote refs; earlier changes had already been pushed.
ZIPs, build logs, probe outputs and adb keys are not source changes and remain local.
The root lk_inc.mk is a manifest-managed copy of trusty/vendor/google/aosp/lk_inc.mk.

One-off verification scripts are retained in ../../../tools/historical. They use
historical paths and assumptions and are not current build gates. The supported
APK audit is vendor/lineage/build/tools/check_apk_packages.py and is wired into OTA
packaging. Build fairlady with vendor/extras/tools/build_fairlady.sh.
