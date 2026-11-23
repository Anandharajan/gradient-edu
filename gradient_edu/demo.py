"""Synthetic class for demos and tests (no network, no keys)."""
import csv
import json
import random
import shutil
from pathlib import Path

from .gradebook import write_all
from .labs import LABS, grade_letter

NAMES = ["Aarav", "Divya", "Karthik", "Meena", "Rahul", "Sneha", "Vignesh", "Priya", "Arjun", "Kavya",
         "Surya", "Nithya", "Harish", "Lakshmi", "Pranav", "Swathi", "Gokul", "Revathi", "Ajay", "Deepika",
         "Bala", "Janani", "Ravi", "Sandhya", "Tamil", "Yamini", "Varun", "Keerthi", "Mohan", "Anitha"]


def make_class(folder, n=30, seed=7, deadline_day=10):
    folder = Path(folder)
    if folder.exists():
        shutil.rmtree(folder)
    (folder / "submissions").mkdir(parents=True)
    rng = random.Random(seed)
    roster, manual = [], []
    for i in range(n):
        gh = f"{NAMES[i % len(NAMES)].lower()}-sjce{i:02d}"
        roster.append(dict(roll_no=f"2116230{i + 1:02d}", name=NAMES[i % len(NAMES)], github=gh,
                           section="A" if i < n // 2 else "B"))
        ability = rng.uniform(0.35, 1.0)
        for lab in LABS:
            if rng.random() > 0.35 + 0.6 * ability or lab > 10 and rng.random() < 0.3:
                continue  # not submitted
            for attempt in range(rng.randint(1, 3)):
                hidden = min(50, round(50 * min(1, ability + rng.uniform(-0.2, 0.25) + 0.1 * attempt) / 5) * 5)
                quality = rng.randint(6, 10)
                report = rng.choice([0, 4, 8, 11, 15]) if ability < .6 else rng.choice([11, 15])
                late = rng.random() < 0.12
                ontime = 6 if late else 10
                auto = hidden + quality + report + ontime
                day = deadline_day + (2 if late else -rng.randint(0, 5))
                r = dict(course="CS3491", lab=lab, lab_title=LABS[lab]["title"], co=LABS[lab]["co"],
                         student=gh, commit=f"{rng.getrandbits(40):010x}",
                         submitted_at=f"2026-12-{day:02d}T1{attempt}:00:00+05:30",
                         components=dict(hidden=hidden, quality=quality, report=report, viva=None, ontime=ontime),
                         auto_total=auto, auto_max=85, provisional_percent=round(100 * auto / 85, 1),
                         provisional_grade=grade_letter(100 * auto / 85), tests=[],
                         details=dict(ontime="late by 2.0 day(s)" if late else "on time"))
                (folder / "submissions" / f"{gh}-lab{lab:02d}-{attempt}.json").write_text(json.dumps(r))
            if rng.random() < 0.8:
                manual.append(dict(github=gh, lab=lab, viva=rng.randint(8, 15), report=""))
    for name, rows in (("roster.csv", roster), ("manual.csv", manual)):
        with (folder / name).open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    return folder


def run_demo(out):
    print("Gradient demo: building a sample CS3491 class of 30 students…")
    folder = make_class(out)
    data = write_all(folder)
    teacher_html = Path(__file__).parent / "web" / "teacher.html"
    if teacher_html.exists():
        shutil.copy(teacher_html, folder / "teacher.html")
        (folder / "dashboard.js").write_text("window.DASHBOARD = " + json.dumps(data) + ";")
    print(f"\n✅ Done. Open {folder}/DASHBOARD.md (or teacher.html in a browser).\n")
    for co, c in data["co_summary"].items():
        bar = "█" * int(c["percent"] / 5)
        print(f"  {co} {bar:<20} {c['percent']:5.1f}% attained  (level {c['level']})")
    print(f"\n  Labs submitted: {sum(s['submitted'] for s in data['students'])} / {len(data['students']) * 12}")
