"""Unit tests for the calculator expression engine."""

import math
import pytest

from calculator.engine import CalculatorEngine


@pytest.fixture
def calc():
    return CalculatorEngine()


class TestBasicInput:
    def test_starts_at_zero(self, calc):
        assert calc.display() == "0"

    def test_digit_entry(self, calc):
        calc.press("1")
        calc.press("2")
        calc.press("3")
        assert calc.display() == "123"

    def test_leading_zero_replaced(self, calc):
        calc.press("0")
        calc.press("5")
        assert calc.display() == "5"

    def test_decimal(self, calc):
        calc.press("3")
        calc.press(".")
        calc.press("1")
        calc.press("4")
        assert calc.display() == "3.14"

    def test_only_one_decimal_per_number(self, calc):
        calc.press("1")
        calc.press(".")
        calc.press(".")
        calc.press("5")
        assert calc.display() == "1.5"


class TestBasicArithmetic:
    def test_addition(self, calc):
        for key in "2+3=":
            calc.press(key)
        assert calc.display() == "5"

    def test_subtraction(self, calc):
        for key in "9-4=":
            calc.press(key)
        assert calc.display() == "5"

    def test_multiplication(self, calc):
        for key in "6*7=":
            calc.press(key)
        assert calc.display() == "42"

    def test_division(self, calc):
        for key in "8/2=":
            calc.press(key)
        assert calc.display() == "4"

    def test_operator_precedence(self, calc):
        for key in "2+3*4=":
            calc.press(key)
        assert calc.display() == "14"

    def test_chained_after_equals(self, calc):
        for key in "2+3=":
            calc.press(key)
        calc.press("+")
        calc.press("4")
        calc.press("=")
        assert calc.display() == "9"

    def test_new_number_after_equals(self, calc):
        for key in "2+3=":
            calc.press(key)
        calc.press("7")
        assert calc.display() == "7"


class TestClearAndEdit:
    def test_clear(self, calc):
        for key in "12+3":
            calc.press(key)
        calc.press("C")
        assert calc.display() == "0"

    def test_backspace(self, calc):
        calc.press("1")
        calc.press("2")
        calc.press("3")
        calc.press("⌫")
        assert calc.display() == "12"

    def test_backspace_to_empty_shows_zero(self, calc):
        calc.press("5")
        calc.press("⌫")
        assert calc.display() == "0"

    def test_negate(self, calc):
        calc.press("5")
        calc.press("±")
        assert calc.display() == "-5"
        calc.press("±")
        assert calc.display() == "5"

    def test_percent(self, calc):
        calc.press("5")
        calc.press("0")
        calc.press("%")
        assert calc.display() == "0.5"


class TestErrors:
    def test_division_by_zero(self, calc):
        for key in "1/0=":
            calc.press(key)
        assert calc.display() == "Error"

    def test_digit_after_error_starts_fresh(self, calc):
        for key in "1/0=":
            calc.press(key)
        calc.press("4")
        assert calc.display() == "4"

    def test_sqrt_negative(self, calc):
        calc.press("±")  # need a number first
        calc.press("C")
        calc.press("4")
        calc.press("±")
        calc.press("sqrt")
        assert calc.display() == "Error"


class TestAdvanced:
    def test_parentheses(self, calc):
        for key in list("(1+2)*3="):
            calc.press(key)
        assert calc.display() == "9"

    def test_power(self, calc):
        for key in list("2^8="):
            calc.press(key)
        assert calc.display() == "256"

    def test_square(self, calc):
        calc.press("5")
        calc.press("square")
        assert calc.display() == "25"

    def test_sqrt(self, calc):
        calc.press("9")
        calc.press("0")
        calc.press("0")
        calc.press("sqrt")
        assert calc.display() == "30"

    def test_reciprocal(self, calc):
        calc.press("4")
        calc.press("reciprocal")
        assert calc.display() == "0.25"

    def test_abs(self, calc):
        calc.press("5")
        calc.press("±")
        calc.press("abs")
        assert calc.display() == "5"

    def test_sin_degrees(self, calc):
        calc.press("9")
        calc.press("0")
        calc.press("sin")
        assert float(calc.display()) == pytest.approx(1.0)

    def test_cos_degrees(self, calc):
        calc.press("0")
        calc.press("cos")
        assert float(calc.display()) == pytest.approx(1.0)

    def test_tan_degrees(self, calc):
        calc.press("4")
        calc.press("5")
        calc.press("tan")
        assert float(calc.display()) == pytest.approx(1.0)

    def test_log10(self, calc):
        calc.press("1")
        calc.press("0")
        calc.press("0")
        calc.press("log")
        assert float(calc.display()) == pytest.approx(2.0)

    def test_ln(self, calc):
        calc.press("e")
        calc.press("ln")
        assert float(calc.display()) == pytest.approx(1.0)

    def test_pi_constant(self, calc):
        calc.press("pi")
        assert float(calc.display()) == pytest.approx(math.pi)

    def test_e_constant(self, calc):
        calc.press("e")
        assert float(calc.display()) == pytest.approx(math.e)

    def test_function_on_expression(self, calc):
        for key in list("2+2"):
            calc.press(key)
        calc.press("square")
        assert calc.display() == "16"


class TestRegression:
    def test_paren_after_digit(self, calc):
        for key in list("2*(3+1)="):
            calc.press(key)
        assert calc.display() == "8"

    def test_paren_after_operator(self, calc):
        for key in list("2+(3)="):
            calc.press(key)
        assert calc.display() == "5"

    def test_implicit_multiply_paren(self, calc):
        for key in list("2(3+1)="):
            calc.press(key)
        assert calc.display() == "8"

    def test_percent_in_expression(self, calc):
        for key in list("2+50%="):
            calc.press(key)
        assert calc.display() == "2.5"

    def test_negate_after_subtraction(self, calc):
        for key in list("1-2"):
            calc.press(key)
        calc.press("±")
        assert calc.expression == "1--2"
        calc.press("=")
        assert calc.display() == "3"

    def test_constant_then_digit_starts_fresh(self, calc):
        calc.press("e")
        calc.press("2")
        assert calc.display() == "2"

    def test_constant_then_operator_chains(self, calc):
        calc.press("e")
        calc.press("*")
        calc.press("2")
        calc.press("=")
        assert float(calc.display()) == pytest.approx(2 * math.e)

    def test_function_after_error_is_ignored(self, calc):
        for key in list("1/0="):
            calc.press(key)
        calc.press("sin")
        assert calc.display() == "0"

    def test_digit_after_error_still_works(self, calc):
        for key in list("1/0="):
            calc.press(key)
        calc.press("7")
        assert calc.display() == "7"
