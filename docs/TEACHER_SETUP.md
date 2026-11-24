# Teacher setup (≈ 30 minutes, once per semester)

> **GitHub Classroom was retired on 28 Aug 2026.** Gradient therefore uses a *self-serve* flow: **Start lab** creates
> the student's own private repo from a public lab template, and the student adds the teacher account as a
> collaborator so the grader can mark it. (You can later switch to Classroom 50 — see the end of this page.)

| Repo | Visibility | Contents |
|---|---|---|
| `gradient-edu` (your account) | Public | App, package, docs — the repo people star and fork |
| `sjce-aiml/cs3491-grader` | **Private** | Hidden tests + model solutions |
| `sjce-aiml/cs3491-gradebook` | **Private** | Roster, deadlines, viva marks, dashboards (auto-updated) |
| `sjce-aiml/cs3491-lab-01-bfs-dfs` … `cs3491-lab-13-cond-prob-quiz` | **Public template** | Starter code only (no solutions, no hidden tests) |
| `<student>/cs3491-lab-NN-<slug>` | Private (student creates it) | Each student's work; teacher account is a collaborator |

## 1. Organisation and repos (done)
The org, the private grader/gradebook and the 13 public lab templates are already set up. To recreate them,
run `setup_github.ps1` and tick **Settings → Template repository** on every lab repo.

## 2. Grader token (you must do this — it is a credential)
1. github.com → Settings → Developer settings → **Personal access tokens → Tokens (classic)** → Generate new token.
   Scopes: **repo** (and **read:org**). Expiry: end of semester.
   *A classic token is needed because students' repos are in their own accounts; fine-grained org tokens cannot reach them.*
2. `sjce-aiml/cs3491-gradebook` → Settings → Secrets and variables → Actions → New secret `GRADER_TOKEN` = the token.
3. Actions → **Collect & grade** → *Run workflow* once. It then runs every 15 minutes: accepts students'
   collaborator invites for lab repos (only repos named `cs3491-lab-NN-…`), grades new commits, writes `GRADE.md`
   back and rebuilds the dashboard.

> Why this design? Hidden tests never run inside student repos, so a student cannot edit a workflow to print them.
> Student code runs in a separate process with all tokens removed from its environment.

## 3. What students do (per lab)
1. App → lab page → **Start lab** → GitHub's "Create repository" page opens with the template, name and *Private* preset → **Create**.
2. In the new repo: **Settings → Collaborators → Add people → `Anandharajan`**.
3. **Code → Codespaces → Create codespace** (browser VS Code, Python preinstalled), implement, `gradient-edu check`, commit & push.
4. `GRADE.md` appears within ~15 minutes; the teacher dashboard updates.

## 4. Roster
`roster.csv` (`roll_no,name,github,section`) maps GitHub usernames to roll numbers. Collect usernames in week 1
(e.g. a Google Form or a "Lab 0" where students create Lab 1 and add you as collaborator), then fill the file.

## 5. Gradebook files
- `roster.csv`: `roll_no,name,github,section` (see section 4).
- `deadlines.json`: one IST deadline per lab. Late work loses 2 marks per day (max −10).
- `manual.csv`: after each viva add `github,lab,viva,report` (viva /15; `report` optionally overrides the provisional REPORT.md marks /15).

## 6. Each week
| When | Do |
|---|---|
| Before the lab | Release the lesson + lab video; share the invite link |
| In the lab | Students code; `gradient-edu check` for instant feedback |
| After pushes | `GRADE.md` appears in each student repo; `DASHBOARD.md` updates |
| Viva | Ask about their code; add marks to `manual.csv` |
| Friday | Check the **follow-up list** in `DASHBOARD.md`; remind defaulters |

Open `teacher.html` from the app and load `dashboard.json` from the gradebook for the interactive dashboard (filters, CSV export).

## 7. End of semester
- `internal_marks.csv` gives the practical marks (set `--practical-max` in the workflow to your scale).
- `DASHBOARD.md` gives CO attainment per CO with levels 3/2/1/0 (≥70% / ≥60% / ≥50% / <50% of students scoring ≥60%) for NBA.
- Plagiarism: `gh classroom clone student-repos` then run JPlag on the `src/` folders.
- Next year: change seeds and fixtures in `hidden/tests.py`, then regenerate templates with `python scripts/make_lab_templates.py`.

## Later: moving to Classroom 50 (optional)
Classroom 50 (classroom50.org, by the Fifty Foundation) is GitHub's recommended free replacement for Classroom.
It needs the org on the **Team plan**, which is free after GitHub Education teacher verification. Once verified:
create the classroom on `sjce-aiml`, register the 13 templates as assignments, and paste each accept link into
`app/config.js → classroomLinks`; Start lab then uses those links and `gradient-edu collect --org sjce-aiml` grades the org repos.
