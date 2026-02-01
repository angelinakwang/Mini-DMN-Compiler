import json
from src.parser import ExpressionParser
from src.interpreter import Interpreter

with open('data/sample_ruleset.json') as f:
    ruleset = json.load(f)

patients = []
with open('data/sample_patients.jsonl') as f:
    for line in f:
        if line.strip():
            patients.append(json.loads(line))

parser = ExpressionParser(ruleset['variables'])
interpreter = Interpreter(ruleset, parser)

results = []
for patient in patients:
    result = interpreter.evaluate(patient)
    results.append(result)
    print(f"{result['patient_id']}: {result['outcome']} (matched: {result['matched_rule']})")

with open('output/results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nSaved to output/results.json")