import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("テーマ変更ボタン")
        self.geometry("300x100")

        # テーマを変更する関数
        def change_theme():
            current_theme = self.tk.call("ttk::style", "theme", "use")
            if current_theme == "clam":
                self.tk.call("ttk::style", "theme", "use", "winnative")
            else:
                self.tk.call("ttk::style", "theme", "use", "clam")

        # テーマ変更ボタン
        theme_button = ttk.Button(self, text="テーマ変更", command=change_theme)
        theme_button.pack(pady=20)

if __name__ == '__main__':
    app = App()
    app.mainloop()