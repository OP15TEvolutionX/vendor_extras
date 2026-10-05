#!/usr/bin/env bash
# Build the Evolution X fairlady product without stale alternate APKs.
set -eo pipefail

task_script_path="$(readlink -f -- "${BASH_SOURCE[0]}")"
task_tree_root="$(cd -- "$(dirname -- "$task_script_path")/../../.." && pwd)"
cd "$task_tree_root"
build_jobs="${1:-12}"
if [[ ! "$build_jobs" =~ ^[1-9][0-9]*$ ]]; then
    echo "Usage: $0 [positive job count]" >&2
    exit 2
fi
source build/envsetup.sh
lunch evolution_fairlady-userdebug
export _JAVA_OPTIONS="${_JAVA_OPTIONS:--Xmx3g}"
mkdir -p logs
build_log="logs/fairlady-$(date +%Y%m%d-%H%M%S).log"
m installclean 2>&1 | tee "$build_log"
m evolution -j"$build_jobs" 2>&1 | tee -a "$build_log"
echo "Build completed; log: $build_log"
