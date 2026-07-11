"""Advanced / scientific calculator button pad."""

from __future__ import annotations

from tkinter import Button, Frame
from typing import Callable

from calculator.theme import BUTTON_STYLES, COLORS, FONTS


# Rows of (label, key, style[, columnspan]). Default colspan is 1.
_ADVANCED_LAYOUT: list[list[tuple]] = [
    [("sin", "sin", "function"), ("cos", "cos", "function"), ("tan", "tan", "function"), ("π", "pi", "function"), ("e", "e", "function")],
    [("ln", "ln", "function"), ("log", "log", "function"), ("√", "sqrt", "function"), ("x²", "square", "function"), ("1/x", "reciprocal", "function")],
    [("(", "(", "operator"), (")", ")", "operator"), ("^", "^", "operator"), ("|x|", "abs", "function"), ("⌫", "⌫", "clear")],
    [("C", "C", "clear"), ("%", "%", "operator"), ("÷", "/", "operator"), ("×", "*", "operator"), ("−", "-", "operator")],
    [("7", "7", "number"), ("8", "8", "number"), ("9", "9", "number"), ("+", "+", "operator"), ("±", "±", "function")],
    [("4", "4", "number"), ("5", "5", "number"), ("6", "6", "number"), (".", ".", "number"), ("=", "=", "equals")],
    [("1", "1", "number"), ("2", "2", "number"), ("3", "3", "number"), ("0", "0", "number", 2)],
]


class AdvancedPad(Frame):
    """Scientific keypad with trig, logs, powers, and constants."""

    def __init__(self, master, on_press: Callable[[str], None], **kwargs):
        super().__init__(master, bg=COLORS["panel"], **kwargs)
        self._on_press = on_press
        self._build()

    def _build(self) -> None:
        for r, row in enumerate(_ADVANCED_LAYOUT):
            self.grid_rowconfigure(r, weight=1, uniform="abtn")
            c = 0
            for cell in row:
                label, key, style_name = cell[0], cell[1], cell[2]
                colspan = cell[3] if len(cell) > 3 else 1
                self.grid_columnconfigure(c, weight=1, uniform="abtn")
                if colspan > 1:
                    for extra in range(1, colspan):
                        self.grid_columnconfigure(c + extra, weight=1, uniform="abtn")
                style = BUTTON_STYLES[style_name]
                font = FONTS["button_sm"] if style_name == "function" else FONTS["button"]
                btn = Button(
                    self,
                    text=label,
                    font=font,
                    relief="flat",
                    borderwidth=0,
                    cursor="hand2",
                    command=lambda k=key: self._on_press(k),
                    **style,
                )
                btn.grid(row=r, column=c, columnspan=colspan, sticky="nsew", padx=2, pady=2)
                c += colspan
