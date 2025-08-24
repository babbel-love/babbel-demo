import sys; sys.path.insert(0, ".")
import sys; sys.path.insert(0, ".")
import subprocess,sys
def test_scanners_run():
    r=subprocess.run(["bash","scripts/deny_scan.sh"],capture_output=True,text=True)
    assert r.returncode in (0,1)
