import tkinter as tk


class Cell(tk.Button):

    def __init__(self, master, row, column, background, mark):
        super().__init__(master=master)
        self.field = master
        self.app = master.parent
        self.row = str(row)
        self.column = str(column)
        self.nearby_bombs = None
        self.bomb = False
        self.state = "closed"
        self.closed_image = background
        self.configure(image=self.get_closed_image())
        self.last_image = property(self.get_last_image, self.set_last_image)
        self.bomb_image = property(self.get_bomb_image, self.set_bomb_image)
        self.marked_image = mark
        self.opened_image = property(self.get_opened_image, self.set_opened_image)

    # Getters
    def is_bomb(self):
        return self.bomb

    def is_closed(self):
        return self.state == "closed"

    def is_disabled(self):
        return self.state == "disabled"

    def is_marked(self):
        return self.state == "marked"

    def get_opened_image(self):
        return self.opened_image

    def get_closed_image(self):
        return self.closed_image

    def get_last_image(self):
        return self.last_image

    def get_bomb_image(self):
        return self.bomb_image

    # Setters
    def set_opened_image(self, image):
        self.opened_image = image

    def set_last_image(self, image):
        self.last_image = image

    def set_bomb_image(self, image):
        self.bomb_image = image

    # State changers
    def activate(self):
        self.configure(state="normal")
        self.bind("<ButtonRelease-3>", self.mark)
        self.bind("<Button-2>", self.two_buttons)
        self.bind("<ButtonRelease-2>", self.automated_opening)
        self.bind("<B2-Leave>", self.mouse_leave)
        self.bind("<B2-Motion>", self.two_buttons)

    def deactivate(self):
        self.configure(state="disabled")
        self.unbind("<ButtonRelease-3>")
        self.unbind("<Button-2>")
        self.unbind("<ButtonRelease-2>")
        self.unbind("<B2-Leave>")
        self.unbind("<B2-Motion>")

    def add_bomb(self, bomb_image, last_image):
        self.bomb = True
        self.set_bomb_image(bomb_image)
        self.set_opened_image(bomb_image)
        self.set_last_image(last_image)

    def close(self):
        self.state = "closed"
        self.configure(image=self.get_closed_image(), state="normal")

    def open(self):
        if not self.is_marked():
            self.configure(image=self.get_opened_image(), relief="sunken")
            self.unbind("<B1>")
            self.state = "disabled"
            if self.is_bomb():
                self.blow_up()
                self.app.lose()
            elif self.nearby_bombs == 0:
                self.open_zeros()

    def mark(self, event=None):
        if not self.is_disabled():
            counter = self.field.number_of_bombs
            if self.is_closed():
                self.state = "marked"
                self.configure(image=self.marked_image)
                counter.set(counter.get()-1)
            elif self.is_marked():
                self.close()
                counter.set(counter.get()+1)
            if self.field.number_of_bombs.get() == 0:
                self.field.check()

    def show(self, place_of_death):
        if ((self.is_bomb() and not self.is_marked() and not place_of_death) or
                (not self.is_bomb() and self.is_marked())):
            self.configure(image=self.get_bomb_image())

    # Other actions
    def automated_opening(self, event=None):
        neighbours = self.field.get_neighbours(self.column + self.row)
        if not (self.is_closed() or self.is_bomb()):
            amount_of_opened_nearby_bombs = 0
            for n in neighbours:
                if self.field.cells[n].is_marked():
                    amount_of_opened_nearby_bombs += 1
            if amount_of_opened_nearby_bombs == self.nearby_bombs:
                for n in neighbours:
                    cell = self.field.cells[n]
                    if cell.is_closed():
                        cell.open()
        elif self.is_closed():
            self.configure(relief="raised")
        for n in neighbours:
            cell = self.field.cells[n]
            if cell.is_closed() or cell.is_marked():
                cell.configure(relief="raised")

    def blow_up(self):
        self.configure(image=self.get_last_image())
        self.field.place_of_death = self.column + self.row

    # Function recursively checks if the cell has no bombs around and opens them
    def open_zeros(self):
        neighbours = self.field.get_neighbours(self.column + self.row)
        for n in neighbours:
            cell = self.field.cells[n]
            if cell.is_closed():
                cell.open()
                if cell.nearby_bombs == 0:
                    cell.open_zeros()

    def two_buttons(self, event=None):
        if not self.is_marked():
            neighbours = self.field.get_neighbours(self.column + self.row)
            self.configure(relief="sunken")
            for n in neighbours:
                button = self.field.cells[n]
                if not (button.is_marked() or button.is_disabled()):
                    button.configure(relief="sunken")

    def mouse_leave(self, event=None):
        if self.is_closed():
            self.configure(relief="raised")
        neighbours = self.field.get_neighbours(self.column + self.row)
        for n in neighbours:
            button = self.field.cells[n]
            if button.is_closed():
                button.configure(relief="raised")
