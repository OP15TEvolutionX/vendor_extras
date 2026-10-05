#!/usr/bin/env python3
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "build_fairlady.sh"

class BuildLauncherTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        script = self.root / "vendor/extras/tools/build_fairlady.sh"
        script.parent.mkdir(parents=True)
        shutil.copy2(SOURCE, script)
        self.script = script
        setup = self.root / "build/envsetup.sh"
        setup.parent.mkdir()
        setup.write_text("lunch() { printf 'lunch %s\\n' \"$*\" >> \"$TASK_CALLS\"; [[ \"$1\" == evolution_fairlady-userdebug ]]; }\n"
                         "m() { printf 'm %s\\n' \"$*\" >> \"$TASK_CALLS\"; if [[ \"$1\" == \"$TASK_FAIL\" ]]; then return 7; fi; }\n")
        (self.root / "run_build.sh").symlink_to(script)
        self.calls = self.root / "calls.txt"

    def run_script(self, target=None, args=(), fail=""):
        env = dict(os.environ, TASK_CALLS=str(self.calls), TASK_FAIL=fail)
        return subprocess.run(["bash", str(target or self.script), *args],
                              cwd="/", env=env, capture_output=True, text=True)

    def test_default_product_clean_then_build(self):
        r = self.run_script()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.calls.read_text().splitlines(),
                         ["lunch evolution_fairlady-userdebug", "m installclean", "m evolution -j12"])
        self.assertTrue(list((self.root / "logs").glob("*.log")))

    def test_manifest_root_symlink_and_custom_jobs(self):
        r = self.run_script(self.root / "run_build.sh", ("4",))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue(self.calls.read_text().endswith("m evolution -j4\n"))

    def test_build_failure_survives_tee(self):
        r = self.run_script(fail="evolution")
        self.assertEqual(r.returncode, 7)
        self.assertNotIn("Build completed", r.stdout)

    def test_clean_failure_prevents_build(self):
        r = self.run_script(fail="installclean")
        self.assertEqual(r.returncode, 7)
        self.assertNotIn("m evolution", self.calls.read_text())

    def test_invalid_job_count(self):
        r = self.run_script(args=("0",))
        self.assertEqual(r.returncode, 2)
        self.assertFalse(self.calls.exists())

if __name__ == "__main__": unittest.main()
