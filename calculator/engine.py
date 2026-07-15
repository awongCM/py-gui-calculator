"""Safe expression-based calculator engine (no raw eval)."""

from __future__ import annotations

import ast
import math
import operator
import re
from typing import Any, Callable


_BINARY_OPS: dict[type, Callable[[Any, Any], Any]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

_UNARY_OPS: dict[type, Callable[[Any], Any]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

_FUNCTIONS: dict[str, Callable[[float], float]] = {
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)),
    "log": math.log10,
    "ln": math.log,
    "sqrt": math.sqrt,
    "abs": abs,
}

_CONSTANTS: dict[str, float] = {
    "pi": math.pi,
    "e": math.e,
}

_OPERATORS = frozenset({"+", "-", "*", "/", "^"})
_DIGITS = frozenset("0123456789")
_APPLY_FUNCS = frozenset(
    {"sin", "cos", "tan", "log", "ln", "sqrt", "square", "reciprocal", "abs"}
)


def _safe_eval(expression: str) -> float:
    """Evaluate a calculator expression via AST — never uses eval()."""
    source = expression.replace("^", "**")
    # Allow bare constants and function names as identifiers.
    tree = ast.parse(source, mode="eval")
    return float(_eval_node(tree.body))


def _eval_node(node: ast.AST) -> Any:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in _CONSTANTS:
            return _CONSTANTS[node.id]
        raise ValueError(f"Unknown name: {node.id}")
    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _BINARY_OPS:
            raise ValueError("Unsupported operator")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        if op_type is ast.Div and right == 0:
            raise ZeroDivisionError
        if op_type is ast.Pow and left < 0 and isinstance(right, float) and not right.is_integer():
            raise ValueError("Invalid power")
        return _BINARY_OPS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _UNARY_OPS:
            raise ValueError("Unsupported unary operator")
        return _UNARY_OPS[op_type](_eval_node(node.operand))
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _FUNCTIONS:
            raise ValueError("Unsupported function")
        if len(node.args) != 1 or node.keywords:
            raise ValueError("Function expects one argument")
        value = _eval_node(node.args[0])
        return _FUNCTIONS[node.func.id](value)
    raise ValueError(f"Unsupported expression: {type(node).__name__}")


def _format_number(value: float) -> str:
    if math.isnan(value) or math.isinf(value):
        raise ValueError("Invalid result")
    if abs(value - round(value)) < 1e-12 and abs(value) < 1e15:
        return str(int(round(value)))
    text = f"{value:.12g}"
    if "e" in text.lower():
        # Avoid scientific notation so % and ± can edit the display string.
        if value == 0:
            return "0"
        abs_v = abs(value)
        if abs_v < 1:
            decimals = max(6, int(-math.floor(math.log10(abs_v))) + 2)
            text = f"{value:.{decimals}f}".rstrip("0").rstrip(".")
        else:
            text = f"{value:.15f}".rstrip("0").rstrip(".")
        if text in ("-0", "-0."):
            return "0"
    return text


def _last_operand_bounds(expr: str) -> tuple[int, int] | None:
    """Return [start, end) slice bounds for the trailing numeric literal."""
    if not expr:
        return None
    end = len(expr)
    i = end - 1
    saw_dot = False
    while i >= 0:
        ch = expr[i]
        if ch.isdigit():
            i -= 1
            continue
        if ch == "." and not saw_dot:
            saw_dot = True
            i -= 1
            continue
        break
    start = i + 1
    if start >= end:
        return None
    if start > 0 and expr[start - 1] == "-":
        prev = expr[start - 2] if start >= 2 else ""
        if start == 1 or prev in "+-*/^(":
            start -= 1
    return (start, end)


