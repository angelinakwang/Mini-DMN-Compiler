class ExpressionParser:
    def __init__(self, variables) -> None:
        self.variables = set(variables)

    def parse(self, expression):
        """Convert string to tree, following operator precedence """
        tokens = self._tokenize(expression)
        expr, pos = self._parse_or(tokens, 0)
        
        return expr
    

    def _tokenize(self, expr):
        import re 
        pattern = r'\b(AND|OR|NOT|true|false)\b|([a-zA-Z_]\w*)|([()])'
        tokens = [m.group(0) for m in re.finditer(pattern, expr)]
        
        return tokens
    
    def _parse_or(self, tokens, pos):
        left, pos = self._parse_and(tokens, pos)
    
        while pos < len(tokens) and tokens[pos] == 'OR':
            pos += 1
            right, pos = self._parse_and(tokens, pos)
            left = OrExpression(left, right)
        
        return left, pos
    
    def _parse_and(self, tokens, pos):
        left, pos = self._parse_not(tokens, pos)
    
        while pos < len(tokens) and tokens[pos] == 'AND':
            pos += 1
            right, pos = self._parse_not(tokens, pos)
            left = AndExpression(left, right)
        
        return left, pos
    
    def _parse_not(self, tokens, pos):
        if pos < len(tokens) and tokens[pos] == 'NOT':
            pos += 1
            expr, pos = self._parse_not(tokens, pos)
            
            return NotExpression(expr), pos
    
        return self._parse_primary(tokens, pos)

    def _parse_primary(self, tokens, pos):
        token = tokens[pos]

        if token == '(':
            pos += 1  
            expr, pos = self._parse_or(tokens, pos)  
            return expr, pos

        if token == 'true':
            return LiteralExpression(True), pos + 1

        if token == 'false':
            return LiteralExpression(False), pos + 1
    
        if token not in self.variables:
            raise ValueError(f"Unknown variable: '{token}' is not in the ruleset variables")

        return VariableExpression(token), pos + 1
    

class VariableExpression:
    def __init__(self, name):
        self.name = name

    def evaluate(self, context):
        return bool(context[self.name])

class OrExpression:
    def __init__(self, left, right): 
        self.left = left
        self.right = right

    def evaluate(self, context):
        return self.left.evaluate(context) or self.right.evaluate(context)
    
class AndExpression:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def evaluate(self, context):
        return self.left.evaluate(context) and self.right.evaluate(context)

class NotExpression:
    def __init__(self, operand):
        self.operand = operand
    
    def evaluate(self, context):
        return not self.operand.evaluate(context)

class LiteralExpression:
    def __init__(self, value):
        self.value = value 
    
    def evaluate(self, context):
        return self.value  