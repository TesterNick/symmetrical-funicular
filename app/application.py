import tkinter as tk

from .dialog import Dialog
from .field import Field


class Application(tk.Frame):

    def __init__(self):
        self.root = tk.Tk()
        super().__init__()
        self.root.resizable(0, 0)
        self.root.config(menu=self.create_menu(self.root))
        self.root.title('My sap')
        self.root.protocol("WM_DELETE_WINDOW", self.ensure_exit)
        self.grid()
        self.field = Field(self, self.root)

    # Main menu
    def create_menu(self, root):
        m = tk.Menu(root)
        game = tk.Menu(m, tearoff=0)
        m.add_cascade(label="Игра", menu=game)
        game.add_command(label="Новая", command=self.ensure_restart)
        game.add_command(label="Выход", command=self.ensure_exit)
        about = tk.Menu(m, tearoff=0)
        m.add_cascade(label="О программе", menu=about)
        about.add_command(label="Версия", command=self.show_info)
        return m

    def ensure_restart(self):
        Dialog(self, "restart")

    def ensure_exit(self):
        Dialog(self, "quit")

    def lose(self):
        Dialog(self, "lose")

    def win(self):
        Dialog(self, "win")

    def show_info(self):
        Dialog(self, "info")