class CalculatorEngine:
    """Handles key presses and evaluates arithmetic expressions safely."""

    def __init__(self) -> None:
        self._expression = ""
        self._just_evaluated = False
        self._error = False

    def display(self) -> str:
        if self._error:
            return "Error"
        return self._expression if self._expression else "0"

    @property
    def expression(self) -> str:
        """Current expression text (empty when idle or in error)."""
        if self._error:
            return ""
        return self._expression

    @property
    def in_error(self) -> bool:
        return self._error

    def press(self, key: str) -> str:
        if self._error:
            self._reset()
            if key == "C":
                return self.display()
            if key == "⌫":
                return self.display()
            if key in _APPLY_FUNCS | {"pi", "e", "±", "%"}:
                return self.display()

        if key == "C":
            self._reset()
            return self.display()

        if key == "⌫":
            self._backspace()
            return self.display()

        if key == "=":
            self._evaluate()
            return self.display()

        if key in _APPLY_FUNCS:
            self._apply_function(key)
            return self.display()

        if key in ("pi", "e"):
            self._input_constant(key)
            return self.display()

        if key == "±":
            self._negate()
            return self.display()

        if key == "%":
            self._percent()
            return self.display()

        if key in _DIGITS:
            self._input_digit(key)
            return self.display()

        if key == ".":
            self._input_decimal()
            return self.display()

        if key in _OPERATORS:
            self._input_operator(key)
            return self.display()

        if key == "(":
            self._input_lparen()
            return self.display()

        if key == ")":
            self._input_rparen()
            return self.display()

        return self.display()

    def _reset(self) -> None:
        self._expression = ""
        self._just_evaluated = False
        self._error = False

    def _set_error(self) -> None:
        self._expression = ""
        self._just_evaluated = False
        self._error = True

    def _backspace(self) -> None:
        if self._just_evaluated:
            self._reset()
            return
        if not self._expression:
            return
        self._expression = self._expression[:-1]

    def _evaluate(self) -> None:
        if not self._expression:
            return
        try:
            result = _safe_eval(self._expression)
            self._expression = _format_number(result)
            self._just_evaluated = True
            self._error = False
        except Exception:
            self._set_error()

    def _start_fresh_if_needed_for_value(self) -> None:
        if self._just_evaluated:
            self._expression = ""
            self._just_evaluated = False

    def _input_digit(self, digit: str) -> None:
        self._start_fresh_if_needed_for_value()
        if self._expression == "0":
            self._expression = digit
            return
        # Replace a lone zero after an operator / paren.
        if re.search(r"(?:^|[\+\-\*/\^\(])0$", self._expression):
            self._expression = self._expression[:-1] + digit
            return
        self._expression += digit

    def _input_decimal(self) -> None:
        self._start_fresh_if_needed_for_value()
        number = self._current_number()
        if "." in number:
            return
        if not number or number in {"+", "-"}:
            # Starting a fractional number, possibly after operator.
            if not self._expression or self._expression[-1] in "+-*/^(":
                self._expression += "0."
            elif self._expression[-1] == "-":
                self._expression += "0."
            else:
                self._expression += "0."
            return
        self._expression += "."

    def _input_operator(self, op: str) -> None:
        if self._error:
            self._reset()
        self._just_evaluated = False
        if not self._expression:
            if op == "-":
                self._expression = "-"
            return
        last = self._expression[-1]
        if last in _OPERATORS:
            # Allow "*-" style? Keep simple: replace trailing operator, except
            # allow unary minus after another operator via separate handling.
            if op == "-" and last in "*/^":
                self._expression += "-"
                return
            self._expression = self._expression[:-1] + op
            return
        if last == "(":
            if op == "-":
                self._expression += "-"
            return
        self._expression += op

    def _input_lparen(self) -> None:
        self._start_fresh_if_needed_for_value()
        if self._expression:
            last = self._expression[-1]
            if last.isdigit() or last in {".", ")"}:
                self._expression += "*("
                return
        self._expression += "("

    def _input_rparen(self) -> None:
        if not self._expression:
            return
        opens = self._expression.count("(")
        closes = self._expression.count(")")
        if opens <= closes:
            return
        if self._expression[-1] in _OPERATORS | {"("}:
            return
        self._expression += ")"
        self._just_evaluated = False

    def _input_constant(self, name: str) -> None:
        self._start_fresh_if_needed_for_value()
        value = _format_number(_CONSTANTS[name])
        if self._expression and self._expression[-1] not in _OPERATORS | {"("}:
            self._expression += "*" + value
        else:
            self._expression += value
        self._just_evaluated = True

    def _current_number(self) -> str:
        bounds = _last_operand_bounds(self._expression)
        if not bounds:
            return ""
        return self._expression[bounds[0] : bounds[1]]

    def _replace_current_number(self, new_value: str) -> None:
        bounds = _last_operand_bounds(self._expression)
        if not bounds:
            self._expression = new_value
            return
        start, end = bounds
        self._expression = self._expression[:start] + new_value + self._expression[end:]

    def _negate(self) -> None:
        if self._just_evaluated and self._expression:
            try:
                value = float(self._expression)
                self._expression = _format_number(-value)
                self._just_evaluated = True
                return
            except ValueError:
                pass

        number = self._current_number()
        if number and number not in {"+", "-", ".", "+.", "-."}:
            try:
                value = float(number)
                self._replace_current_number(_format_number(-value))
                return
            except ValueError:
                pass

        # Negate whole expression by wrapping.
        if self._expression:
            if self._expression.startswith("-(") and self._expression.endswith(")"):
                # Unwrap if already negated as -(...)
                inner = self._expression[2:-1]
                # Only unwrap when parens are balanced for the wrap we added.
                self._expression = inner
            else:
                self._expression = f"-({self._expression})"

    def _percent(self) -> None:
        number = self._current_number()
        if not number or number in {"+", "-", ".", "+.", "-."}:
            return
        try:
            value = float(number) / 100.0
            self._replace_current_number(_format_number(value))
            self._just_evaluated = False
        except ValueError:
            self._set_error()

    def _apply_function(self, name: str) -> None:
        expr = self._expression if self._expression else "0"
        try:
            if name == "square":
                result = _safe_eval(f"({expr})**2")
            elif name == "reciprocal":
                result = _safe_eval(f"1/({expr})")
            else:
                result = _safe_eval(f"{name}({expr})")
            self._expression = _format_number(result)
            self._just_evaluated = True
            self._error = False
        except Exception:
            self._set_error()
