import tkinter as tk
from tkinter import ttk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("GUIテーマ色変更")
        self.pack()

        # テーマ色を変更する関数
        def change_theme():
            theme_color = color_var.get()
            style = ttk.Style()
            style.theme_use('default')
            style.configure('.', background=theme_color)

        # ボタンとラジオボタンを作成して配置
        color_var = tk.StringVar()
        color_var.set('#ffffff')  # 初期値は白色
        color_radio1 = ttk.Radiobutton(self, text="白色", variable=color_var, value='#ffffff')
        color_radio1.pack(padx=10, pady=5, anchor=tk.W)
        color_radio2 = ttk.Radiobutton(self, text="グレー", variable=color_var, value='#f0f0f0')
        color_radio2.pack(padx=10, pady=5, anchor=tk.W)
        color_radio3 = ttk.Radiobutton(self, text="ブルー", variable=color_var, value='#cfe2f3')
        color_radio3.pack(padx=10, pady=5, anchor=tk.W)
        theme_button = ttk.Button(self, text="テーマ色を変更する", command=change_theme)
        theme_button.pack(pady=10)

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
