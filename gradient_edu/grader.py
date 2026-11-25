"""Autograder: scores a student's lab repo and writes results.json + GRADE.md.

Usage (inside a student lab repo, normally from GitHub Actions):
    gradient-edu grade --lab 4 --repo . --hidden /path/to/hidden/tests.py --deadline 2026-12-01T23:59:00+05:30
"""
import datetime as dt
import importlib.util
import json
import re
import shutil
import signal
import subprocess
import sys
import traceback
from pathlib import Path

from .labs import LABS, RUBRIC, grade_letter, lab_id

TEST_TIMEOUT = 120  # seconds per hidden test


class _Timeout(Exception):
    pass


def _alarm(_sig, _frm):
    raise _Timeout()


def load_module(path, name="student_module"):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(Path(path).parent))
    old, sys.dont_write_bytecode = sys.dont_write_bytecode, True
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path.pop(0)
        sys.dont_write_bytecode = old
    return mod


def run_hidden(lab, module_path, hidden_path):
    hidden = load_module(hidden_path, "hidden_tests").HIDDEN[lab]
    results = []
    try:
        mod = load_module(module_path)
    except Exception as e:  # import error -> zero, but report it
        return [dict(name=n, points=p, earned=0, passed=False, message=f"Import failed: {e}")
                for n, p, _ in hidden]
    use_alarm = hasattr(signal, "SIGALRM")
    for name, points, fn in hidden:
        msg, ok = "", False
        try:
            if use_alarm:
                signal.signal(signal.SIGALRM, _alarm)
                signal.alarm(TEST_TIMEOUT)
            fn(mod)
            ok = True
        except _Timeout:
            msg = f"Timed out after {TEST_TIMEOUT}s"
        except NotImplementedError:
            msg = "Not implemented yet"
        except AssertionError as e:
            msg = f"Wrong answer{': ' + str(e) if str(e) else ''}"
        except Exception as e:
            # keep messages short so hidden-test internals cannot be echoed back to students
            msg = f"{type(e).__name__}: {str(e)[:100]}"
            if "--debug" in sys.argv:
                traceback.print_exc()
        finally:
            if use_alarm:
                signal.alarm(0)
        results.append(dict(name=name, points=points, earned=points if ok else 0, passed=ok, message=msg))
    return results


def run_quality(repo):
    """6 marks if public tests pass, 4 marks if ruff finds no errors."""
    repo = Path(repo)
    detail = {}
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "tests"], cwd=repo,
                       capture_output=True, text=True, timeout=600)
    m = re.search(r"(\d+) passed", r.stdout)
    f = re.search(r"(\d+) failed", r.stdout)
    passed, failed = int(m.group(1)) if m else 0, int(f.group(1)) if f else 0
    total = passed + failed
    pub = round(6 * passed / total) if total else 0
    detail["public_tests"] = f"{passed}/{total} passed"
    ruff = shutil.which("ruff")
    if ruff:
        q = subprocess.run([ruff, "check", "--select", "E9,F63,F7,F82", "--quiet", "src"], cwd=repo,
                           capture_output=True, text=True)
        issues = len([ln for ln in q.stdout.splitlines() if ln.strip() and ":" in ln])
        style = 4 if q.returncode == 0 else max(0, 4 - issues)
        detail["lint_issues"] = issues
    else:
        style, detail["lint_issues"] = 4, "ruff not installed (full marks)"
    return pub + style, detail


REPORT_SECTIONS = ["Aim", "Algorithm", "Observations", "Result"]


def read_roll_no(repo):
    """Roll number the student typed in REPORT.md ('Roll no: 212924106001'); None if missing."""
    p = Path(repo) / "REPORT.md"
    if not p.exists():
        return None
    m = re.search(r"Roll\s*no\.?\s*[:\-]?\s*(\d{12})", re.sub(r"<!--.*?-->", "", p.read_text(encoding="utf-8"), flags=re.S),
                  re.I)
    return m.group(1) if m else None


