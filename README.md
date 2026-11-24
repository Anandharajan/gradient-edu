<div align="center">

# 📈 Gradient

**Learn AI & ML like a language: bite-sized lessons, playable sandboxes, and every lab you push to GitHub is auto-graded.**

Built for Anna University **CS3491 Artificial Intelligence and Machine Learning** — 5 units, 12 syllabus labs + 1 exam-prep lab, CO1–CO5.

![License: MIT](https://img.shields.io/badge/license-MIT-58CC02) ![Python](https://img.shields.io/badge/python-3.9%2B-1CB0F6) ![Tests](https://img.shields.io/badge/tests-passing-58CC02) ![Content: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-FF9600)

[**▶ Try the app**](https://anandharajan.github.io/gradient-edu) · [**YouTube lectures**](https://www.youtube.com/@DrAnandharajan) · [**Teacher setup**](docs/TEACHER_SETUP.md) · [**Contribute**](CONTRIBUTING.md)

</div>

## ⚡ 60-second quickstart (no API keys, no GPU)

```bash
pip install git+https://github.com/anandharajan/gradient-edu.git      # soon: pip install gradient-edu
gradient-edu demo          # builds a sample 30-student class + teacher dashboard in under a second
gradient-edu labs          # list the 13 CS3491 labs and course outcomes
```

Or just open **[the app](https://anandharajan.github.io/gradient-edu)**: it runs fully in the browser, with nothing to install.

## How it works

```
YouTube lecture ─► lesson notes ─► quiz ─► 🎮 sandbox ─► 🏰 lab (GitHub Classroom repo)
                                                             │ git push
                         GRADE.md in your repo ◄── hidden-test autograder (every 15 min)
                         teacher dashboard     ◄── CO1–CO5 attainment, completion matrix, marks export
```

| For students | For teachers |
|---|---|
| Duolingo-style skill path: XP, streaks, hearts | One private repo per student per lab (GitHub Classroom) |
| 5 interactive sandboxes: A* vs BFS, Bayes rule, gradient descent, k-means, perceptron/XOR | Hidden tests run on the teacher's grader, never in student repos |
| `gradient-edu check` self-test before pushing | Rubric: hidden tests 50 · quality 10 · report 15 · viva 15 · on-time 10 |
| Marks + feedback in `GRADE.md` within ~15 min; best attempt counts | `DASHBOARD.md` + interactive `teacher.html`: who finished which lab |
| "My progress" page with CO mastery and lab marks | Automatic CO attainment levels (0–3) and internal-marks CSV |

## The 13 labs

| # | Lab | CO | # | Lab | CO |
|---|---|---|---|---|---|
| 1 | Uninformed search (BFS, DFS) | CO1 | 7 | SVM models | CO3 |
| 2 | Informed search (A*, memory-bounded A*, uniform-cost) | CO1 | 8 | Ensembling techniques | CO4 |
| 3 | Naive Bayes models | CO2 | 9 | Clustering algorithms | CO4 |
| 4 | Bayesian networks (inference, learning, drawing) | CO2 | 10 | EM for Bayesian networks | CO2 |
| 5 | Regression models | CO3 | 11 | Simple NN models | CO5 |
| 6 | Decision trees & random forests | CO3 | 12 | Deep learning NN models (architecture comparison) | CO5 |
|  |  |  | 13 | Conditional probability quiz app (exam Q18) | CO2 |

## Teaching with it

See **[docs/TEACHER_SETUP.md](docs/TEACHER_SETUP.md)**: about 1 hour to set up the GitHub org, Classroom, grader and gradebook.
Outcome mapping is in [docs/CO_MAPPING.md](docs/CO_MAPPING.md), and the video funnel in [docs/YOUTUBE_FUNNEL.md](docs/YOUTUBE_FUNNEL.md).

## Contributing

Students and teachers are welcome: new quiz questions, Tamil translations, sandboxes and lessons.
Look for [`good first issue`](../../labels/good%20first%20issue) and read [CONTRIBUTING.md](CONTRIBUTING.md).

## Citation

If you use Gradient in teaching or research, please cite it (see [CITATION.cff](CITATION.cff)).

Code MIT · Lesson content CC BY 4.0 · © 2026 Anandharajan TRV, St. Joseph College of Engineering, Chennai.
Gradient is an independent open-source project and is not affiliated with Duolingo.
