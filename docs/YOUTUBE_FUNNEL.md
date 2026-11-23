# YouTube → app → GitHub funnel

```
Video ─► lesson page (notes + quiz) ─► sandbox ─► "Start lab" (Classroom) ─► push ─► GRADE.md
  ▲                                                                                   │
  └──────────── monthly "contributor spotlight" video ◄── best PRs to public gradient-edu ◄─┘
```

## Playlists (about 50 long videos + Shorts)
| Playlist | Videos |
|---|---|
| 0 · Start here | Course tour · GitHub in 10 min (fork, commit, push) · Lab 0: accept your first assignment |
| Unit I · Problem Solving | 1.1–1.6 (one per lesson, 8–12 min) |
| Unit II · Probabilistic Reasoning | 2.1–2.6 |
| Unit III · Supervised Learning | 3.1–3.5 |
| Unit IV · Ensembles & Unsupervised | 4.1–4.4 |
| Unit V · Neural Networks | 5.1–5.5 |
| Lab walkthroughs | Lab 1–12: problem, interface, `gradient-edu check`, push (no full solution) |
| Shorts | "A* in 60 s", "Why XOR breaks a perceptron", etc., recorded from the sandboxes |
| Spotlights | Monthly: merged student contributions |

## Video template (8–12 min)
1. **Hook (0:00–0:20)**: sandbox animation ("BFS expands 252 nodes, A* only 27. Why?")
2. **Concept (0:20–6:00)**: slides/whiteboard
3. **Demo (6:00–9:00)**: the sandbox, then the lab interface in VS Code
4. **Call to action (last 30 s)**: "Take the quiz and start Lab N; link in the description. Your marks appear in GRADE.md."

## Description template
```
Lesson 1.4 · Heuristic search: A*   (CS3491 · Unit I · CO1)

📗 Notes + quiz: https://anandharajan.github.io/gradient-edu/#lesson-1.4
🎮 Sandbox:     https://anandharajan.github.io/gradient-edu/#sandbox-astar
🏰 Lab 2:       https://anandharajan.github.io/gradient-edu/#lab-2
⭐ Code:        https://github.com/anandharajan/gradient-edu

00:00 Hook  00:20 Concept  06:00 Demo  09:00 Your lab
#CS3491 #MachineLearning #AnnaUniversity
```
Pin a comment with the lab link. After publishing, paste the YouTube id into `app/content.js` (the `video` field of that lesson) and the video appears inside the lesson.

## Metrics to watch
YouTube watch time → app visits (Pages analytics) → Classroom accept rate → labs submitted (dashboard) → stars, forks and outside PRs.
