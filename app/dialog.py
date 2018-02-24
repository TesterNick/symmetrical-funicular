import tkinter as tk


class Dialog(tk.Toplevel):

    def __init__(self, app, mode):
        for name in app.field.buttons:
            app.field.buttons[name].configure(state="disabled")
        super().__init__()
        self.app = app
        self.resizable(0, 0)
        self.title('My sap')
        self.content = tk.Frame(self, padx=10, pady=10)
        self.content.grid()
        text_label = {
            "win": "Поздравляем! Вы выиграли! Сыграем еще раз?",
            "lose": "К сожалению, вы проиграли. Хотите попробовать еще раз?",
            "restart": "Вы уверены, что хотите начать новую игру?",
            "quit": "Вы уверены, что хотите выйти из игры?",
            "info": "Текущая версия программы\n2.0.0a"
            }
        yes_command = self.exit if mode == "quit" else self.restart
        no_command = self.exit if (mode == "win" or mode == "lose") else self.resume
        self.protocol("WM_DELETE_WINDOW", no_command)
        message = tk.Label(self.content, text=text_label[mode], padx=10, pady=10)
        message.grid(row=0, column=0, columnspan=2)
        if mode == "info":
            self.ok_button = tk.Button(self.content, command=self.resume, text="OK", padx=10)
            self.ok_button.grid(row=1, column=0, columnspan=2)
            self.ok_button.focus_force()
            self.ok_button.bind("<Return>", self.resume)
        else:
            self.yes_button = tk.Button(self.content, command=yes_command, text="Да", padx=10)
            self.yes_button.grid(row=1, column=0)
            self.yes_button.bind("<Return>", yes_command)
            self.no_button = tk.Button(self.content, command=no_command, text="Нет", padx=8)
            self.no_button.grid(row=1, column=1)
            self.no_button.bind("<Return>", no_command)
            if mode == "win" or mode == "lose":
                self.yes_button.focus_force()
            else:
                self.no_button.focus_force()
            self.bind("<Right>", self.no_button_focus)
            self.bind("<Left>", self.yes_button_focus)

    def no_button_focus(self, event):
        self.no_button.focus_set()

    def yes_button_focus(self, event):
        self.yes_button.focus_set()

    def resume(self, event=None):
        self.withdraw()
        for name in self.app.field.buttons:
            if self.app.field.buttons[name].cget("text") == "X" or self.app.field.buttons[name].cget("text") == "":
                color = self.app.field.color_chooser(name)
                self.app.field.buttons[name].configure(state="normal", disabledforeground=color)

    def restart(self, event=None):
        self.withdraw()
        self.app.field = Field(self.app, self.app.root)

    def exit(self, event=None):
        self.withdraw()
        self.app.quit()
