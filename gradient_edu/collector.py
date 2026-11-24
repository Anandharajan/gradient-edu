"""Collector: runs in the PRIVATE gradebook repo (cron). Finds new commits in student lab repos,
grades them with the hidden tests, saves results, and writes GRADE.md back to each student repo.

Modes:
  GitHub:  gradient-edu collect --org sjce-aiml --prefix cs3491-lab --hidden grader/hidden/tests.py
           (token in env GITHUB_TOKEN with read/write contents on the org's student repos)
  Local :  gradient-edu collect --local-dir path/with/student/repos ...   (used for testing / offline labs)

  Self-serve (default since GitHub Classroom retired on 28 Aug 2026):
           gradient-edu collect --collaborators --hidden ...
           Students create <prefix>-<NN>-<slug> in their OWN account from the public template and add the
           teacher account as a collaborator. The collector accepts those invites, grades each student repo
           and writes GRADE.md back. Needs a CLASSIC token (scope: repo) of the teacher account.

Repo naming: org mode <prefix>-<NN>-<slug>-<github-username> (e.g. cs3491-lab-04-bayes-net-meena);
             self-serve mode <owner>/<prefix>-<NN>-<slug> (owner = student)
On-time is judged by when the collector FIRST SAW the commit (cannot be back-dated by students).
"""
import base64
import datetime as dt
import json
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

API = "https://api.github.com"


def _now():
    return dt.datetime.now(dt.timezone(dt.timedelta(hours=5, minutes=30))).isoformat(timespec="seconds")


def _api(path, token, method="GET", body=None):
    req = urllib.request.Request(API + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {token}",
                                          "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read() or b"null")


def parse_repo_name(name, prefix):
    """'cs3491-lab-04-bayes-net-meena' -> (4, 'meena'); None if not a student lab repo."""
    from .labs import LABS
    for n, meta in LABS.items():
        head = f"{prefix}-{n:02d}-{meta['slug']}-"
        if name.startswith(head) and len(name) > len(head):
            return n, name[len(head):]
    return None


def parse_own_repo_name(name, prefix):
    """Student-owned repo made from the template: 'cs3491-lab-04-bayes-net' -> 4 (owner = student)."""
    from .labs import LABS
    for n, meta in LABS.items():
        if name == f"{prefix}-{n:02d}-{meta['slug']}":
            return n
    return None


def accept_invitations(token, prefix):
    """Accept pending collaborator invitations for lab repos (students add the teacher account)."""
    accepted = []
    for inv in _api("/user/repository_invitations?per_page=100", token) or []:
        repo = inv.get("repository") or {}
        if parse_own_repo_name(repo.get("name", ""), prefix) is not None:
            _api(f"/user/repository_invitations/{inv['id']}", token, "PATCH")
            accepted.append(repo.get("full_name"))
    return accepted


def discover_collaborator_repos(token, prefix):
    """Repos owned by students in which the teacher account is a collaborator: (owner, name, lab, branch)."""
    found, page = [], 1
    while True:
        batch = _api(f"/user/repos?affiliation=collaborator&per_page=100&page={page}", token)
        if not batch:
            break
        for r in batch:
            n = parse_own_repo_name(r["name"], prefix)
            if n is not None:
                found.append((r["owner"]["login"], r["name"], n, r["default_branch"]))
        page += 1
    return found


def load_deadlines(folder):
    p = Path(folder) / "deadlines.json"
    return {int(k): v for k, v in json.loads(p.read_text()).items()} if p.exists() else {}


def grade_checkout(repo_dir, lab, student, sha, hidden, deadline, seen_at, out_dir):
    """Run the grader in a separate process (student code never runs inside the collector)."""
    cmd = [sys.executable, "-m", "gradient_edu.cli", "grade", "--repo", str(repo_dir), "--lab", str(lab),
           "--hidden", str(hidden), "--student", student, "--commit", sha,
           "--submitted-at", seen_at, "--out", str(out_dir)]
    if deadline:
        cmd += ["--deadline", deadline]
    import os
    # never expose tokens/secrets to student code
    env = {k: v for k, v in os.environ.items() if not any(s in k.upper() for s in ("TOKEN", "SECRET", "KEY"))}
    env["PYTHONPATH"] = str(Path(__file__).parent.parent)
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=1800, env=env)
    res = Path(out_dir) / "results.json"
    if proc.returncode != 0 or not res.exists():
        raise RuntimeError(proc.stderr[-500:])
    return json.loads(res.read_text())


