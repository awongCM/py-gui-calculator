from tkinter import Tk, Label, Button


class PyCalculator:
    """docstring for PyCalculator."""

    def __init__(self, master):
        self.master = master
        master.title("Python GUI Calculator")


root = Tk()
py_calculator = PyCalculator(root)
root.mainloop()
