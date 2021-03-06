import tkinter as tk


class Cell(tk.Button):

    def __init__(self, master, row, column, images):
        super().__init__(master=master)
        self.field = master
        self.app = master.parent
        self.row = str(row)
        self.column = str(column)
        self.nearby_bombs = None
        self.bomb = False
        self.state = "closed"
        self.images = images
        self._closed_image = self.images.closed
        self.configure(image=self._closed_image)
        self._last_image = self.images.boom
        self._bomb_image = self.images.bomb
        self._not_bomb_image = self.images.wrong
        self._marked_image = self.images.marked
        self._opened_image = None

    # Image control
    def _get_opened_image(self):
        return self._opened_image

    def _set_opened_image(self, opened_image):
        del self._opened_image
        self._opened_image = opened_image
    opened_image = property(_get_opened_image, _set_opened_image)

    def set_closed_image(self, counter):
        self.nearby_bombs = counter if counter != 0 else None
        self.opened_image = self.images.opened["{}".format(counter)]

    # Getters
    def is_bomb(self):
        return self.bomb

    def is_closed(self):
        return self.state == "closed"

    def is_disabled(self):
        return self.state == "disabled"

    def is_marked(self):
        return self.state == "marked"

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

    def close(self):
        self.state = "closed"
        self.configure(image=self._closed_image, state="normal")

    def open(self):
        if not self.is_marked():
            self.configure(image=self._opened_image, relief="sunken")
            self.unbind("<B1>")
            self.state = "disabled"
            if self.is_bomb():
                self.blow_up()
                self.app.lose()
            elif self.nearby_bombs is None:
                self.open_zeros()

    def mark(self, event=None):
        if not self.is_disabled():
            counter = self.field.number_of_bombs
            if self.is_closed():
                self.state = "marked"
                self.configure(image=self._marked_image)
                counter.set(counter.get()-1)
            elif self.is_marked():
                self.close()
                counter.set(counter.get()+1)
            if self.field.number_of_bombs.get() == 0:
                self.field.check()

    def show(self, place_of_death):
        if self.is_bomb() and not self.is_marked() and not place_of_death:
            self.configure(image=self._bomb_image)
        elif not self.is_bomb() and self.is_marked():
            self.configure(image=self._not_bomb_image)

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
                    # When player was wrong and previous cell blew up,
                    # cells are deleted and following opening is not needed
                    if not cell:
                        return
                    if cell.is_closed():
                        cell.open()
        elif self.is_closed():
            self.configure(relief="raised")
        for n in neighbours:
            cell = self.field.cells[n]
            if cell.is_closed() or cell.is_marked():
                cell.configure(relief="raised")

    def blow_up(self):
        self.configure(image=self._last_image)
        self.field.place_of_death = self.column + self.row

    # Function recursively checks if the cell has no bombs around and
    # opens them
    def open_zeros(self):
        neighbours = self.field.get_neighbours(self.column + self.row)
        for n in neighbours:
            cell = self.field.cells[n]
            if cell.is_closed():
                cell.open()
                if cell.nearby_bombs is None:
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
