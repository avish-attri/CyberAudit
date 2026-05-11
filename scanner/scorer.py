weights = {
    "PASS": 1,
    "WARNING": 0.5,
    "FAIL": 0,
    "ERROR": 0,
}


def calculate_score(results):
    total = len(results)
    if total == 0:
        return 0
    earned = sum(weights.get(r["status"], 0) for r in results)
    score = (earned / total) * 100
    return round(score, 2)
