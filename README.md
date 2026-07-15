# Py Calculator

A polished Python GUI calculator with **Basic** and **Advanced** modes, built with Tkinter.

## Features

### Basic mode
- Digits, decimal, and four operations (`+ − × ÷`)
- Clear, backspace, percent, and sign toggle (`±`)
- Keyboard support (digits, operators, Enter, Backspace, Esc)

### Advanced mode
Everything in Basic, plus:
- Parentheses and power (`^`)
- `x²`, `√`, `1/x`, absolute value
- Trig in **degrees**: `sin`, `cos`, `tan`
- Logs: `log` (base 10), `ln`
- Constants: `π`, `e`

## Requirements

- Python 3.9+
- Tkinter (`python3-tk` on Debian/Ubuntu)

## Run

```bash
python3 main.py
```

## Tests

```bash
python3 -m pytest -q
```

## Project layout

```
main.py                 # Entry point
calculator/
  engine.py             # Safe AST expression engine (no eval)
  app.py                # Window chrome + mode switching
  basic_pad.py          # Basic keypad
  advanced_pad.py       # Scientific keypad
  theme.py              # Colors and fonts
tests/
  test_engine.py
```

## License

MIT
