"""Gradebook: merges autograder results + teacher marks into a ledger, CO attainment and dashboards.

Folder layout (private `cs3491-gradebook` repo):
    roster.csv            roll_no,name,github,section
    manual.csv            github,lab,viva,report      (teacher marks; report overrides provisional)
    submissions/*.json    results.json files posted by each lab repo's workflow
Outputs:
    ledger.csv, internal_marks.csv, dashboard.json, DASHBOARD.md
"""
import csv
import json
from pathlib import Path

from .labs import COS, COURSE, LABS, grade_letter


def _read_csv(path):
    p = Path(path)
    if not p.exists():
        return []
    with p.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load(folder):
    folder = Path(folder)
    roster = _read_csv(folder / "roster.csv")
    manual = {(r["github"].lower(), int(r["lab"])): r for r in _read_csv(folder / "manual.csv")}
    best = {}
    for f in sorted((folder / "submissions").glob("*.json")):
        r = json.loads(f.read_text())
        key = ((r.get("student") or "").lower(), int(r["lab"]))
        prev = best.get(key)
        if prev is None or r["auto_total"] > prev["auto_total"] or (
                r["auto_total"] == prev["auto_total"] and r["submitted_at"] > prev["submitted_at"]):
            best[key] = dict(r, attempts=(prev or {}).get("attempts", 0) + 1)
        else:
            prev["attempts"] = prev.get("attempts", 1) + 1
    return roster, manual, best


def link_accounts(roster, best):
    """Fill blank roster GitHub names from the roll number students write in REPORT.md.
    Returns (roster_with_links, unmatched) where unmatched lists submitters not on the roster."""
    rolls = {s["roll_no"]: s for s in roster}
    claimed = {}
    for (gh, _lab), r in sorted(best.items(), key=lambda kv: kv[1].get("submitted_at", "")):
        roll = r.get("roll_no")
        if gh and roll in rolls and not rolls[roll].get("github") and roll not in claimed:
            claimed[roll] = gh
    linked = []
    for s in roster:
        s = dict(s)
        if not s.get("github") and s["roll_no"] in claimed:
            s["github"], s["linked"] = claimed[s["roll_no"]], "auto (REPORT.md roll no)"
        linked.append(s)
    known = {s["github"].lower() for s in linked if s.get("github")}
    unmatched = {}
    for (gh, lab), r in best.items():
        if gh and gh not in known:
            unmatched.setdefault(gh, {"github": gh, "roll_no_written": r.get("roll_no") or "", "labs": []})["labs"].append(lab)
    return linked, sorted(unmatched.values(), key=lambda u: u["github"])


def build(folder, practical_max=100):
    roster, manual, best = load(folder)
    roster, unmatched = link_accounts(roster, best)
    ledger, students = [], []
    for s in roster:
        gh = (s.get("github") or "").lower()
        row = dict(roll_no=s["roll_no"], name=s["name"], github=s.get("github", ""), section=s.get("section", ""),
                   labs={}, co={})
        for lab in LABS:
            sub, man = best.get((gh, lab)), manual.get((gh, lab), {})
            if sub is None:
                status, total = "pending", None
                entry = dict(status=status, score=None)
            else:
                c = sub["components"]
                report = float(man["report"]) if man.get("report") else c["report"]
                viva = float(man["viva"]) if man.get("viva") else None
                total = c["hidden"] + c["quality"] + report + c["ontime"] + (viva or 0)
                late = "late" in sub.get("details", {}).get("ontime", "")
                status = "viva-pending" if viva is None else ("late" if late else "completed")
                entry = dict(status=status, score=round(total, 1), hidden=c["hidden"], viva=viva,
                             attempts=sub.get("attempts", 1), submitted_at=sub["submitted_at"],
                             grade=grade_letter(total))
            row["labs"][lab] = entry
            ledger.append(dict(roll_no=s["roll_no"], name=s["name"], github=s["github"], lab=lab,
                               co=LABS[lab]["co"], status=entry["status"],
                               score="" if entry["score"] is None else entry["score"],
                               grade=entry.get("grade", ""), attempts=entry.get("attempts", 0),
                               submitted_at=entry.get("submitted_at", "")))
        for co in COS:
            labs = [n for n, m in LABS.items() if m["co"] == co]
            scores = [row["labs"][n]["score"] or 0 for n in labs]
            pct = sum(scores) / len(scores)
            row["co"][co] = dict(percent=round(pct, 1), attained=pct >= COURSE["attainment_threshold"])
        done = [e["score"] for e in row["labs"].values() if e["score"] is not None]
        row["completed"] = sum(1 for e in row["labs"].values() if e["status"] in ("completed", "late"))
        row["submitted"] = len(done)
        row["lab_average"] = round(sum(e["score"] or 0 for e in row["labs"].values()) / len(LABS), 1)
        row["internal_practical"] = round(row["lab_average"] * practical_max / 100, 1)
        row["grade"] = grade_letter(row["lab_average"])
        students.append(row)

    n = len(students) or 1
    co_summary = {}
    for co, desc in COS.items():
        attained = sum(1 for s in students if s["co"][co]["attained"])
        pct = 100 * attained / n
        level = 3 if pct >= 70 else 2 if pct >= COURSE["class_target"] else 1 if pct >= 50 else 0
        co_summary[co] = dict(description=desc, students_attained=attained, percent=round(pct, 1),
                              average=round(sum(s["co"][co]["percent"] for s in students) / n, 1),
                              level=level, target_met=pct >= COURSE["class_target"])
    lab_summary = {}
    for lab, meta in LABS.items():
        subs = [s["labs"][lab] for s in students]
        scored = [e["score"] for e in subs if e["score"] is not None]
        lab_summary[lab] = dict(title=meta["title"], co=meta["co"], submitted=len(scored),
                                completed=sum(e["status"] in ("completed", "late") for e in subs),
                                viva_pending=sum(e["status"] == "viva-pending" for e in subs),
                                average=round(sum(scored) / len(scored), 1) if scored else None)
    return dict(course=COURSE, cos=COS, labs={k: v["title"] for k, v in LABS.items()},
                students=students, co_summary=co_summary, lab_summary=lab_summary, ledger=ledger,
                unmatched=unmatched,
                not_linked=[s["roll_no"] for s in roster if not s.get("github")])


