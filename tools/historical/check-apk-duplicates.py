#!/usr/bin/env python3
"""Check APK package-name collisions in the fairlady image staging directories."""
from pathlib import Path
import subprocess, concurrent.futures, collections, json
root = Path(__file__).resolve().parent
product = root / "out/target/product/fairlady"
aapt = root / "out/host/linux-x86/bin/aapt2"
files = [p for part in ("system", "system_ext", "product", "vendor", "odm", "oem")
         for p in (product / part).rglob("*.apk") if "/apex/" not in str(p)]
def inspect(p):
    r = subprocess.run([str(aapt), "dump", "packagename", str(p)], capture_output=True, text=True, timeout=60)
    return str(p.relative_to(product)), r.stdout.strip() if r.returncode == 0 else None, r.stderr[:200]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    records = list(pool.map(inspect, files))
groups = collections.defaultdict(list)
errors = []
for path, package, error in records:
    if package: groups[package].append(path)
    else: errors.append({"path": path, "error": error})
report = {"apk_count": len(files), "package_count": len(groups),
          "duplicates": {k: v for k, v in groups.items() if len(v) > 1}, "errors": errors}
(root / "apk-duplicate-audit-2026-10-05.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2), flush=True)
raise SystemExit(bool(report["duplicates"] or errors))
