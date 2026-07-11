# Dual-Mode Calculator Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a polished Tkinter calculator with Basic and Advanced modes, driven by a safe, tested expression engine.

**Architecture:** Pure `engine.py` for evaluation; Tkinter shell with swappable Basic/Advanced pads; shared theme.

**Tech Stack:** Python 3, Tkinter, pytest, AST-based safe evaluator

---

### Task 1: Calculator engine (TDD)

**Files:**
- Create: `calculator/__init__.py`
- Create: `calculator/engine.py`
- Create: `tests/test_engine.py`

- [ ] Write failing tests for digits, operators, evaluate, clear, backspace, errors
- [ ] Implement minimal engine to pass
- [ ] Add advanced function tests then implement
- [ ] Commit

### Task 2: Theme + app shell

**Files:**
- Create: `calculator/theme.py`
- Create: `calculator/app.py`
- Create: `calculator/basic_pad.py`
- Create: `calculator/advanced_pad.py`
- Modify: `main.py`
- Modify: `README.md`

- [ ] Theme constants
- [ ] App with display, mode switch, keyboard
- [ ] Basic and Advanced pads
- [ ] Wire main.py
- [ ] Update README
- [ ] Run tests, commit, push, PR
