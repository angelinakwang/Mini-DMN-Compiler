# In test_parser.py
from src.parser import AndExpression, ExpressionParser, VariableExpression, OrExpression

# Test OR
left = VariableExpression("danger_sign")
right = VariableExpression("chest_indrawing")
or_expr = OrExpression(left, right)
and_expr = AndExpression(left, right)

patient = {"danger_sign": False, "chest_indrawing": True}
result = and_expr.evaluate(patient)
print("and result:", result)  # Should print: True