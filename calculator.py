"""Safe expression evaluator for the calculator web app."""

from __future__ import annotations

import ast
import operator

_ALLOWED_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: lambda x: x,
    ast.USub: lambda x: -x,
}


class CalculatorError(ValueError):
    """Raised when an expression cannot be evaluated safely."""


def evaluate_expression(expression: str) -> float:
    """Evaluate a mathematical expression with a restricted AST.

    Supports +, -, *, /, %, ** and parentheses.
    """
    if expression is None:
        raise CalculatorError("Expression is required.")

    expression = expression.strip()
    if not expression:
        raise CalculatorError("Expression cannot be empty.")

    try:
        tree = ast.parse(expression, mode="eval")
        return _eval_node(tree.body)
    except ZeroDivisionError as exc:
        raise CalculatorError("Division by zero is not allowed.") from exc
    except (SyntaxError, TypeError, ValueError) as exc:
        raise CalculatorError("Invalid expression.") from exc


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise CalculatorError("Only numeric values are allowed.")

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_BINARY_OPERATORS:
            raise CalculatorError("Operator is not supported.")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_BINARY_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY_OPERATORS:
            raise CalculatorError("Unary operator is not supported.")
        return _ALLOWED_UNARY_OPERATORS[op_type](_eval_node(node.operand))

    raise CalculatorError("Unsupported expression.")
