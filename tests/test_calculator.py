import pytest

from calculator import CalculatorError, evaluate_expression


def test_valid_expressions():
    assert evaluate_expression("1 + 2") == 3
    assert evaluate_expression("(12 + 8) * 4 / 2") == 40
    assert evaluate_expression("2 ** 3") == 8
    assert evaluate_expression("10 % 3") == 1


def test_invalid_expression():
    with pytest.raises(CalculatorError):
        evaluate_expression("__import__('os').system('echo unsafe')")


def test_division_by_zero():
    with pytest.raises(CalculatorError, match="Division by zero"):
        evaluate_expression("10 / 0")


def test_empty_expression():
    with pytest.raises(CalculatorError, match="empty"):
        evaluate_expression("   ")
