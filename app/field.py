import os
import random
import tkinter as tk
from .cell import Cell


class Field(tk.Frame):

    def __init__(self, master, settings):
        super().__init__()
        self.parent = master
        self.place_of_death = None
        self.cells = {}
        self.columns = settings.available_columns[:settings.columns]
        self.rows = settings.rows
        self.number_of_bombs = tk.IntVar()
        self.number_of_bombs.set(settings.number_of_bombs)
        self.bomb_counter = tk.Label(self, textvariable=self.number_of_bombs, font="courier 15 bold", fg="red")
        self.bomb_counter.grid(column=0, columnspan=len(self.columns), row=0)
        self.folder = os.path.dirname(__file__)
        self.cell_images = {
            "closed": tk.PhotoImage(file=(os.path.join(self.folder, "../img/closed.png"))),
            "last": tk.PhotoImage(file=(os.path.join(self.folder, "../img/boom.png"))),
            "bomb": tk.PhotoImage(file=(os.path.join(self.folder, "../img/bomb.png"))),
            "not_bomb": tk.PhotoImage(file=(os.path.join(self.folder, "../img/wrong.png"))),
            "marked": tk.PhotoImage(file=(os.path.join(self.folder, "../img/marked.png"))),
            "0": tk.PhotoImage(file=(os.path.join(self.folder, "../img/empty.png"))),
            "1": tk.PhotoImage(file=(os.path.join(self.folder, "../img/1.png"))),
            "2": tk.PhotoImage(file=(os.path.join(self.folder, "../img/2.png"))),
            "3": tk.PhotoImage(file=(os.path.join(self.folder, "../img/3.png"))),
            "4": tk.PhotoImage(file=(os.path.join(self.folder, "../img/4.png"))),
            "5": tk.PhotoImage(file=(os.path.join(self.folder, "../img/5.png"))),
            "6": tk.PhotoImage(file=(os.path.join(self.folder, "../img/6.png"))),
            "7": tk.PhotoImage(file=(os.path.join(self.folder, "../img/7.png"))),
            "8": tk.PhotoImage(file=(os.path.join(self.folder, "../img/8.png")))
        }
        self.grid()
        self.create_field()

    # Field creation and configuration
    def create_field(self):
        for i in range(self.rows):
            for j in self.columns:
                self.cells[j+str(i)] = Cell(self, i, j, self.cell_images["closed"], self.cell_images["marked"])
        counter = 0
        # Placing bombs
        while counter < self.number_of_bombs.get():
            cell = self.get_random_cell()
            if not cell.is_bomb():
                cell.add_bomb(self.cell_images["bomb"], self.cell_images["last"])
                counter += 1
        # Filling non-bomb cells with numbers of nearby bombs
        for name in self.cells:
            cell = self.cells[name]
            if not cell.is_bomb():
                counter = 0
                neighbours = self.get_neighbours(cell.column+cell.row)
                for n in neighbours:
                    if self.cells[n].is_bomb():
                        counter += 1
                cell.nearby_bombs = counter
                cell.set_opened_image(self.cell_images["{}".format(counter)])
                cell.set_bomb_image(self.cell_images["not_bomb"])
        # Placing cells on the field
        for name in self.cells:
            cell = self.cells[name]
            cell.configure(command=cell.open, takefocus=0, width=24, height=24)
            cell.activate()
            cell.grid(column=self.columns.index(name[0]), row=(int(name[1:]) + 1))

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

    def get_random_cell(self):
        rnd = random.choice(list(self.cells.keys()))
        cell = self.cells[rnd]
        return cell

    # Checking if all the bombs marked correctly
    def check(self):
        for name in self.cells:
            cell = self.cells[name]
            if cell.is_bomb() and not cell.is_marked():
                if self.place_of_death is None:
                    cell.blow_up()
                self.parent.lose()
                return
        self.parent.win()

    def show_the_bombs(self):
        for name in self.cells:
            self.cells[name].show(name == self.place_of_death)