def collect(gradebook, hidden, org=None, prefix="cs3491-lab", token=None, local_dir=None, write_back=True,
            collaborators=False):
    gradebook = Path(gradebook)
    (gradebook / "submissions").mkdir(parents=True, exist_ok=True)
    state_p = gradebook / "state.json"
    state = json.loads(state_p.read_text()) if state_p.exists() else {}
    deadlines = load_deadlines(gradebook)
    graded = []

    if local_dir:
        repos = []
        for d in sorted(Path(local_dir).iterdir()):
            parsed = parse_repo_name(d.name, prefix)
            if not parsed or not (d / ".git").exists():
                continue
            sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=d, capture_output=True, text=True).stdout.strip()
            repos.append((None, d.name, parsed, sha, d))
    else:
        repos, page = [], 1
        while org:
            batch = _api(f"/orgs/{org}/repos?per_page=100&page={page}", token)
            if not batch:
                break
            for r in batch:
                parsed = parse_repo_name(r["name"], prefix)
                if parsed:
                    head = _api(f"/repos/{org}/{r['name']}/commits/{r['default_branch']}", token)
                    if "[gradient-bot]" in head["commit"]["message"]:
                        continue  # our own GRADE.md commit
                    repos.append((org, r["name"], parsed, head["sha"], None))
            page += 1
        if collaborators:
            for full in accept_invitations(token, prefix):
                print(f"🤝 accepted collaborator invite: {full}")
            for owner, name, n, branch in discover_collaborator_repos(token, prefix):
                head = _api(f"/repos/{owner}/{name}/commits/{branch}", token)
                if "[gradient-bot]" in head["commit"]["message"]:
                    continue
                repos.append((owner, name, (n, owner), head["sha"], None))

    for owner, name, (lab, student), sha, local_path in repos:
        key = f"{owner}/{name}" if owner and owner != org else name
        st = state.setdefault(key, {})
        if sha in st.get("graded", []):
            continue
        seen_at = st.setdefault("first_seen", {}).setdefault(sha, _now())
        with tempfile.TemporaryDirectory() as tmp:
            if local_path:
                work = local_path
            else:
                work = Path(tmp) / "repo"
                url = f"https://x-access-token:{token}@github.com/{owner}/{name}.git"
                subprocess.run(["git", "clone", "--depth", "1", url, str(work)], check=True, capture_output=True)
            out = Path(tmp) / "out"
            try:
                r = grade_checkout(work, lab, student, sha, hidden, deadlines.get(lab), seen_at, out)
            except Exception as e:  # noqa: BLE001
                print(f"⚠️  {name}@{sha[:7]}: grading failed: {e}")
                continue
            (gradebook / "submissions" / f"{student}-lab{lab:02d}-{sha[:7]}.json").write_text(json.dumps(r, indent=2))
            grade_md = (out / "GRADE.md").read_text(encoding="utf-8")
            if write_back:
                if local_path:
                    (local_path / "GRADE.md").write_text(grade_md, encoding="utf-8")
                    (local_path / ".gradient").mkdir(exist_ok=True)
                    (local_path / ".gradient" / "results.json").write_text(json.dumps(r, indent=2))
                else:
                    _put_file(owner, name, "GRADE.md", grade_md, token)
                    _put_file(owner, name, ".gradient/results.json", json.dumps(r, indent=2), token)
        st.setdefault("graded", []).append(sha)
        graded.append((name, r["auto_total"]))
        print(f"✅ {name}@{sha[:7]} → {r['auto_total']}/85")
    state_p.write_text(json.dumps(state, indent=2))
    return graded


def _put_file(owner, repo, path, content, token):
    try:
        existing = _api(f"/repos/{owner}/{repo}/contents/{path}", token)
        sha = existing.get("sha")
    except Exception:  # noqa: BLE001
        sha = None
    body = {"message": f"[gradient-bot] update {path}", "content": base64.b64encode(content.encode()).decode()}
    if sha:
        body["sha"] = sha
    _api(f"/repos/{owner}/{repo}/contents/{path}", token, "PUT", body)
