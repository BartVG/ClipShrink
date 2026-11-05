"""The check. Run:  check.bat   (or: python check.py "a note")
Passes only if every test passes. A skipped test counts as a failure.
Every full run is appended to docs/check_history.md."""
import datetime, subprocess, sys, xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
py = ROOT / ".venv" / "Scripts" / "python.exe"
log = ROOT / "docs" / "check_history.md"
xml = ROOT / "docs" / ".last_check.xml"
label = " ".join(sys.argv[1:]) or "(no note)"
start = datetime.datetime.now()
r = subprocess.run([str(py if py.exists() else sys.executable), "-m", "pytest", "tests", "-q", "--tb=short",
                    "-p", "no:cacheprovider", f"--junitxml={xml}", "-o", "junit_family=xunit2"], cwd=ROOT)
s = ET.parse(xml).getroot()
s = s if s.tag == "testsuite" else s[0]
n, f, e, sk = [int(s.get(k)) for k in ("tests", "failures", "errors", "skipped")]
ok = r.returncode == 0 and n > 0 and f == 0 and e == 0 and sk == 0
took = (datetime.datetime.now() - start).seconds / 60
line = (f"| {start:%Y-%m-%d %H:%M} | {took:.1f} min | {n} | {n - f - e - sk} | "
        f"{f + e} | {sk} | {'PASS' if ok else 'FAIL'} | {label} |\n")
if not log.exists():
    log.write_text("# Every run of the check\n\n| When | Took | Tests | Passed | Failed | Skipped | Result | Note |\n"
                   "|---|---|---|---|---|---|---|---|\n", encoding="utf-8")
with open(log, "a", encoding="utf-8") as h:
    h.write(line)
print(f"\nCHECK {'PASSED' if ok else 'FAILED'}: {n - f - e - sk} of {n} passed, {f + e} failed, {sk} skipped")
sys.exit(0 if ok else 1)
