import re

class RuleExtractor:
    def __init__(self):
        self.extracted_variables = set()
    
    def extract_from_file(self, filepath):
        """Extract rules from JSONL file"""
        import json
        
        chunks = []
        with open(filepath) as f:
            for line in f:
                if line.strip():
                    chunks.append(json.loads(line))
        
        return self.extract_from_chunks(chunks)
    
    def extract_from_chunks(self, chunks):
        """Convert text chunks to ruleset"""
        rules = []
        default = None
        
        for i, chunk in enumerate(chunks):
            text = chunk['text']
            chunk_id = chunk['chunk_id']
            
            if 'otherwise' in text.lower():
                default = self._extract_default(text, chunk_id)
            else:
                rule = self._extract_rule(text, chunk_id, i + 1)
                if rule:
                    rules.append(rule)
            
        if not default:
            raise ValueError("No default outcome found in manual text")
    
        if not rules:
            raise ValueError("No rules found in manual text")
        
        return {
            'name': 'extracted_ruleset',
            'variables': sorted(list(self.extracted_variables)),
            'rules': rules,
            'default': default
        }
    
    def _extract_default(self, text, chunk_id):
        """Extract: 'Otherwise classify as OUTCOME'"""
        match = re.search(r'classify as (\w+)', text, re.IGNORECASE)
        return match.group(1)
    
    def _extract_rule(self, text, chunk_id, rule_num):
        """Extract: 'If CONDITION, classify as OUTCOME'"""
        if not text.lower().startswith('if '):
            return None
        
        outcome_match = re.search(r'classify as (\w+)', text, re.IGNORECASE)
        if not outcome_match:
            raise ValueError(f"Cannot extract outcome from chunk {chunk_id}: '{text}'")
        outcome = outcome_match.group(1)
        
        condition_match = re.search(r'if (.*?) is true,? classify', text, re.IGNORECASE)
        if not condition_match:
            condition_match = re.search(r'if (.*?),? classify', text, re.IGNORECASE)

        if not condition_match:
            raise ValueError(f"Cannot extract condition from chunk {chunk_id}: '{text}'")
        
        condition = condition_match.group(1).strip()

        self._extract_variables(condition)
        
        return {
            'id': f'R{rule_num}',
            'when': condition,
            'then': outcome,
            'evidence': chunk_id
        }
    
    def _extract_variables(self, condition):
        """Find variable names in condition"""
        var_pattern = r'\b([a-z_]\w*)\b'
        for match in re.finditer(var_pattern, condition):
            var = match.group(1)
            if var.upper() not in ['OR', 'AND', 'NOT', 'TRUE', 'FALSE', 'IS']:
                self.extracted_variables.add(var)