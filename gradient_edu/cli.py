"""Command line interface:  gradient-edu demo | check | grade | gradebook | labs"""
import argparse
import os
import sys
from pathlib import Path

from . import __version__
from .labs import COS, LABS


def cmd_labs(_a):
    print("CS3491 practical exercises\n")
    for n, m in LABS.items():
        print(f"  Lab {n:02d}  [{m['co']}]  {m['title']}")
    print("\nCourse outcomes:")
    for co, d in COS.items():
        print(f"  {co}: {d}")


def cmd_check(a):
    """Student self-check: public tests + lint + report (no hidden tests)."""
    from .grader import run_quality, score_report
    repo = Path(a.repo)
    lab = a.lab or _detect_lab(repo)
    print(f"🔎 Checking Lab {lab:02d} – {LABS[lab]['title']}\n")
    q, qd = run_quality(repo)
    r, rd = score_report(repo)
    print(f"  Public tests + quality : {q}/10   ({qd['public_tests']}, lint: {qd['lint_issues']})")
    print(f"  Report (provisional)   : {r}/15   " + ", ".join(f"{k}: {v}" for k, v in rd.items()))
    print("\nHidden tests (50 marks) run on GitHub when you push. Good luck! 💚")


def _detect_lab(repo):
    for f in sorted((repo / "src").glob("lab*.py")):
        return int(f.stem[3:])
    sys.exit("Could not find src/labNN.py – pass --lab N")


def cmd_grade(a):
    from .grader import grade, render_grade_md, write_outputs
    lab = a.lab or _detect_lab(Path(a.repo))
    r = grade(lab, a.repo, a.hidden, deadline=a.deadline or os.environ.get("LAB_DEADLINE") or None,
              submitted_at=a.submitted_at, student=a.student or os.environ.get("GITHUB_ACTOR"),
              commit=a.commit or os.environ.get("GITHUB_SHA"))
    write_outputs(r, a.out)
    md = render_grade_md(r)
    print(md)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(md)
    print(f"::notice title=Lab {lab:02d} score::{r['auto_total']}/85 ({r['provisional_percent']}%)")


def cmd_gradebook(a):
    from .gradebook import write_all
    data = write_all(a.folder, a.practical_max)
    print(f"Gradebook updated for {len(data['students'])} students → {a.folder}/DASHBOARD.md")
    for co, c in data["co_summary"].items():
        print(f"  {co}: {c['percent']}% students attained (level {c['level']})")


def cmd_collect(a):
    from .collector import collect
    from .gradebook import write_all
    graded = collect(a.gradebook, a.hidden, org=a.org, prefix=a.prefix,
                     token=os.environ.get("GITHUB_TOKEN"), local_dir=a.local_dir,
                     collaborators=a.collaborators)
    print(f"Graded {len(graded)} new commit(s).")
    if (Path(a.gradebook) / "roster.csv").exists():
        write_all(a.gradebook, a.practical_max)
        print("Dashboard rebuilt.")


def cmd_demo(a):
    """No-keys demo: builds a sample class gradebook and teacher dashboard in under a minute."""
    from .demo import run_demo
    run_demo(Path(a.out))


def main(argv=None):
    p = argparse.ArgumentParser(prog="gradient-edu", description="Gradient – CS3491 AI & ML labs, graded on GitHub")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("labs", help="list labs and course outcomes").set_defaults(fn=cmd_labs)
    c = sub.add_parser("check", help="self-check your lab before pushing")
    c.add_argument("--repo", default=".")
    c.add_argument("--lab", type=int)
    c.set_defaults(fn=cmd_check)
    g = sub.add_parser("grade", help="autograde a lab repo (used by GitHub Actions)")
    g.add_argument("--repo", default=".")
    g.add_argument("--lab", type=int)
    g.add_argument("--hidden", required=True, help="path to hidden tests.py")
    g.add_argument("--deadline")
    g.add_argument("--submitted-at")
    g.add_argument("--student")
    g.add_argument("--commit")
    g.add_argument("--out", default=".gradient")
    g.set_defaults(fn=cmd_grade)
    b = sub.add_parser("gradebook", help="rebuild ledger, CO attainment and dashboards")
    b.add_argument("--folder", default=".")
    b.add_argument("--practical-max", type=float, default=100)
    b.set_defaults(fn=cmd_gradebook)
    k = sub.add_parser("collect", help="(teacher) grade new commits from all student lab repos")
    k.add_argument("--gradebook", default=".")
    k.add_argument("--hidden", required=True)
    k.add_argument("--org")
    k.add_argument("--prefix", default="cs3491-lab")
    k.add_argument("--local-dir")
    k.add_argument("--collaborators", action="store_true",
                   help="also grade student-owned lab repos where the token user is a collaborator")
    k.add_argument("--practical-max", type=float, default=100)
    k.set_defaults(fn=cmd_collect)
    d = sub.add_parser("demo", help="60-second demo with a sample class (no keys needed)")
    d.add_argument("--out", default="gradient-demo")
    d.set_defaults(fn=cmd_demo)
    a = p.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
