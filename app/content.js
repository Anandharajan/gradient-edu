// CS3491 course content: units → lessons (notes + video + quiz) → lab castle.
// Contributors: add lessons/questions here (see CONTRIBUTING.md). Video ids are YouTube ids ("" = coming soon).
window.COURSE = {
  code: "CS3491",
  title: "Artificial Intelligence and Machine Learning",
  channel: "https://www.youtube.com/@DrAnandharajan",
  org: "https://github.com/sjce-aiml",
  units: [
    {
      n: 1, title: "Problem Solving", co: "CO1", color: "#58CC02", sandbox: "astar",
      lessons: [
        { id: "1.1", title: "What is AI?", video: "",
          notes: "AI builds agents that perceive an environment and act to maximise performance. Applications: search engines, games, robotics, medical diagnosis, recommendation and speech. Russell & Norvig frame AI as acting rationally.",
          quiz: [
            { q: "An agent that acts to achieve the best expected outcome is called…", a: ["Rational", "Random", "Reflexive", "Omniscient"], c: 0 },
            { q: "Which is NOT a typical AI application?", a: ["Spam filtering", "Route planning", "Compiling C code", "Face recognition"], c: 2 } ] },
        { id: "1.2", title: "Problem-solving agents", video: "",
          notes: "A search problem = initial state, actions, transition model, goal test and path cost. The agent formulates a goal, formulates the problem, searches for a solution and executes it.",
          quiz: [
            { q: "Which is NOT part of a search problem definition?", a: ["Initial state", "Goal test", "Path cost", "Learning rate"], c: 3 },
            { q: "The transition model tells us…", a: ["The result of doing an action in a state", "The cost of the best path", "The heuristic value", "The number of states"], c: 0 } ] },
        { id: "1.3", title: "Uninformed search: BFS & DFS", video: "", lab: 1,
          notes: "BFS expands the shallowest node first using a FIFO queue: complete and optimal for unit step costs, but memory O(b^d). DFS expands the deepest node using a LIFO stack: memory O(bm), but not optimal and can loop without a visited set.",
          quiz: [
            { q: "BFS uses which data structure for the frontier?", a: ["FIFO queue", "LIFO stack", "Priority queue", "Hash map"], c: 0 },
            { q: "Which search is optimal when all step costs are equal?", a: ["DFS", "BFS", "Depth-limited", "Greedy"], c: 1 },
            { q: "DFS memory complexity is…", a: ["O(b^d)", "O(bm)", "O(d)", "O(b)"], c: 1 } ] },
        { id: "1.4", title: "Heuristic search: A*", video: "", lab: 2,
          notes: "A* orders nodes by f(n) = g(n) + h(n). With an admissible heuristic (never overestimates) tree-search A* is optimal. Memory-bounded variants (IDA*, SMA*) trade time for memory by re-expanding nodes.",
          quiz: [
            { q: "In A*, f(n) =", a: ["g(n)", "h(n)", "g(n) + h(n)", "g(n) × h(n)"], c: 2 },
            { q: "An admissible heuristic…", a: ["Never overestimates the true cost", "Is always zero", "Always overestimates", "Ignores the goal"], c: 0 },
            { q: "IDA* reduces…", a: ["Time", "Memory", "Optimality", "Branching factor"], c: 1 } ] },
        { id: "1.5", title: "Local search & optimisation", video: "",
          notes: "Local search keeps one current state and moves to neighbours: hill climbing (can get stuck in local maxima), simulated annealing (accepts bad moves with decreasing probability) and genetic algorithms.",
          quiz: [
            { q: "Hill climbing can get stuck at a…", a: ["Local maximum", "Global minimum only", "Goal state", "Leaf node"], c: 0 },
            { q: "Simulated annealing escapes local maxima by…", a: ["Sometimes accepting worse moves", "Restarting BFS", "Using a heuristic of zero", "Sorting states"], c: 0 } ] },
        { id: "1.6", title: "Adversarial search & CSP", video: "",
          notes: "Minimax chooses the move with the best worst-case outcome; alpha-beta pruning skips branches that cannot change the decision. CSPs have variables, domains and constraints, solved by backtracking with heuristics (MRV) and propagation (forward checking, arc consistency).",
          quiz: [
            { q: "Alpha-beta pruning changes the minimax result?", a: ["Never", "Always", "Only in chess", "Only with bad ordering"], c: 0 },
            { q: "MRV heuristic picks the variable with…", a: ["Fewest legal values", "Most legal values", "Highest degree only", "Random order"], c: 0 } ] }
      ]
    },
    {
      n: 2, title: "Probabilistic Reasoning", co: "CO2", color: "#1CB0F6", sandbox: "bayes",
      lessons: [
        { id: "2.1", title: "Acting under uncertainty", video: "",
          notes: "Agents rarely know the world exactly. Probability summarises uncertainty; decision theory = probability theory + utility theory. Rational agents maximise expected utility.",
          quiz: [{ q: "Decision theory combines probability theory with…", a: ["Utility theory", "Graph theory", "Set theory", "Number theory"], c: 0 }] },
        { id: "2.2", title: "Bayesian inference", video: "",
          notes: "Bayes' rule: P(H|E) = P(E|H) P(H) / P(E). It turns causal knowledge P(effect|cause) into diagnostic knowledge P(cause|effect). Try the Bayes slider sandbox!",
          quiz: [
            { q: "In Bayes' rule, P(H) is called the…", a: ["Prior", "Likelihood", "Posterior", "Evidence"], c: 0 },
            { q: "A test is 99% accurate and the disease is rare. A positive result means disease is…", a: ["Certain", "Still fairly unlikely", "Impossible", "Exactly 99% likely"], c: 1 } ] },
        { id: "2.3", title: "Naive Bayes models", video: "", lab: 3,
          notes: "Naive Bayes assumes features are conditionally independent given the class: P(C|x) ∝ P(C) Π P(xi|C). Gaussian NB models each feature per class with a mean and variance. Fast, works well for text and small data.",
          quiz: [
            { q: "The 'naive' assumption is that features are…", a: ["Conditionally independent given the class", "Normally distributed", "Binary", "Equal"], c: 0 },
            { q: "Gaussian NB stores per class and feature a…", a: ["Mean and variance", "Decision threshold", "Weight vector", "Kernel"], c: 0 } ] },
        { id: "2.4", title: "Bayesian networks", video: "", lab: 4,
          notes: "A Bayesian network is a DAG; each node has a CPT P(X | Parents(X)). The joint distribution factorises as Π P(Xi | Parents(Xi)). Example: Burglary → Alarm ← Earthquake; Alarm → JohnCalls, MaryCalls.",
          quiz: [
            { q: "Each node in a BN stores…", a: ["P(X | Parents(X))", "P(X) only", "The full joint", "A utility"], c: 0 },
            { q: "A BN graph must be…", a: ["Directed and acyclic", "Undirected", "A tree", "Complete"], c: 0 } ] },
        { id: "2.5", title: "Exact & approximate inference", video: "",
          notes: "Inference by enumeration sums the joint over hidden variables (exact, exponential). Variable elimination reuses factors. Approximate inference samples: rejection sampling, likelihood weighting and Gibbs sampling (MCMC).",
          quiz: [
            { q: "Likelihood weighting is a form of…", a: ["Approximate inference", "Exact inference", "Learning", "Search"], c: 0 },
            { q: "Enumeration on large networks is…", a: ["Exponential in the worst case", "Always linear", "Constant", "Impossible"], c: 0 } ] },
        { id: "2.6", title: "Causal networks & EM", video: "", lab: 10,
          notes: "Causal networks support interventions: do(X=x) cuts incoming edges to X. When variables are hidden, Expectation-Maximisation alternates E-step (expected hidden values) and M-step (re-estimate parameters); the likelihood never decreases.",
          quiz: [
            { q: "In EM, the M-step…", a: ["Re-estimates parameters", "Computes expectations", "Prunes the graph", "Adds edges"], c: 0 },
            { q: "Each EM iteration makes the likelihood…", a: ["Not decrease", "Decrease", "Random", "Zero"], c: 0 } ] }
      ]
    },
    {
      n: 3, title: "Supervised Learning", co: "CO3", color: "#FF9600", sandbox: "regression",
      lessons: [
        { id: "3.1", title: "Linear regression & least squares", video: "", lab: 5,
          notes: "Model y = w·x + b. Least squares minimises Σ(y − ŷ)²; closed form w = (XᵀX)⁻¹Xᵀy. Multiple regression uses many input variables. Bayesian linear regression puts a prior on w and returns a posterior distribution.",
          quiz: [
            { q: "Least squares minimises…", a: ["Sum of squared errors", "Absolute errors", "Number of errors", "Margin"], c: 0 },
            { q: "Bayesian linear regression returns…", a: ["A distribution over weights", "One tree", "Cluster labels", "A kernel"], c: 0 } ] },
        { id: "3.2", title: "Gradient descent", video: "",
          notes: "Update w ← w − η ∇L(w). Too large a learning rate diverges, too small is slow. Batch GD uses all data; stochastic GD uses one sample; mini-batch is in between. Try the regression sandbox!",
          quiz: [
            { q: "If the learning rate is too large, GD may…", a: ["Diverge", "Always converge faster", "Stop immediately", "Become exact"], c: 0 } ] },
        { id: "3.3", title: "Linear classification & logistic regression", video: "",
          notes: "Discriminant functions split classes directly. Probabilistic discriminative models (logistic regression) model P(C|x) = σ(w·x). Generative models (Naive Bayes) model P(x|C)P(C).",
          quiz: [
            { q: "Logistic regression is a…", a: ["Discriminative model", "Generative model", "Clustering method", "Search method"], c: 0 },
            { q: "The sigmoid outputs values in…", a: ["(0, 1)", "(−1, 1)", "[0, ∞)", "Any real"], c: 0 } ] },
        { id: "3.4", title: "Support vector machines", video: "", lab: 7,
          notes: "SVM finds the maximum-margin hyperplane; only support vectors matter. Margin width = 2/‖w‖. Kernels (RBF, polynomial) separate non-linear data by implicitly mapping to higher dimensions.",
          quiz: [
            { q: "SVM maximises the…", a: ["Margin", "Error", "Depth", "Entropy"], c: 0 },
            { q: "For moon-shaped data the best kernel is usually…", a: ["RBF", "Linear", "None", "Identity"], c: 0 } ] },
        { id: "3.5", title: "Decision trees & random forests", video: "", lab: 6,
          notes: "Trees split on the feature with highest information gain (entropy drop). Deep trees overfit. Random forests average many trees trained on bootstrap samples with random feature subsets, reducing variance.",
          quiz: [
            { q: "Entropy of [1,1,0,0] is…", a: ["1 bit", "0", "0.5", "2 bits"], c: 0 },
            { q: "Random forests mainly reduce…", a: ["Variance", "Bias only", "Training data", "Features"], c: 0 } ] }
      ]
    },
    {
      n: 4, title: "Ensembles & Unsupervised", co: "CO4", color: "#CE82FF", sandbox: "kmeans",
      lessons: [
        { id: "4.1", title: "Combining learners & voting", video: "", lab: 8,
          notes: "Model combination: voting (majority/average), bagging (bootstrap + average, reduces variance), boosting (sequentially focus on mistakes, e.g. AdaBoost, reduces bias) and stacking (a meta-learner combines base predictions).",
          quiz: [
            { q: "AdaBoost increases the weight of…", a: ["Misclassified samples", "Correct samples", "All features", "Outliers only"], c: 0 },
            { q: "Stacking uses a…", a: ["Meta-learner", "Single tree", "Kernel", "Heuristic"], c: 0 } ] },
        { id: "4.2", title: "K-means clustering", video: "", lab: 9,
          notes: "Repeat: assign each point to the nearest centroid, then move each centroid to the mean of its points. Minimises within-cluster squared distance (inertia). Needs k; sensitive to initialisation (use k-means++).",
          quiz: [
            { q: "K-means minimises…", a: ["Within-cluster squared distance", "Number of clusters", "Margin", "Entropy"], c: 0 },
            { q: "k-means++ improves…", a: ["Initialisation", "Distance metric", "Labels", "Speed of prediction only"], c: 0 } ] },
        { id: "4.3", title: "Instance-based learning: KNN", video: "",
          notes: "KNN stores the training data and predicts by majority vote of the k nearest neighbours. Small k → noisy; large k → smooth. Scale features first!",
          quiz: [{ q: "KNN is called a lazy learner because…", a: ["It does no work until prediction", "It is slow to train", "It ignores data", "It uses gradients"], c: 0 }] },
        { id: "4.4", title: "Gaussian mixtures & EM", video: "",
          notes: "A GMM models data as a weighted sum of Gaussians. EM: E-step computes soft responsibilities; M-step updates means, covariances and weights. K-means is the hard-assignment special case.",
          quiz: [{ q: "In a GMM, the E-step computes…", a: ["Soft cluster responsibilities", "New means", "The kernel", "The margin"], c: 0 }] }
      ]
    },
    {
      n: 5, title: "Neural Networks", co: "CO5", color: "#FF4B4B", sandbox: "perceptron",
      lessons: [
        { id: "5.1", title: "Perceptron", video: "", lab: 11,
          notes: "Output = step(w·x + b). Learning rule: w ← w + η(y − ŷ)x. Converges for linearly separable data (AND, OR) but cannot learn XOR.",
          quiz: [
            { q: "A single perceptron cannot learn…", a: ["XOR", "AND", "OR", "NOT"], c: 0 } ] },
        { id: "5.2", title: "Multilayer perceptron & backprop", video: "",
          notes: "Hidden layers with non-linear activations make MLPs universal approximators. Backpropagation applies the chain rule layer by layer to compute gradients; weights are updated by gradient descent.",
          quiz: [
            { q: "Backpropagation is an application of the…", a: ["Chain rule", "Bayes rule", "Pigeonhole principle", "Triangle inequality"], c: 0 } ] },
        { id: "5.3", title: "SGD & training", video: "",
          notes: "Stochastic gradient descent updates on mini-batches: noisy but fast and escapes poor minima. Momentum and adaptive methods (Adam) speed it up. Monitor validation loss to avoid overfitting.",
          quiz: [{ q: "Mini-batch SGD uses…", a: ["A small subset per update", "All data per update", "No gradients", "One weight"], c: 0 }] },
        { id: "5.4", title: "Going deep: vanishing gradients & ReLU", video: "", lab: 12,
          notes: "Sigmoid units saturate, so gradients shrink layer by layer (vanishing gradient). ReLU = max(0, z) keeps gradient 1 for positive inputs, enabling deep networks.",
          quiz: [
            { q: "ReLU(−3) =", a: ["0", "−3", "3", "1"], c: 0 },
            { q: "Vanishing gradients are worst with…", a: ["Saturating sigmoids", "ReLU", "Batch norm", "Dropout"], c: 0 } ] },
        { id: "5.5", title: "Regularisation: dropout & batch norm", video: "",
          notes: "Dropout randomly zeroes units during training (scale by 1/(1−p)). Batch normalisation standardises layer inputs per mini-batch then scales/shifts. L2 regularisation penalises large weights. Tune hyperparameters on validation data.",
          quiz: [
            { q: "Dropout is used to reduce…", a: ["Overfitting", "Training data", "Bias only", "Model size on disk"], c: 0 },
            { q: "Batch norm output (before γ, β) has mean…", a: ["0", "1", "γ", "Undefined"], c: 0 } ] }
      ]
    }
  ],
  labs: {
    1: "Uninformed search (BFS, DFS)", 2: "Informed search (A*, memory-bounded A*)", 3: "Naive Bayes models",
    4: "Bayesian networks", 5: "Regression models", 6: "Decision trees and random forests", 7: "SVM models",
    8: "Ensembling techniques", 9: "Clustering algorithms", 10: "EM for Bayesian networks",
    11: "Simple NN models", 12: "Deep learning NN models"
  },
  labSlugs: { 1: "bfs-dfs", 2: "astar", 3: "naive-bayes", 4: "bayes-net", 5: "regression", 6: "trees", 7: "svm",
              8: "ensembles", 9: "clustering", 10: "em-bayes-net", 11: "simple-nn", 12: "deep-nn" }
};
