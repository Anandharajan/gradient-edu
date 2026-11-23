# Contributing to Gradient

Thank you! Contributions from CS3491 students count toward the **project component (CO6)**.

## Tiers
| Tier | Examples | Label |
|---|---|---|
| 🥉 Bronze | New quiz questions, typo fixes, Tamil translation of notes, docs | `good first issue` |
| 🥈 Silver | A new lesson, a new dataset, improving a lab README | `intermediate` |
| 🥇 Gold | A new sandbox (e.g. minimax tree, GMM ellipses, dropout visualiser), app features | `advanced` |

## How
1. Fork → branch → change → open a pull request that references the issue.
2. **Quiz/lesson content** lives in `app/content.js`. Each question needs 4 options, the index `c` of the correct one, and one clearly correct answer.
3. **Sandboxes** go in `app/index.html` (`sbXxx` functions). Keep them dependency-free and use the colour variables.
4. Run `pytest -q tests` and open `app/index.html` in a browser before you submit.
5. Never submit lab solutions to this repo. Hidden tests and solutions are kept private.

## Style
Python: `ruff check`. Front-end: plain JS, the Nunito font, and the colour variables in `:root`. Please be kind in reviews.
