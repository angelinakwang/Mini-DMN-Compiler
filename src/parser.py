from ast import Pass
from turtle import left, right


class ExpressionParser:
    def __init__(self, variables) -> None:
        self.variables = variables

    def parse(self, expression):
        tokens = self._tokenize(expression)
        return VariableExpression(tokens[0])
    

    def _tokenize(self, expr):
        import re 
        pattern = r'\b(AND|OR|NOT|true|false)\b|([a-zA-Z_]\w*)|([()])'
        tokens = [m.group(0) for m in re.finditer(pattern, expr)]
        return tokens
    
    def _parse_and():
        pass

    def _parse_or():
        pass

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
        