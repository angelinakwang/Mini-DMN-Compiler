import json
from src.mermaid import MermaidGenerator

with open('data/sample_ruleset.json') as f:
    ruleset = json.load(f)

gen = MermaidGenerator(ruleset)
diagram = gen.generate()

print(diagram)

with open('output/diagram.mmd', 'w') as f:
    f.write(diagram)

print("\nSaved to output/diagram.mmd")