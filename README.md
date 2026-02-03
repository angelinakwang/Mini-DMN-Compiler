# Mini DMN Compiler, Mermaid Emitter, Interpreter, and Rule Extraction

## Features

- **Expression parser**: Converts boolean logic strings into evaluable tree structures. Supports AND, OR, NOT, parentheses, and follows operator precendence.
- **DMN interpreter**: Evaluates patients against rulesets and matches first rule. Returns which rule matched, the outcome, the path taken through rules, and a justification explaining the decision. 
- **Mermaid Flowchart Generator**: Creates visual flowchart diagrams from ruleset.
- **Rule Extractor**: Parses short chunks of text into structure rules, and shows evidence for each extracted rule.
- **Error handling**: Error messages for unknown variables, missing patient data, invalid syntax, and unparseable text.

## Project Structure
```
mini-dmn-compiler/
├── src/
│   ├── parser.py          # Boolean expression parser
│   ├── interpreter.py      # Rule interpreter
│   ├── mermaid.py         # Mermaid diagram generator
│   └── extractor.py       # Text-to-rules extractor
├── tests/
│   └── test_automated.py  # Automated tests
├── data/
│   ├── sample_ruleset.json
│   ├── sample_patients.jsonl
│   └── sample_manual_excerpt.jsonl
└── output/
    ├── diagram.mmd
    ├── results.json
    └── extracted_ruleset.json
```

## Installation

No external dependencies required. Uses Python 3.7+ standard library only.

## Usage

### 1. Generate Mermaid Flowchart
```bash
python -c "
import json
from src.mermaid import MermaidGenerator

with open('data/sample_ruleset.json') as f:
    ruleset = json.load(f)

gen = MermaidGenerator(ruleset)
gen.save('output/diagram.mmd')
print('Saved to output/diagram.mmd')
"
```

### 2. Evaluate Patients Against Rules
```bash
python -c "
import json
from src.parser import ExpressionParser
from src.interpreter import Interpreter

# Load ruleset
with open('data/sample_ruleset.json') as f:
    ruleset = json.load(f)

# Load patients
patients = []
with open('data/sample_patients.jsonl') as f:
    for line in f:
        if line.strip():
            patients.append(json.loads(line))

# Evaluate
parser = ExpressionParser(ruleset['variables'])
interpreter = Interpreter(ruleset, parser)

results = []
for patient in patients:
    result = interpreter.evaluate(patient)
    results.append(result)
    print(f\"{result['patient_id']}: {result['outcome']} (matched: {result['matched_rule']})\")

# Save results
with open('output/results.json', 'w') as f:
    json.dump(results, f, indent=2)
print('\\nSaved to output/results.json')
"
```

### 3. Extract Rules from Manual Text
```bash
python -c "
import json
from src.extractor import RuleExtractor

extractor = RuleExtractor()
ruleset = extractor.extract_from_file('data/sample_manual_excerpt.jsonl')

print('Extracted Rules:')
print(json.dumps(ruleset, indent=2))

with open('output/extracted_ruleset.json', 'w') as f:
    json.dump(ruleset, f, indent=2)
print('\\nSaved to output/extracted_ruleset.json')
"
```

### 4. Run Automated Tests
```bash
python tests/test_automated.py
```

Expected output:
```
Running automated tests...

✓ Test 1 passed: danger_sign matches R1
✓ Test 2 passed: OR condition matches R2
✓ Test 3 passed: No match returns default

✓ All tests passed!
```

## DMN Semantics

- Rules evaluated top to bottom
- First match wins (stops evaluation)
- If no match, returns default
- Path tracks all rules checked

