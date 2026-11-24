"""Public tests (no hidden grader needed)."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from gradient_edu import collector, gradebook, grader  # noqa: E402
from gradient_edu.demo import make_class  # noqa: E402
from gradient_edu.labs import COS, LABS, grade_letter  # noqa: E402


def test_catalogue_matches_cs3491():
    assert len(LABS) == 13 and set(COS) == {"CO1", "CO2", "CO3", "CO4", "CO5"}
    assert {m["co"] for m in LABS.values()} == set(COS)   # every CO has at least one lab


def test_grade_bands():
    assert [grade_letter(s) for s in (95, 85, 75, 65, 58, 52, 30)] == ["O", "A+", "A", "B+", "B", "C", "RA"]


def test_ontime_penalty():
    assert grader.score_ontime("2026-12-01T10:00:00+05:30", "2026-12-01T23:59:00+05:30")[0] == 10
    assert grader.score_ontime("2026-12-03T10:00:00+05:30", "2026-12-01T23:59:00+05:30")[0] == 6


def test_report_scoring(tmp_path):
    (tmp_path / "REPORT.md").write_text("## Aim\n<!-- x -->\n## Algorithm\n" + "w " * 30 + "\n## Observations\n\n## Result\n" + "w " * 30)
    pts, detail = grader.score_report(tmp_path)
    assert pts == 8 and "need 20+" in detail["Aim"]


def test_repo_name_parsing():
    assert collector.parse_repo_name("cs3491-lab-12-deep-nn-arjun", "cs3491-lab") == (12, "arjun")


def test_gradebook_demo(tmp_path):
    data = gradebook.write_all(make_class(tmp_path / "c", n=12), practical_max=25)
    assert len(data["students"]) == 12 and (tmp_path / "c" / "DASHBOARD.md").exists()


def test_cli_demo(tmp_path):
    r = subprocess.run([sys.executable, "-m", "gradient_edu.cli", "demo", "--out", str(tmp_path / "d")],
                       cwd=ROOT, capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr


def test_every_exam_question_has_a_lab():
    from gradient_edu.labs import EXAM_QUESTIONS, EXAM_RUBRIC
    assert len(EXAM_QUESTIONS) == 20 and all(lab in LABS for _, lab in EXAM_QUESTIONS.values())
    assert sum(m for _, m in EXAM_RUBRIC) == 100
