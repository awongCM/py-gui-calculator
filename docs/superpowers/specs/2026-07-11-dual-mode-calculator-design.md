# Dual-Mode GUI Calculator Design

**Date:** 2026-07-11  
**Status:** Approved for implementation (cloud agent — proceed from clear product request)

## Goal

Complete the unfinished Tkinter calculator into a polished desktop app with two modes: **Basic** and **Advanced**.

## Architecture

```
main.py                 # Entry point — creates Tk root, launches app
calculator/
  __init__.py
  engine.py             # Pure expression evaluation (no UI) — unit tested
  app.py                # Shell window: mode switch, display, shared chrome
  basic_pad.py          # Basic button grid
  advanced_pad.py       # Scientific button grid
  theme.py              # Colors, fonts, button styles
tests/
  test_engine.py        # Engine unit tests
```

- **Engine** owns all math and expression logic. UI only sends key presses / evaluate / clear.
- **App** owns the display, history line, mode toggle, and keyboard bindings.
- **Pads** are swappable frames; switching modes rebuilds the button area without resetting the display value.

## Modes

### Basic
- Digits `0–9`, decimal `.`
- Operators `+ − × ÷`
- `=` evaluate, `C` clear all, `⌫` backspace, `±` negate
- Percent `%` (divide current operand by 100)

### Advanced
Everything in Basic, plus:
- Parentheses `( )`
- Power `xʸ` / `^`, square `x²`, reciprocal `1/x`, sqrt `√`
- Trig: `sin`, `cos`, `tan` (degrees)
- Logs: `log` (base 10), `ln` (natural)
- Constants: `π`, `e`
- Absolute value `|x|`

## Expression model

- Display shows the current expression (or result after `=`).
- Evaluation uses a safe AST-based evaluator (no `eval` / `exec` on raw strings).
- Division by zero and domain errors (e.g. `sqrt(-1)`, `ln(0)`) show `Error` and reset cleanly on the next digit.
- After `=`, typing a digit starts a new expression; typing an operator continues from the result.

## UI / UX

- Clean dark charcoal palette with teal accents (not purple/glow defaults).
- Distinct button types: number, operator, function, equals, clear.
- Mode segmented control at the top: Basic | Advanced.
- Keyboard support for digits, operators, Enter (`=`), Backspace, Escape (`C`).
- Window resizes modestly; buttons use grid weight for a balanced layout.

## Testing

- Unit tests cover the engine only (expression parsing, ops, errors, chaining).
- GUI smoke: import/`PyCalculator` construction under a headless-friendly path when possible; engine coverage is the reliability gate.

## Out of scope

- Graphing, unit conversion, history panel persistence, themes beyond one polished scheme, packaging/installers.
