"""Tests for expression display helpers."""

from calculator.expression import is_compound_expression


def test_compound_expression_ignores_scientific_notation():
    assert is_compound_expression("1e-10") is False
    assert is_compound_expression("2+3") is True
    assert is_compound_expression("-42") is False
