# Agent instructions

## Cursor Cloud specific instructions

This repository is a Python 3 Tkinter desktop calculator. Cloud agents should be able to develop and verify changes without a display server.

### Environment

- Python 3.9+ with Tkinter (`python3-tk` on Debian/Ubuntu)
- Test dependencies are installed via `requirements.txt` during cloud agent startup

### Verify changes

Run the unit test suite from the repository root:

```bash
.venv/bin/python -m pytest -q
```

If the virtual environment is not present yet, create it and install dependencies first:

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

All tests should pass before opening a pull request.

### Run the GUI locally

The calculator is a desktop app and requires a display. In cloud environments without a GUI, use the test suite for verification instead of launching the window:

```bash
python3 main.py
```

When developing calculator behavior, prefer extending or updating tests in `tests/` so changes can be verified headlessly.

### Project layout

- `main.py` — application entry point
- `calculator/` — GUI and expression engine
- `tests/` — pytest unit tests for the calculator engine
