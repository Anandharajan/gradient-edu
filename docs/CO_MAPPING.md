# How notes, sandboxes and labs achieve every CS3491 outcome

Each unit has the same learning loop: **Know** (notes + video) → **Understand** (quiz + sandbox) → **Apply/Build** (graded lab) → **Evidence** (recorded automatically).

| CO | Notes & videos (Know) | Quiz & sandbox (Understand) | Labs (Apply / Build) | Evidence the grader records |
|---|---|---|---|---|
| **CO1** Use appropriate search algorithms for problem solving | 1.1–1.6: AI, agents, BFS/DFS, A*, local search, minimax/α-β, CSP | 14 quiz questions · **A* vs BFS** grid (nodes expanded) | **Lab 1** BFS/DFS · **Lab 2** A* + memory-bounded A* (IDA*) | Correct paths on hidden graphs, optimal cost 418 on Romania, cycle handling |
| **CO2** Apply reasoning under uncertainty | 2.1–2.6: uncertainty, Bayes rule, Naive Bayes, BNs, exact/approximate inference, causal nets & EM | 11 questions · **Bayes-rule slider** (base-rate fallacy) | **Lab 3** Naive Bayes · **Lab 4** BN enumeration · **Lab 10** EM for BN | ≥90% NB accuracy, P(B\|j,m)=0.284, explaining-away, EM matches textbook (0.80/0.52), likelihood never decreases |
| **CO3** Build supervised learning models | 3.1–3.5: least squares, Bayesian LR, GD, logistic regression, SVM, trees & forests | 10 questions · **gradient-descent** fitter (learning-rate divergence) | **Lab 5** regression · **Lab 6** DT/RF · **Lab 7** SVM | Closed form = GD, Bayesian posterior, entropy/info-gain, RF ≥ DT, RBF chosen for moons, ≥94% linear SVM |
| **CO4** Build ensembling and unsupervised models | 4.1–4.4: voting, bagging, boosting, stacking, k-means, KNN, GMM + EM | 7 questions · **k-means** stepper (inertia) | **Lab 8** ensembles · **Lab 9** k-means + KNN | Majority vote, 4 ensembles ≥92%, ARI ≥0.9, KNN ≥90% |
| **CO5** Build deep learning neural network models | 5.1–5.5: perceptron, MLP/backprop, SGD, vanishing gradients/ReLU, dropout/batch norm | 7 questions · **perceptron** (AND/OR converge, XOR fails) | **Lab 11** perceptron + XOR MLP · **Lab 12** ReLU, dropout, batch norm, deep model | XOR solved, inverted dropout scaling, BN mean 0/std 1, ≥95% on digits |

## Attainment calculation (automatic)
- Lab score (100) = hidden 50 + quality 10 + report 15 + viva 15 + on-time 10.
- **Student CO %** = average of that CO's lab scores (missing lab = 0). Attained if ≥ 60%.
- **Class CO level**: 3 if ≥70% of students attain it, 2 if ≥60%, 1 if ≥50%, otherwise 0.
- Thresholds are set in `gradient_edu/labs.py → COURSE`.
- Map to POs with the existing CS3491 CO-PO-PSO matrix (direct attainment). Add the end-of-course survey for indirect attainment (suggested weighting 80/20).

## What students gain
- **Notes**: exam-ready 1-minute summaries per topic. **Videos**: replayable explanations.
- **Sandboxes**: make the maths visible (why A* beats BFS, why XOR needs a hidden layer, why a huge learning rate diverges).
- **Labs**: instant feedback and unlimited retries, so mastery comes before the deadline.
- **GitHub portfolio**: 12 graded repos and optional open-source contributions, useful for placements.
