import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('matplotlib graph')

        #-----------------------------------------------

        # matplotlib配置用フレーム
        frame = tk.Frame(self.master)
        
        # matplotlibの描画領域の作成
        fig = Figure()
        # 座標軸の作成
        self.ax = fig.add_subplot(1, 1, 1)
        # matplotlibの描画領域とウィジェット(Frame)の関連付け
        self.fig_canvas = FigureCanvasTkAgg(fig, frame)
        # matplotlibのツールバーを作成
        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, frame)
        # matplotlibのグラフをフレームに配置
        self.fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # フレームをウィンドウに配置
        frame.pack()

        # ボタンの作成
        button = tk.Button(self.master, text = "Draw Graph", command = self.button_click)
        # 配置
        button.pack(side = tk.BOTTOM)

        #-----------------------------------------------

    def button_click(self):
        # 表示するデータの作成
        x = np.arange(-np.pi, np.pi, 0.1)
        y = np.sin(x)
        # グラフの描画
        self.ax.plot(x, y)
        # 表示
        self.fig_canvas.draw()

root = tk.Tk()
app = Application(master=root)
app.mainloop()