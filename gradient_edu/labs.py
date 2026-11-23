"""CS3491 course catalogue: units, course outcomes and the 12 practical exercises."""

COURSE = {
    "code": "CS3491",
    "title": "Artificial Intelligence and Machine Learning",
    "ltpc": "3 0 2 4",
    "attainment_threshold": 60,   # % score for a student to attain a CO
    "class_target": 60,           # % of students who must attain a CO
}

COS = {
    "CO1": "Use appropriate search algorithms for problem solving",
    "CO2": "Apply reasoning under uncertainty",
    "CO3": "Build supervised learning models",
    "CO4": "Build ensembling and unsupervised models",
    "CO5": "Build deep learning neural network models",
}

UNITS = {
    1: ("Problem Solving", "CO1"),
    2: ("Probabilistic Reasoning", "CO2"),
    3: ("Supervised Learning", "CO3"),
    4: ("Ensemble Techniques and Unsupervised Learning", "CO4"),
    5: ("Neural Networks", "CO5"),
}

# lab number -> metadata
LABS = {
    1: dict(title="Uninformed search (BFS, DFS)", unit=1, co="CO1", slug="bfs-dfs"),
    2: dict(title="Informed search (A*, memory-bounded A*)", unit=1, co="CO1", slug="astar"),
    3: dict(title="Naive Bayes models", unit=2, co="CO2", slug="naive-bayes"),
    4: dict(title="Bayesian networks", unit=2, co="CO2", slug="bayes-net"),
    5: dict(title="Regression models", unit=3, co="CO3", slug="regression"),
    6: dict(title="Decision trees and random forests", unit=3, co="CO3", slug="trees"),
    7: dict(title="SVM models", unit=3, co="CO3", slug="svm"),
    8: dict(title="Ensembling techniques", unit=4, co="CO4", slug="ensembles"),
    9: dict(title="Clustering algorithms", unit=4, co="CO4", slug="clustering"),
    10: dict(title="EM for Bayesian networks", unit=2, co="CO2", slug="em-bayes-net"),
    11: dict(title="Simple NN models", unit=5, co="CO5", slug="simple-nn"),
    12: dict(title="Deep learning NN models", unit=5, co="CO5", slug="deep-nn"),
}

# Rubric (out of 100). "auto" components are scored by the grader on every push.
RUBRIC = [
    ("hidden", "Hidden tests (correctness)", 50, "auto"),
    ("quality", "Public tests + code quality", 10, "auto"),
    ("report", "Observations in REPORT.md", 15, "auto-provisional"),
    ("viva", "Viva voce", 15, "teacher"),
    ("ontime", "On-time submission", 10, "auto"),
]

GRADE_BANDS = [(91, "O"), (81, "A+"), (71, "A"), (61, "B+"), (56, "B"), (50, "C"), (0, "RA")]


def grade_letter(score):
    for cut, letter in GRADE_BANDS:
        if score >= cut:
            return letter
    return "RA"


def lab_id(n):
    return f"lab{int(n):02d}"
