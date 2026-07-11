"""Launch the Py Calculator desktop app."""

from tkinter import Tk

from calculator.app import CalculatorApp


def main() -> None:
    root = Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
