import json

class Interpreter:
    def __init__(self, ruleset, parser):
        self.ruleset = ruleset
        self.parser = parser

        self.parsed_rules = []
        for rule in ruleset['rules']:
            parsed_expr = parser.parse(rule['when'])
            self.parsed_rules.append({
                'id': rule['id'],
                'when': rule['when'],
                'then': rule['then'],
                'expression': parsed_expr,
                'evidence': rule.get('evidence') 
            })
    
    def evaluate(self, patient):
        """Evaluate patient against rules until first match"""
        path = []

        for var in self.ruleset['variables']:
            if var not in patient:
                raise ValueError(f"Patient '{patient.get('id', 'unknown')}' is missing required variable: '{var}'")
        
        for rule in self.parsed_rules:
            path.append(rule['id'])
            
            if rule['expression'].evaluate(patient):
                return {
                    'patient_id': patient['id'],
                    'outcome': rule['then'],
                    'matched_rule': rule['id'],
                    'path': path,
                    'justification': f"Rule {rule['id']} matched: {rule['when']} → {rule['then']}",  
                    'evidence': rule.get('evidence') 
                }
        
        return {
            'patient_id': patient['id'],
            'outcome': self.ruleset['default'],
            'matched_rule': None,
            'path': path,
            'justification': f"No rules matched, using default: {self.ruleset['default']}", 
            'evidence': None
        }