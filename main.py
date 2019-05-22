from tkinter import (Tk, Label, Button, Text)


class PyCalculator:
    """docstring for PyCalculator."""

    def __init__(self, master):
        self.master = master
        master.title("Python GUI Calculator")

        # screen widget
        self.screen = Text(master, state='disabled', width=40,
                           height=10, background="yellow", foreground="blue")

        # screen widget positioning
        self.screen.grid(row=0, column=0, columnspan=4, padx=20, pady=20)
        self.screen.configure(state='normal')

        # initialize screen value
        self.equation = ''


root = Tk()
py_calculator = PyCalculator(root)
root.mainloop()
