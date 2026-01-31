class MermaidGenerator:
    def __init__(self, ruleset):
        self.ruleset = ruleset
    
    def generate(self):
        lines = ["flowchart TD"]
        lines.append("    Start -> R1")
        
        for i, rule in enumerate(self.ruleset['rules']):
            rule_id = rule['id']
            condition = rule['when']
            outcome = rule['then']
            
            
            # Yes path
            lines.append(f"    {rule_id} ->|Yes| {outcome}")
            
            # No path
            if i < len(self.ruleset['rules']) - 1:
                next_rule = self.ruleset['rules'][i + 1]['id']
                lines.append(f"    {rule_id} ->|No| {next_rule}")
            else:
                lines.append(f"    {rule_id} ->|No| {self.ruleset['default']}")
        
        return "\n".join(lines)