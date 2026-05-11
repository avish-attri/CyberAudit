import json

from scanner.main import run_all_checks
from scanner.scorer import calculate_score


results = run_all_checks()
score = calculate_score(results)

output = {
    "score": score,
    "results": results,
}

print(json.dumps(output, indent=4))
