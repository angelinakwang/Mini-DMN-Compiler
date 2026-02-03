import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.parser import ExpressionParser
from src.interpreter import Interpreter


def test_danger_sign_matches_r1():
    """Test patient with danger_sign matches R1"""
    ruleset = {
        'name': 'test',
        'variables': ['danger_sign', 'chest_indrawing', 'stridor', 'fast_breathing'],
        'rules': [
            {'id': 'R1', 'when': 'danger_sign', 'then': 'SEVERE'},
            {'id': 'R2', 'when': 'chest_indrawing OR stridor', 'then': 'SEVERE'},
            {'id': 'R3', 'when': 'fast_breathing', 'then': 'PNEUMONIA'}
        ],
        'default': 'COUGH_NO_PNEUMONIA'
    }
    
    parser = ExpressionParser(ruleset['variables'])
    interpreter = Interpreter(ruleset, parser)
    
    patient = {'id': 'P1', 'danger_sign': True, 'chest_indrawing': False, 'stridor': False, 'fast_breathing': False}
    result = interpreter.evaluate(patient)
    
    assert result['outcome'] == 'SEVERE'
    assert result['matched_rule'] == 'R1'
    print("✓ Test 1 passed")


def test_or_condition_matches_r2():
    """Test OR condition"""
    ruleset = {
        'name': 'test',
        'variables': ['danger_sign', 'chest_indrawing', 'stridor', 'fast_breathing'],
        'rules': [
            {'id': 'R1', 'when': 'danger_sign', 'then': 'SEVERE'},
            {'id': 'R2', 'when': 'chest_indrawing OR stridor', 'then': 'SEVERE'},
            {'id': 'R3', 'when': 'fast_breathing', 'then': 'PNEUMONIA'}
        ],
        'default': 'COUGH_NO_PNEUMONIA'
    }
    
    parser = ExpressionParser(ruleset['variables'])
    interpreter = Interpreter(ruleset, parser)
    
    patient = {'id': 'P2', 'danger_sign': False, 'chest_indrawing': True, 'stridor': False, 'fast_breathing': False}
    result = interpreter.evaluate(patient)
    
    assert result['outcome'] == 'SEVERE'
    assert result['matched_rule'] == 'R2'
    print("✓ Test 2 passed")


def test_default_outcome():
    """Test default when no rules match"""
    ruleset = {
        'name': 'test',
        'variables': ['danger_sign', 'chest_indrawing', 'stridor', 'fast_breathing'],
        'rules': [
            {'id': 'R1', 'when': 'danger_sign', 'then': 'SEVERE'},
            {'id': 'R2', 'when': 'chest_indrawing OR stridor', 'then': 'SEVERE'},
            {'id': 'R3', 'when': 'fast_breathing', 'then': 'PNEUMONIA'}
        ],
        'default': 'COUGH_NO_PNEUMONIA'
    }
    
    parser = ExpressionParser(ruleset['variables'])
    interpreter = Interpreter(ruleset, parser)
    
    patient = {'id': 'P3', 'danger_sign': False, 'chest_indrawing': False, 'stridor': False, 'fast_breathing': False}
    result = interpreter.evaluate(patient)
    
    assert result['outcome'] == 'COUGH_NO_PNEUMONIA'
    assert result['matched_rule'] is None
    print("✓ Test 3 passed")


if __name__ == '__main__':
    print("Running automated tests...\n")
    try:
        test_danger_sign_matches_r1()
        test_or_condition_matches_r2()
        test_default_outcome()
        print("\n✓ All tests passed!")
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)