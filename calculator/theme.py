"""Visual theme for the calculator UI."""

from __future__ import annotations

# Charcoal + teal palette — deliberate, not purple/glow defaults.
COLORS = {
    "bg": "#1a1d23",
    "panel": "#22262e",
    "display_bg": "#12151a",
    "display_fg": "#e8eaed",
    "display_muted": "#8b939e",
    "number_bg": "#2c313a",
    "number_fg": "#e8eaed",
    "number_active": "#3a404c",
    "op_bg": "#2a4a4e",
    "op_fg": "#7fd4c7",
    "op_active": "#356065",
    "fn_bg": "#252a33",
    "fn_fg": "#a8b0bc",
    "fn_active": "#323844",
    "eq_bg": "#2dd4bf",
    "eq_fg": "#0f1419",
    "eq_active": "#5eead4",
    "clear_bg": "#4a3038",
    "clear_fg": "#f0a8b0",
    "clear_active": "#5c3c44",
    "mode_active_bg": "#2dd4bf",
    "mode_active_fg": "#0f1419",
    "mode_inactive_bg": "#2c313a",
    "mode_inactive_fg": "#8b939e",
    "accent": "#2dd4bf",
}

FONTS = {
    "brand": ("DejaVu Sans", 11, "bold"),
    "display": ("DejaVu Sans Mono", 28, "bold"),
    "expression": ("DejaVu Sans Mono", 11),
    "button": ("DejaVu Sans", 12),
    "button_sm": ("DejaVu Sans", 10),
    "mode": ("DejaVu Sans", 10, "bold"),
}

BUTTON_STYLES = {
    "number": {
        "bg": COLORS["number_bg"],
        "fg": COLORS["number_fg"],
        "activebackground": COLORS["number_active"],
        "activeforeground": COLORS["number_fg"],
    },
    "operator": {
        "bg": COLORS["op_bg"],
        "fg": COLORS["op_fg"],
        "activebackground": COLORS["op_active"],
        "activeforeground": COLORS["op_fg"],
    },
    "function": {
        "bg": COLORS["fn_bg"],
        "fg": COLORS["fn_fg"],
        "activebackground": COLORS["fn_active"],
        "activeforeground": COLORS["fn_fg"],
    },
    "equals": {
        "bg": COLORS["eq_bg"],
        "fg": COLORS["eq_fg"],
        "activebackground": COLORS["eq_active"],
        "activeforeground": COLORS["eq_fg"],
    },
    "clear": {
        "bg": COLORS["clear_bg"],
        "fg": COLORS["clear_fg"],
        "activebackground": COLORS["clear_active"],
        "activeforeground": COLORS["clear_fg"],
    },
}
