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
                'expression': parsed_expr
            })
    
    def evaluate(self, patient):
        """Evaluate patient against rules until first match"""
        path = []
        
        for rule in self.parsed_rules:
            path.append(rule['id'])
            
            if rule['expression'].evaluate(patient):
                return {
                    'patient_id': patient['id'],
                    'outcome': rule['then'],
                    'matched_rule': rule['id'],
                    'path': path
                }
        
        return {
            'patient_id': patient['id'],
            'outcome': self.ruleset['default'],
            'matched_rule': None,
            'path': path
        }