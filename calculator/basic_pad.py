"""Basic calculator button pad."""

from __future__ import annotations

from tkinter import Button, Frame
from typing import Callable

from calculator.theme import BUTTON_STYLES, COLORS, FONTS


# (label, key, style, columnspan)
_BASIC_LAYOUT: list[list[tuple[str, str, str, int]]] = [
    [("C", "C", "clear", 1), ("⌫", "⌫", "clear", 1), ("%", "%", "operator", 1), ("÷", "/", "operator", 1)],
    [("7", "7", "number", 1), ("8", "8", "number", 1), ("9", "9", "number", 1), ("×", "*", "operator", 1)],
    [("4", "4", "number", 1), ("5", "5", "number", 1), ("6", "6", "number", 1), ("−", "-", "operator", 1)],
    [("1", "1", "number", 1), ("2", "2", "number", 1), ("3", "3", "number", 1), ("+", "+", "operator", 1)],
    [("±", "±", "function", 1), ("0", "0", "number", 1), (".", ".", "number", 1), ("=", "=", "equals", 1)],
]


class BasicPad(Frame):
    """Standard four-function keypad."""

    def __init__(self, master, on_press: Callable[[str], None], **kwargs):
        super().__init__(master, bg=COLORS["panel"], **kwargs)
        self._on_press = on_press
        self._build()

    def _build(self) -> None:
        for r, row in enumerate(_BASIC_LAYOUT):
            self.grid_rowconfigure(r, weight=1, uniform="btn")
            c = 0
            for label, key, style_name, colspan in row:
                self.grid_columnconfigure(c, weight=1, uniform="btn")
                style = BUTTON_STYLES[style_name]
                btn = Button(
                    self,
                    text=label,
                    font=FONTS["button"],
                    relief="flat",
                    borderwidth=0,
                    cursor="hand2",
                    command=lambda k=key: self._on_press(k),
                    **style,
                )
                btn.grid(row=r, column=c, columnspan=colspan, sticky="nsew", padx=3, pady=3)
                c += colspan
