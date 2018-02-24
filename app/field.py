import math
import random
import tkinter as tk

from .cell import Cell


class Field(tk.Frame):

    def __init__(self, app, master):
        super().__init__()
        self.app = app
        self.master = master
        self.cells = {}
        self.buttons = {}
        self.columns = "abcdefghij"
        self.rows = 10
        self.number_of_bombs = 20
        self.bomb_counter = tk.Label(master, text=self.number_of_bombs, font="courier 15 bold", fg="red")
        self.bomb_counter.grid(column=0, columnspan=len(self.columns), row=0)
        self.create_field(master)

    # Field creation and configuration
    def create_field(self, root):
        for i in range(self.rows):
            for j in self.columns:
                self.cells[j+str(i)] = Cell(self.app, i, j, " ")
        counter = 0
        # Placing bombs
        while counter < self.number_of_bombs:
            i = int(math.floor(random.random() * self.rows))
            j = self.columns[int(math.floor(random.random() * len(self.columns)))]
            if self.cells[j+str(i)].value != "!":
                self.cells[j+str(i)].value = "!"
                counter += 1
        # Filling non-bomb cells with numbers of nearby bombs
        for i in range(self.rows):
            for j in self.columns:
                cell = self.cells[j+str(i)]
                if cell.value != "!":
                    counter = 0
                    neighbours = self.get_neighbours(j+str(i))
                    for n in neighbours:
                        if self.cells[n].value == "!":
                            counter += 1
                    if counter == 0:
                        cell.value = " "
                    else:
                        cell.value = str(counter)
        # Creating buttons for cells
        for i in range(self.rows):
            for j in self.columns:
                name = j+str(i)
                color = self.color_chooser(name)
                self.buttons[name] = tk.Button(root, command=self.cells[name].open_cell, disabledforeground=color,
                                               width=1, height=1, font="arial 12 bold", takefocus=0)
                self.buttons[name].bind("<ButtonRelease-3>", self.cells[name].mark_cell)
                self.buttons[name].bind("<Button-1>"+"<Button-3>", self.cells[name].two_buttons)
                self.buttons[name].bind("<ButtonRelease-1>"+"<ButtonRelease-3>", self.cells[name].automated_opening)
                self.buttons[name].bind("<Leave>", self.cells[name].mouse_leave)
                self.buttons[name].bind("<B1-Motion>"+"<B3-Motion>", self.cells[name].two_buttons)
        for cell in self.buttons:
            self.buttons[cell].grid(column=self.columns.index(cell[0]), row=(int(cell[1:]) + 1), ipadx=6)

    # Function return list of cell's names that are neighbours of the current cell
    def get_neighbours(self, coordinates):
        neighbours = []
        column = self.columns.index(coordinates[0])
        row = int(coordinates[1:])
        for i in range(row-1, row+2):
            for j in range(column-1, column+2):
                if (0 <= i < self.rows) and (0 <= j < len(self.columns)):
                    if not (i == row and j == column):
                        j = self.columns[j]
                        neighbours.append(j+str(i))
        return neighbours

    # Checking if all the bombs marked correctly
    def check(self):
        for name in self.buttons:
            if self.cells[name].value == "!" and self.buttons[name].cget("text") == "":
                self.cells[name].open_cell()
                return
        self.app.win()

    # Choosing color of the digits
    def color_chooser(self, name):
        color = {
            " ": "grey",
            "1": "blue",
            "2": "green",
            "3": "red",
            "4": "dark blue",
            "5": "dark red",
            "6": "cyan",
            "7": "DarkMagenta",
            "8": "magenta",
            "!": "black"
            }[str(self.cells[name].value)]
        return color
