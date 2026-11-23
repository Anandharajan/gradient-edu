# Teacher setup (≈ 1 hour, once per semester)

You will create **one GitHub organisation** with these repositories:

| Repo | Visibility | Contents |
|---|---|---|
| `gradient-edu` (your account) | Public | App, package, docs — the repo people star and fork |
| `cs3491-grader` | **Private** | Hidden tests + model solutions |
| `cs3491-gradebook` | **Private** | Roster, deadlines, viva marks, dashboards (auto-updated) |
| `cs3491-lab-01-bfs-dfs` … `cs3491-lab-12-deep-nn` | Private, **template** | Starter code students receive |
| `cs3491-lab-NN-<slug>-<student>` | Private (auto-created) | Each student's work |

## 1. Organisation and Classroom
1. Apply for **GitHub Education teacher benefits** (education.github.com → Teachers), which gives free private repos and Actions minutes.
2. Create an organisation, e.g. `sjce-aiml`. Settings → Member privileges → Base permission: **No permission**.
3. Go to **classroom.github.com** → New classroom → choose the organisation.
4. Classroom → **Roster** → upload `roll_no` identifiers (one per line). Students link their GitHub account on first login.

## 2. Push the repos
1. Push `cs3491-grader/` and `cs3491-gradebook/` to the org as **private** repos.
2. Push each folder in `lab-templates/` as a private repo and tick **Settings → Template repository**.
3. Push `gradient-edu/` as a **public** repo, then enable **Settings → Pages → Source: GitHub Actions**.

## 3. Grader token
1. Create a **fine-grained personal access token**: Resource owner = the org; repositories = all; permissions: **Contents read & write**, **Metadata read**.
2. In `cs3491-gradebook` → Settings → Secrets → Actions → `GRADER_TOKEN` = the token.
3. Actions tab → **Collect & grade** → *Run workflow* once to test. After that it runs every 15 minutes.

> Why this design? Hidden tests never run inside student repos, so a student cannot edit a workflow to print them.
> Student code runs in a separate process with all tokens removed from its environment.

## 4. Create the 12 assignments
For each lab: Classroom → **New assignment** → Individual →
- Title `cs3491-lab-04-bayes-net` (**exactly the template name**; repos then become `cs3491-lab-04-bayes-net-<username>`)
- Private repos ✔, Template = the matching lab template, deadline = same as `deadlines.json`
- Autograding: none (our grader does it), **Feedback pull request** ✔ (for viva comments)

Copy each invite link into `gradient-edu/app/config.js` → `classroomLinks`, push, and the **Start lab** buttons go live.

## 5. Gradebook files
- `roster.csv`: `roll_no,name,github,section`. Export the Classroom roster after students join.
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
