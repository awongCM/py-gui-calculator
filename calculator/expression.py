"""Expression display helpers (no UI dependencies)."""


def is_compound_expression(expr: str) -> bool:
    """True when expr has operators beyond a single signed number."""
    if any(ch in expr for ch in "+*/^()"):
        return True
    lower = expr.lower()
    if "e-" in lower or "e+" in lower:
        return False
    return "-" in expr[1:]