def score_report(repo):
    """Provisional: 15 marks spread over 4 required sections; each needs >= 20 words of your own."""
    p = Path(repo) / "REPORT.md"
    if not p.exists():
        return 0, {"missing": "REPORT.md"}
    text = p.read_text(encoding="utf-8")
    detail, earned = {}, 0.0
    for sec in REPORT_SECTIONS:
        m = re.search(rf"^##\s*{sec}\s*$(.*?)(?=^##\s|\Z)", text, re.S | re.M | re.I)
        body = re.sub(r"<!--.*?-->", "", m.group(1), flags=re.S) if m else ""
        words = len(re.findall(r"\w+", body))
        ok = words >= 20
        detail[sec] = f"{words} words" + ("" if ok else " (need 20+)")
        earned += 15 / len(REPORT_SECTIONS) if ok else 0
    return round(earned), detail


def score_ontime(submitted_at, deadline):
    if not deadline:
        return 10, "no deadline set"
    sub = dt.datetime.fromisoformat(submitted_at)
    due = dt.datetime.fromisoformat(deadline)
    if sub <= due:
        return 10, "on time"
    days = (sub - due).total_seconds() / 86400
    pts = max(0, 10 - 2 * int(days + 0.999))
    return pts, f"late by {days:.1f} day(s)"


def grade(lab, repo, hidden_path, deadline=None, submitted_at=None, student=None, commit=None):
    lab = int(lab)
    repo = Path(repo)
    module_path = repo / "src" / f"{lab_id(lab)}.py"
    submitted_at = submitted_at or dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    tests = run_hidden(lab, module_path, hidden_path)
    hidden_score = sum(t["earned"] for t in tests)
    quality, qdetail = run_quality(repo)
    report, rdetail = score_report(repo)
    ontime, odetail = score_ontime(submitted_at, deadline)
    comps = {"hidden": hidden_score, "quality": quality, "report": report, "viva": None, "ontime": ontime}
    auto_total = sum(v for v in comps.values() if v is not None)
    result = dict(
        course="CS3491", lab=lab, lab_title=LABS[lab]["title"], co=LABS[lab]["co"],
        student=student, roll_no=read_roll_no(repo), commit=commit, submitted_at=submitted_at,
        components=comps, auto_total=auto_total, auto_max=85,
        provisional_percent=round(100 * auto_total / 85, 1),
        provisional_grade=grade_letter(100 * auto_total / 85),
        tests=tests, details={"quality": qdetail, "report": rdetail, "ontime": odetail},
    )
    return result


def render_grade_md(r):
    lines = [
        f"# 📊 Lab {r['lab']:02d} – {r['lab_title']}",
        "",
        f"**Course outcome:** {r['co']}  |  **Submitted:** {r['submitted_at']}  |  **Commit:** `{(r['commit'] or '-')[:7]}`",
        "",
        f"## Score: {r['auto_total']} / 85 auto marks → provisional **{r['provisional_percent']}% ({r['provisional_grade']})**",
        "_Viva (15) is added by your teacher; final marks appear on the dashboard._",
        "",
        "| Component | Max | Marks |",
        "|---|---|---|",
    ]
    for key, label, mx, _ in RUBRIC:
        v = r["components"][key]
        lines.append(f"| {label} | {mx} | {'⏳ teacher' if v is None else v} |")
    lines += ["", "## Hidden tests", "", "| Test | Points | Result |", "|---|---|---|"]
    for t in r["tests"]:
        res = "✅ passed" if t["passed"] else f"❌ {t['message']}"
        lines.append(f"| {t['name']} | {t['points']} | {res} |")
    d = r["details"]
    lines += ["", "## Feedback",
              f"- Public tests: {d['quality'].get('public_tests')}; lint issues: {d['quality'].get('lint_issues')}",
              "- Report: " + ", ".join(f"{k}: {v}" for k, v in d["report"].items()),
              f"- Submission: {d['ontime']}", "",
              "Push again to improve your score — your best attempt counts. 💚"]
    return "\n".join(lines) + "\n"


def badge_json(r):
    pct = r["provisional_percent"]
    color = "brightgreen" if pct >= 80 else "green" if pct >= 60 else "yellow" if pct >= 50 else "red"
    return {"schemaVersion": 1, "label": f"Lab {r['lab']:02d}", "message": f"{pct}% {r['provisional_grade']}",
            "color": color}


def write_outputs(r, outdir):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "results.json").write_text(json.dumps(r, indent=2))
    (out / "GRADE.md").write_text(render_grade_md(r), encoding="utf-8")
    (out / "badge.json").write_text(json.dumps(badge_json(r)))
