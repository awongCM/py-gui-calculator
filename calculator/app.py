"""Main calculator application shell."""

from __future__ import annotations

from tkinter import Button, Frame, Label, StringVar, Tk

from calculator.advanced_pad import AdvancedPad
from calculator.basic_pad import BasicPad
from calculator.engine import CalculatorEngine
from calculator.theme import COLORS, FONTS


_UNARY_KEYS = frozenset(
    {"sin", "cos", "tan", "log", "ln", "sqrt", "square", "reciprocal", "abs"}
)


def _is_compound_expression(expr: str) -> bool:
    """True when expr has operators beyond a single signed number."""
    if any(ch in expr for ch in "+*/^()"):
        return True
    return "-" in expr[1:]


class CalculatorApp:
    """Dual-mode calculator window (Basic / Advanced)."""

    def __init__(self, master: Tk) -> None:
        self.master = master
        self.engine = CalculatorEngine()
        self.mode = StringVar(value="basic")
        self._pad: Frame | None = None

        self._configure_window()
        self._build_chrome()
        self._show_pad("basic")
        self._bind_keys()
        self._refresh_display()

    def _configure_window(self) -> None:
        self.master.title("Py Calculator")
        self.master.configure(bg=COLORS["bg"])
        self.master.minsize(320, 480)
        self.master.geometry("360x560")
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(3, weight=1)

    def _build_chrome(self) -> None:
        header = Frame(self.master, bg=COLORS["bg"])
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        header.grid_columnconfigure(1, weight=1)

        Label(
            header,
            text="Py Calculator",
            font=FONTS["brand"],
            bg=COLORS["bg"],
            fg=COLORS["accent"],
        ).grid(row=0, column=0, sticky="w")

        mode_bar = Frame(header, bg=COLORS["bg"])
        mode_bar.grid(row=0, column=1, sticky="e")
        self._basic_btn = self._mode_button(mode_bar, "Basic", "basic")
        self._advanced_btn = self._mode_button(mode_bar, "Advanced", "advanced")
        self._basic_btn.pack(side="left", padx=(0, 4))
        self._advanced_btn.pack(side="left")

        display_frame = Frame(self.master, bg=COLORS["display_bg"], padx=16, pady=12)
        display_frame.grid(row=1, column=0, sticky="ew", padx=16, pady=(4, 8))
        display_frame.grid_columnconfigure(0, weight=1)

        self._expr_var = StringVar(value="")
        self._result_var = StringVar(value="0")

        Label(
            display_frame,
            textvariable=self._expr_var,
            font=FONTS["expression"],
            bg=COLORS["display_bg"],
            fg=COLORS["display_muted"],
            anchor="e",
        ).grid(row=0, column=0, sticky="ew")

        Label(
            display_frame,
            textvariable=self._result_var,
            font=FONTS["display"],
            bg=COLORS["display_bg"],
            fg=COLORS["display_fg"],
            anchor="e",
        ).grid(row=1, column=0, sticky="ew")

        Label(
            self.master,
            text="Trig functions use degrees  ·  Esc clears  ·  Enter equals",
            font=("DejaVu Sans", 8),
            bg=COLORS["bg"],
            fg=COLORS["display_muted"],
        ).grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 4))

        self._pad_host = Frame(self.master, bg=COLORS["panel"])
        self._pad_host.grid(row=3, column=0, sticky="nsew", padx=12, pady=(4, 12))
        self._pad_host.grid_columnconfigure(0, weight=1)
        self._pad_host.grid_rowconfigure(0, weight=1)

        self._update_mode_buttons()

    def _mode_button(self, parent: Frame, label: str, mode: str) -> Button:
        return Button(
            parent,
            text=label,
            font=FONTS["mode"],
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            padx=10,
            pady=4,
            command=lambda: self._set_mode(mode),
        )

    def _update_mode_buttons(self) -> None:
        current = self.mode.get()
        for btn, mode in ((self._basic_btn, "basic"), (self._advanced_btn, "advanced")):
            if mode == current:
                btn.configure(
                    bg=COLORS["mode_active_bg"],
                    fg=COLORS["mode_active_fg"],
                    activebackground=COLORS["mode_active_bg"],
                    activeforeground=COLORS["mode_active_fg"],
                )
            else:
                btn.configure(
                    bg=COLORS["mode_inactive_bg"],
                    fg=COLORS["mode_inactive_fg"],
                    activebackground=COLORS["number_active"],
                    activeforeground=COLORS["mode_inactive_fg"],
                )

    def _set_mode(self, mode: str) -> None:
        if mode == self.mode.get():
            return
        self.mode.set(mode)
        self._update_mode_buttons()
        self._show_pad(mode)
        if mode == "advanced":
            self.master.geometry("420x640")
            self.master.minsize(380, 560)
        else:
            self.master.geometry("360x560")
            self.master.minsize(320, 480)

    def _show_pad(self, mode: str) -> None:
        if self._pad is not None:
            self._pad.destroy()
            self._pad = None
        if mode == "advanced":
            self._pad = AdvancedPad(self._pad_host, on_press=self._on_press)
        else:
            self._pad = BasicPad(self._pad_host, on_press=self._on_press)
        self._pad.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)

    def _on_press(self, key: str) -> None:
        before = self.engine.display()
        expr_before = self.engine.expression
        self.engine.press(key)

        if key == "=" and expr_before:
            self._expr_var.set(expr_before)
        elif key == "C":
            self._expr_var.set("")
        elif key in _UNARY_KEYS:
            label = {"square": "sqr", "reciprocal": "1/"}.get(key, key)
            self._expr_var.set(f"{label}({before})")
        elif self.engine.in_error:
            self._expr_var.set("")
        else:
            expr = self.engine.expression
            if _is_compound_expression(expr):
                self._expr_var.set(expr)

        self._refresh_display()

    def _refresh_display(self) -> None:
        self._result_var.set(self.engine.display())
        if self.engine.in_error:
            self._expr_var.set("")

    def _bind_keys(self) -> None:
        self.master.bind("<Return>", lambda e: self._on_press("="))
        self.master.bind("<KP_Enter>", lambda e: self._on_press("="))
        self.master.bind("<BackSpace>", lambda e: self._on_press("⌫"))
        self.master.bind("<Escape>", lambda e: self._on_press("C"))
        self.master.bind("<Key>", self._on_key)

    def _on_key(self, event) -> str | None:
        # Avoid double-handling keys already bound above.
        if event.keysym in {"Return", "KP_Enter", "BackSpace", "Escape"}:
            return None
        simple = {
            "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
            "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
            ".": ".", "+": "+", "-": "-", "*": "*", "/": "/",
            "^": "^", "%": "%", "(": "(", ")": ")", "=": "=",
        }
        if event.char in simple:
            self._on_press(simple[event.char])
            return "break"
        return None
