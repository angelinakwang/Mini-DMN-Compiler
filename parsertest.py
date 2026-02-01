from src.parser import ExpressionParser

parser = ExpressionParser(['danger_sign', 'chest_indrawing', 'fast_breathing'])

# Test parentheses
expr = parser.parse("(danger_sign OR chest_indrawing) AND fast_breathing")
patient = {"danger_sign": False, "chest_indrawing": True, "fast_breathing": True}
print(expr.evaluate(patient))  # Should print: True