ICON = {"completed": "✅", "late": "🕒", "viva-pending": "🎤", "pending": "❌"}


def render_markdown(data):
    L = ["# 📘 CS3491 AI & ML – Lab Dashboard", "",
         "Legend: ✅ completed · 🎤 auto-graded, viva pending · 🕒 completed late · ❌ not submitted", "",
         "## Course outcome attainment", "",
         "| CO | Description | Class avg % | Students attained | % attained | Level | Target |",
         "|---|---|---|---|---|---|---|"]
    for co, c in data["co_summary"].items():
        L.append(f"| {co} | {c['description']} | {c['average']} | {c['students_attained']} | {c['percent']} "
                 f"| {c['level']} | {'✅' if c['target_met'] else '⚠️'} |")
    L += ["", "## Lab summary", "", "| Lab | Title | CO | Submitted | Completed | Viva pending | Avg |",
          "|---|---|---|---|---|---|---|"]
    for lab, s in data["lab_summary"].items():
        L.append(f"| {lab:02d} | {s['title']} | {s['co']} | {s['submitted']} | {s['completed']} | "
                 f"{s['viva_pending']} | {s['average'] if s['average'] is not None else '-'} |")
    L += ["", "## Completion matrix", "",
          "| Roll no | Name | " + " | ".join(f"L{n:02d}" for n in LABS) + " | Done | Avg | Grade |",
          "|---|---|" + "---|" * len(LABS) + "---|---|---|"]
    for s in data["students"]:
        cells = []
        for n in LABS:
            e = s["labs"][n]
            cells.append(ICON[e["status"]] + (f" {e['score']:.0f}" if e["score"] is not None else ""))
        L.append(f"| {s['roll_no']} | {s['name']} | " + " | ".join(cells) +
                 f" | {s['completed']}/{len(LABS)} | {s['lab_average']} | {s['grade']} |")
    pending = [(s, n) for s in data["students"] for n in LABS if s["labs"][n]["status"] == "pending"]
    if data.get("unmatched"):
        L += ["", f"## ⚠️ Submissions not matched to the roster ({len(data['unmatched'])})", "",
              "Their REPORT.md roll no is missing or not on the roster. Fix REPORT.md, or add the GitHub name to roster.csv.", "",
              "| GitHub | Roll no written | Labs |", "|---|---|---|"]
        L += [f"| {u['github']} | {u['roll_no_written'] or '—'} | {', '.join(str(x) for x in sorted(u['labs']))} |"
              for u in data["unmatched"]]
    L += ["", f"GitHub linked: {len(data['students']) - len(data.get('not_linked', []))}/{len(data['students'])} students "
              "(linked automatically from the roll no in REPORT.md)."]
    L += ["", f"## Follow-up list ({len(pending)} pending lab submissions)", ""]
    by_student = {}
    for s, n in pending:
        by_student.setdefault((s["roll_no"], s["name"]), []).append(f"{n:02d}")
    for (roll, name), labs in by_student.items():
        L.append(f"- **{roll} {name}**: labs {', '.join(labs)}")
    return "\n".join(L) + "\n"


def write_all(folder, practical_max=100):
    folder = Path(folder)
    data = build(folder, practical_max)
    (folder / "dashboard.json").write_text(json.dumps(data, indent=2))
    (folder / "DASHBOARD.md").write_text(render_markdown(data), encoding="utf-8")
    with (folder / "ledger.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(data["ledger"][0].keys()) if data["ledger"] else ["roll_no"])
        w.writeheader()
        w.writerows(data["ledger"])
    with (folder / "internal_marks.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["roll_no", "name", "labs_completed", "lab_average_%", f"practical_out_of_{practical_max}",
                    "grade", *COS.keys()])
        for s in data["students"]:
            w.writerow([s["roll_no"], s["name"], s["completed"], s["lab_average"], s["internal_practical"],
                        s["grade"], *(s["co"][c]["percent"] for c in COS)])
    return data
