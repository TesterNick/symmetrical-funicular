class Cell:

    def __init__(self, app, row, column, value):
        self.app = app
        self.row = str(row)
        self.column = str(column)
        self.value = str(value)

    def automated_opening(self, event):
        neighbours = self.app.field.get_neighbours(self.column+self.row)
        button_text = self.app.field.buttons[self.column+self.row].cget("text")
        if button_text != "" and button_text != "X":
            amount_of_opened_nearby_bombs = 0
            for n in neighbours:
                if self.app.field.buttons[n].cget("text") == "X":
                    amount_of_opened_nearby_bombs += 1
            if str(amount_of_opened_nearby_bombs) == self.value:
                for n in neighbours:
                    self.app.field.cells[n].open_cell()
        for n in neighbours:
            if self.app.field.buttons[n].cget("text") == "" or self.app.field.buttons[n].cget("text") == "X":
                self.app.field.buttons[n].configure(relief="raised")

    def open_cell(self):
        if self.app.field.buttons[self.column+self.row].cget("text") != "X":
            value = self.value
            if value == "!":
                self.app.field.buttons[self.column+self.row].configure(bg="red")
                self.app.lose()
            self.app.field.buttons[self.column+self.row].configure(text=value, state="disabled", relief="sunken")
            if value == " ":
                self.open_zeros()

    # Function recursively checks if the cell has no bombs around and opens them
    def open_zeros(self):
        neighbours = self.app.field.get_neighbours(self.column+self.row)
        for n in neighbours:
            if self.app.field.buttons[n].cget("text") == "":
                self.app.field.cells[n].open_cell()
                if self.app.field.cells[n].value == " ":
                    self.app.field.cells[n].open_zeros()

    def mark_cell(self, event):
        if self.app.field.buttons[self.column+self.row].cget("state") != "disabled":
            if self.app.field.buttons[self.column+self.row].cget("text") == "":
                self.app.field.buttons[self.column+self.row].configure(text="X", disabledforeground="black")
                self.app.field.number_of_bombs -= 1
            else:
                color = self.app.field.color_chooser(self.column+self.row)
                self.app.field.buttons[self.column+self.row].configure(text="", disabledforeground=color)
                self.app.field.number_of_bombs += 1
            self.app.field.bomb_counter.configure(text=self.app.field.number_of_bombs)
            if self.app.field.number_of_bombs == 0:
                self.app.field.check()

    def two_buttons(self, event):
        if self.app.field.buttons[self.column+self.row].cget("text") != "X":
            neighbours = self.app.field.get_neighbours(self.column+self.row)
            for n in neighbours:
                if self.app.field.buttons[n].cget("text") != "X":
                    self.app.field.buttons[n].configure(relief="sunken")

    def mouse_leave(self, event):
        neighbours = self.app.field.get_neighbours(self.column+self.row)
        for n in neighbours:
            if self.app.field.buttons[n].cget("text") == "":
                self.app.field.buttons[n].configure(relief="raised")
