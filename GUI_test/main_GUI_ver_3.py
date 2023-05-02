# -*- coding: utf-8 -*-
from concurrent.futures import thread
import tkinter as tk
from tkinter import filedialog 
from tkinter import messagebox 
import re
import numpy as np
import random as rand
import datetime
import subprocess

import matplotlib.pyplot as plt #tkinter上でグラフを描画するため
from matplotlib.pyplot import box
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk #tkinter上でグラフを描画するため
import os
from os.path import expanduser
import csv
from time import time
import sys
from time import sleep
import time
#import RPi.GPIO as GPIO #ラズパイのピン指定用(windowsじゃ動かない)
#import smbus
import threading
import subprocess
import json


#status_file = open('../main/setting/status.txt')


#グローバル変数の宣言
is_stop = True # 一時停止の実行フラグ
counter_list = [] # 時計回り、反時計回りにどれだけ回転したかを配列で記憶する
is_restart_Count = 0 # 一時停止した際のカウント数を取得
Count = 0

#グラフ作成のための配列
amp_list = []
volt_list = []
watt_list = []
temp_list = []
count_list = []
for_count = 0 # for文の回数をカウント

return_opened_1 = False
return_opened_2 = False


#csvの保存先
dir_op_path = '/home/pi/kakuda/csv'#''の中に保存先のディレクトリを指定

#ピンのセットアップ
direction = 20
step = 21


BUTTON_OPTIONS = {
    "fg": "#fff0f5",
    "bg": "#0b0b33",
    "activebackground": "#77ffd4",
    "activeforeground": "#ff1493",
    "cursor": "man",
    "highlightbackground": "#483d8b",
}



# アプリケーション（GUI）クラス
class Application(tk.Frame):
    DEBUG_LOG = True
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self.create_widgets()
        
    def create_widgets(self):
        
        global fm_main # グローバル変数宣言しないとFrameを閉じれなくなる
        global pw_main
        global fm_graph_1
        global fm_graph_2
        
        
        
        volt = tk.StringVar()
        amp = tk.StringVar()
        watt = tk.StringVar()
        watt = tk.StringVar() # check
        temp = tk.StringVar()
        ohm = tk.StringVar()
        count = tk.StringVar()
        value = tk.StringVar()
        
        #メインウィンドウ作成
        pw_main = tk.PanedWindow(self.master, bg="#add8e6", orient='vertical')
        pw_main.pack(expand=True, fill = tk.BOTH, side="left")
        
        
        #メインフレーム作成
        fm_main = tk.Frame(pw_main, bd=10, bg="#add8e6", relief="ridge")
        pw_main.add(fm_main)
        
        
        
    # -------- メインフレームのオブジェクト作成 --------
    
        # padx, pady ：外側の横、縦の隙間
        # row, column : 行、列
        #label_space = tk.Label(fm_main, text="", bg="#add8e6", height=1, width=10)
        #label_space.grid(row=0, column=0, padx=40, pady=10)
        
        label_head = tk.Label(fm_main, text="   ~~計測された各値~~", bg="#add8e6", font=("Arial", 15), height=2)
        label_head.grid(row=1, column=0, columnspan=3)
        
        label_head = tk.Label(fm_main, text=" ~~詳細設定~~", bg="#add8e6", font=("Arial", 15), height=2)
        label_head.grid(row=1, column=4, columnspan=3, sticky=tk.W)
        
        label_head = tk.Label(fm_main, text=" ~~実行・停止~~", bg="#add8e6", font=("Arial", 15), height=2)
        label_head.grid(row=6, column=4, columnspan=3, sticky=tk.SW)
        
        
        
        label_volt = tk.Label(fm_main, text="〇電圧値(V)", bg="#add8e6", font=("Arial", 10), height=1, width=10)
        label_volt.grid(row=2, column=0, padx=40, pady=10)
        label_V = tk.Label(fm_main, text="V", bg="#add8e6", font=("Arial", 10))
        label_V.grid(row=2, column=2, padx=10, pady=10)
        label_amp = tk.Label(fm_main, text="〇電流値(mA)", bg="#add8e6", font=("Arial", 10), height=1, width=10)
        label_amp.grid(row=3, column=0, padx=40, pady=10)
        label_A = tk.Label(fm_main, text="mA", bg="#add8e6", font=("Arial", 10))
        label_A.grid(row=3, column=2, padx=10, pady=10)
        label_watt = tk.Label(fm_main, text="〇電力(mW)", bg="#add8e6", font=("Arial", 10), height=1, width=10)
        label_watt.grid(row=4, column=0, padx=40, pady=10)
        label_W = tk.Label(fm_main, text="mW", bg="#add8e6", font=("Arial", 10))
        label_W.grid(row=4, column=2, padx=10, pady=10)
        label_temp = tk.Label(fm_main, text="〇温度(℃)", bg="#add8e6", font=("Arial", 10), height=1, width=10)
        label_temp.grid(row=5, column=0, padx=40, pady=10)
        label_T = tk.Label(fm_main, text="℃", bg="#add8e6", font=("Arial", 10))
        label_T.grid(row=5, column=2, padx=10, pady=10)
        label_count = tk.Label(fm_main, text="〇カウント", bg="#add8e6", font=("Arial", 10), height=1, width=10)
        label_count.grid(row=6, column=0, padx=10, pady=10)

        #各値の出力用
        self.volt = tk.StringVar()
        box_volt = tk.Label(fm_main, bg="#f0ffff", font=("Arial", 10), height=1, width=5, textvariable=self.volt)
        box_volt.grid(row=2, column=1)
        self.amp = tk.StringVar()
        box_amp = tk.Label(fm_main, bg="#f0ffff", font=("Arial", 10), height=1, width=5, textvariable=self.amp)
        box_amp.grid(row=3, column=1)
        self.watt = tk.StringVar()
        box_watt = tk.Label(fm_main, bg="#f0ffff", font=("Arial", 10), height=1, width=5, textvariable=self.watt)
        box_watt.grid(row=4, column=1)
        self.temp = tk.StringVar()
        box_temp = tk.Label(fm_main, bg="#f0ffff", font=("Arial", 10), height=1, width=5, textvariable=self.temp)
        box_temp.grid(row=5, column=1)
        self.count = tk.StringVar()
        box_count = tk.Label(fm_main, bg="#f0ffff", font=("Arial", 10), height=1, width=5, textvariable=self.count)
        box_count.grid(row=6, column=1)

        label_space = tk.Label(fm_main, text="", bg="#add8e6", height=1, width=15)
        label_space.grid(row=2, column=3, padx=10, pady=10)
        
        
        #ファイルの名前入力用
        label_filename=tk.Label(fm_main, text="ファイル名：", bg="#add8e6", font=("Arial", 10), height=1)
        label_filename.grid(row=2, column=4, padx=2, pady=10, sticky=tk.W)
        # textvariableは一度selfで宣言しないといけないみたい...
        #StringVar：文字列を扱う, IntVar：整数を扱う, DoubleVar：浮遊小数点を扱う, BooleanVar：真偽値（True/False）を扱う
        self.filename_value = tk.StringVar()
        box_filename=tk.Entry(fm_main, bg="#e0ffff", font=("Arial", 13), width=13, textvariable=self.filename_value) #csvのファイル名を入力するところ
        box_filename.insert(tk.END, u'sample.csv')
        box_filename.grid(row=2, column=5, padx=2, pady=10, sticky=tk.W) #何も入力していないとエラーになる
        
        button_filename = tk.Button(fm_main, text="確認", **BUTTON_OPTIONS, font=("Arial", 10), width=6, command=self.change_filename)
        button_filename.grid(row=2, column=6, padx=2, pady=10, sticky=tk.W)
        
        
        self.var = tk.IntVar()
        self.var.set(1)
        self.LRturn = tk.IntVar()
        self.LRturn.set(1)
        button_turn = tk.Radiobutton(fm_main, bg="#add8e6", text="回転させる", variable=self.var, value=1)
        button_turn.grid(row=3, column=4)
        button_turn = tk.Radiobutton(fm_main, bg="#add8e6", text="回転させない", variable=self.var, value=0)
        button_turn.grid(row=3, column=5, sticky=tk.W)
        button_turn = tk.Radiobutton(fm_main, bg="#add8e6", text="時計回り", variable=self.LRturn, value=1)
        button_turn.grid(row=4, column=4)
        button_turn = tk.Radiobutton(fm_main, bg="#add8e6", text="反時計回り", variable=self.LRturn, value=0)
        button_turn.grid(row=4, column=5, sticky=tk.W)
        
        #回転させる回数の入力用
        label_turn = tk.Label(fm_main, text="回転させる数 :  ", bg="#add8e6", font=("Arial", 9), height=1)
        label_turn.grid(row=5, column=4)
        self.box_turn = tk.StringVar()
        box_turn = tk.Entry(fm_main, fg="#191970", bg="#e0ffff", font=("Arial", 13), width=4, textvariable=self.box_turn)
        box_turn.insert(tk.END, u'20')
        box_turn.grid(row=5, column=5, sticky=tk.W)
        
        #label_space = tk.Label(fm_main, text="", width=5)
        #label_space.grid(row=9, colum=5, columnspan=2, padx=45, pady=10)
        
        #実行・停止
        self.button_start = tk.Button(fm_main, text="スタート", **BUTTON_OPTIONS, font=("Arial", 12), width=10, command=self.dual_thread) #def start()
        self.button_start.grid(row=7, column=4, columnspan=2, padx=20, pady=10, sticky=tk.SW)
        
        button_stop = tk.Button(fm_main, text="一時停止", **BUTTON_OPTIONS, font=("Arial", 12), width=10, command=self.stop_tk)
        button_stop.grid(row=7, column=5, columnspan=2, padx=40, pady=10, sticky=tk.SW)
        
        self.check_value = tk.BooleanVar(value=True)
        chk = tk.Checkbutton(fm_main, bg="#add8e6", selectcolor="#ffe4e1", variable=self.check_value, onvalue=True, offvalue=False, text="終了したとき初期位置に戻す", font=("Arial", 10))
        chk.grid(row=8, column=4, columnspan=2, padx=20, pady=10, sticky=tk.W)
        
        button_stop = tk.Button(fm_main, text="終了", **BUTTON_OPTIONS, font=("Arial", 12), width=10, command=self.exit_tk)
        button_stop.grid(row=9, column=5, columnspan=2, padx=45, pady=10, sticky=tk.W)
        
        
        #グラフを表示するボタン
        button_graph_1 = tk.Button(fm_main, text="IT Graph", **BUTTON_OPTIONS, font=("Arial", 12), width=8, command=self.create_graph_1)
        button_graph_1.grid(row=7, column=0, columnspan=2, padx=20, pady=20, sticky=tk.E)
        
        button_graph_2 = tk.Button(fm_main, text="IV Graph", **BUTTON_OPTIONS, font=("Arial", 12), width=8, command=self.create_graph_2)
        button_graph_2.grid(row=7, column=2, columnspan=2, padx=20, pady=20, sticky=tk.W)
        
        
        
        
        
        
                
        print('DEBUG:----{}----'.format(sys._getframe().f_code.co_name)) if self.DEBUG_LOG else ""
        
        
        
        
        
        
    def filename(self):
        fn = self.filename_value.get()
        print(fn)
        return fn
    
    
    def change_filename(self):
        fn = str(self.filename_value.get())
        res = messagebox.showinfo("title", f" csvファイルは {dir_op_path}/{fn}\n に保存されます。")
        print("ChangeFileName", res)
        
        

    #スタートボタンが押されたときの処理
    def start_tk(self):
                
        global is_stop
        is_stop = True
        
        #スタートボタンのテキストの値を取得（「再開」であればrestart_CountをCountに代入）
        button_text = self.button_start.cget("text")
        if button_text == "再開":
            #スタートボタンのテキストを「スタート」に変更
            self.button_start.config(text = "スタート")
            #global is_restart_Count
            #Count = is_restart_Count
            
            
        messagebox.showinfo("title", "スタートが押されたときの処理を記述していきます。", icon="info")
        
        fn = str(self.filename_value.get())
        print("csvFileDirectory : " + str(dir_op_path) + "/" + str(fn))
        file_name = fn
        
        var_value = self.var.get()
        LR = self.LRturn.get()
        intturn=int(self.box_turn.get())
        print("var_value : " + str(var_value) + "\nLR : " + str(LR) + "\ncount : " + str(intturn))
        
        Amp = 0
        Volt = 0
        Watt = 0
        Temp = 20
        
        for Count in range(1, intturn + 1):
            
            global counter_list
            
            global amp_list
            global volt_list
            global watt_list
            global temp_list
            global count_list
            global for_count
            
            if is_stop == False:
                print("is_stop == False:")
                #スタートボタンのテキストを「再開」に変更
                self.button_start.config(text = "再開")
                is_restart_Count = Count
                break
                
            elif is_stop == True:
                if LR == 1:
                    LR_turn = "Right"
                elif LR == 0:
                    LR_turn = "Left"
                #ターミナルにログを表示する（メモリ使用率が多くなる場合は無くしてもよい）    
                if LR_turn == "Right":
                    print("is_stop == True:" + str(Count) + "count:" + "Right")
                    counter_list.append("Right")
                elif LR_turn == "Left":
                    print("is_stop == True:" + str(Count) + "count:" + "Left")
                    counter_list.append("Left")
                
                
                self.count.set(str(Count))
                self.amp.set(str(Amp))
                self.volt.set(str(Volt))
                self.watt.set(str(Watt))
                self.temp.set(str(Temp))
                
                #グラフ作成のために値を配列に代入
                amp_list.append(int(Amp))
                volt_list.append(int(Volt))
                watt_list.append(int(Watt))
                temp_list.append(int(Temp))
                for_count = for_count + 1
                count_list.append(for_count)
                
                len_count = len(count_list) - 1
                #print(amp_list[len_count] + " : " + volt_list[len_count] + " : " + watt_list[len_count] + " : " + temp_list[len_count] + " : " + count_list[len_count])
                
                #デモグラフのためにランダムに値を入れてる
                Count = Count + 1
                Amp = rand.randrange(10)
                Volt = rand.randrange(10)
                Watt = int(Amp) * int(Volt)
                
                time.sleep(1)
            
            else:
                print("Errors related to global variables")
                break
            
            
            
            
    #start_tkを並列処理で実行する
    def dual_thread(self):
        thread = threading.Thread(target=self.start_tk)
        thread.start()      
        
        
    
    
    
    #グラフ１（電力と時間）のウィンドウが表示される
    def create_graph_1(self):
        
        global fm_graph_1
        global pw_graph_1
        pw_main.destroy()
        
        global return_opened_1
        return_opened_1 = True
        
        #グラフ１ウィンドウ作成
        pw_graph_1 = tk.PanedWindow(self.master, bg="#ffffff", orient='vertical')
        pw_graph_1.pack(expand=True, fill = tk.BOTH, side="left")
        
        #グラフ１フレーム作成
        fm_graph_1 = tk.Frame(bd=10, bg="#ffffff", relief="ridge")
        pw_graph_1.add(fm_graph_1)
        
        
        # フレームの幅と高さを取得
        width = self.winfo_width()
        height = self.winfo_height()
        
        
        # matplotlibの描画領域の作成
        self.fig = Figure(figsize=(width*0.8, height*0.8))
        #座標軸の作成
        self.ax = self.fig.add_subplot(1, 1, 1)
        # 描画領域とFrameの関連ずけ
        self.fig_canvas = FigureCanvasTkAgg(self.fig, fm_graph_1)
        # matplotlibのツールバーを作成
        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, fm_graph_1)
        # matplotlibのグラフをフレームに配置
        self.fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
        #タイトル・ラベル
        self.ax.set_title("電力と時間の関係のグラフ", fontname="MS Mincho", fontweight="bold", fontsize=14, color="#000080")
        self.ax.set_xlabel("時間", fontname="MS Mincho", fontweight="bold", fontsize=10, color="#000080")
        self.ax.set_ylabel("電力", fontname="MS Mincho", fontweight="bold", fontsize=10, color="#000080")
        
        #表示するデータの作成
        global watt_list
        global count_list
        x = count_list
        y = watt_list
        
        #軸の最大値・最小値
        global for_count
        if for_count == 0:
            self.ax.set_xlim(0, 10)
            self.ax.set_ylim(0, 10)
        else:
            len_count = len(count_list) - 1
            max_watt = max(watt_list)
            max_watt_plus = max_watt * 1.2
            self.ax.set_xlim(0, count_list[len_count])
            self.ax.set_ylim(0, max_watt_plus)
        
        self.ax.grid(color="#c0c0c0", alpha=0.6, linestyle="--")
        
        #グラフを描画
        self.ax.plot(x, y)
    
        
    # -------- グラフを表示するフレームのオブジェクト作成 --------
        button_back_fm = tk.Button(fm_graph_1, text="戻る", **BUTTON_OPTIONS, font=("Arial", 12), width=12,  command=self.back_fm)
        button_back_fm.pack(side = tk.RIGHT, padx=80, pady=5)
        
        
        print('DEBUG:----{}----'.format(sys._getframe().f_code.co_name)) if self.DEBUG_LOG else ""
    
    
    
    
    #グラフ２（電流と電圧）のウィンドウが表示される
    def create_graph_2(self):
        
        global fm_graph_2
        global pw_graph_2
        pw_main.destroy()
        
        global return_opened_2
        return_opened_2 = True
        
        #グラフ２ウィンドウ作成
        pw_graph_2 = tk.PanedWindow(self.master, bg="#ffffff", orient='vertical')
        pw_graph_2.pack(expand=True, fill = tk.BOTH, side="left")
        
        #グラフ２フレーム作成
        fm_graph_2 = tk.Frame(bd=10, bg="#ffffff", relief="ridge")
        pw_graph_2.add(fm_graph_2)
        
        
        # フレームの幅と高さを取得
        width = self.winfo_width()
        height = self.winfo_height()
        
        
        # matplotlibの描画領域の作成
        self.fig = Figure(figsize=(width*0.8, height*0.8))
        #座標軸の作成
        self.ax = self.fig.add_subplot(1, 1, 1)
        # 描画領域とFrameの関連ずけ
        self.fig_canvas = FigureCanvasTkAgg(self.fig, fm_graph_2)
        # matplotlibのツールバーを作成
        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, fm_graph_2)
        # matplotlibのグラフをフレームに配置
        self.fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
        #タイトル・ラベル
        self.ax.set_title("電流と電圧の関係のグラフ", fontname="MS Mincho", fontweight="bold", fontsize=14, color="#000080")
        self.ax.set_xlabel("電流", fontname="MS Mincho", fontweight="bold", fontsize=10, color="#000080")
        self.ax.set_ylabel("電圧", fontname="MS Mincho", fontweight="bold", fontsize=10, color="#000080")
        
        #表示するデータの作成
        global amp_list
        global volt_list
        global count_list
        x = amp_list
        y = volt_list
        
        #軸の最大値・最小値
        global for_count
        if for_count == 0:
            self.ax.set_xlim(0, 10)
            self.ax.set_ylim(0, 10)
        else:
            max_amp = max(amp_list)
            max_amp_plus = max_amp * 1.2
            max_volt = max(volt_list)
            max_volt_plus = max_volt * 1.5
            self.ax.set_xlim(0, max_amp_plus)
            self.ax.set_ylim(0, max_volt_plus)
        
        self.ax.grid(color="#c0c0c0", alpha=0.8, linestyle="--")
        
        #グラフを描画
        self.ax.scatter(x, y, s = 200, color="pink", alpha=0.6, edgecolors="red")
        
        
    # -------- グラフを表示するフレームのオブジェクト作成 --------
        button_back_fm = tk.Button(fm_graph_2, text="戻る", **BUTTON_OPTIONS, font=("Arial", 12), width=12,  command=self.back_fm)
        button_back_fm.pack(side = tk.RIGHT, padx=80, pady=5)
        
        
        print('DEBUG:----{}----'.format(sys._getframe().f_code.co_name)) if self.DEBUG_LOG else ""
        
        
        
        
    #グラフのウィンドウからメインウィンドウに戻る
    def back_fm(self):
        
        global return_opened_1
        global return_opened_2
        
        if return_opened_1 == True:
            pw_graph_1.destroy()
            return_opened_1 = False
            self.create_widgets()
            
        elif return_opened_2 == True:
            pw_graph_2.destroy()
            return_opened_2 = False
            self.create_widgets()
            
        
        
        
    #一時停止ボタンが押されたときの処理
    def stop_tk(self):
        res = messagebox.showinfo("title", "一時停止のプログラムを実行します", icon="info")
        print("stop", res)
        
        global is_stop
        is_stop = False
        
        
        
    #終了ボタンが押されたときの処理
    def exit_tk(self):
        
        
        if self.check_value.get():
            #第三引数のオプションについて：
            #detail : 詳細メッセージ 
            #icon : アイコン設定（info, warning, error, question）
            res = messagebox.askquestion("title", "初期位置に戻るプログラムを実行しますか？", detail="※※ここに初期位置に戻るプログラムを書いていきます。\n　　まだ条件分岐は行われません。", icon="info")
            print("InitialPosition", res)
            if res == "yes":
                
                global counter_list
                
                print("LR : " + str(counter_list))
                right_count = counter_list.count("Right")
                print("right_count : " + str(right_count))
                left_count = counter_list.count("Left")
                print("left_count : " + str(left_count))
                
                if right_count > left_count:
                    diff_count = right_count - left_count
                    print("difference : " + str(diff_count) + " : " + "right_count")
                    # ---- 反時計回りに戻すプログラムを記載していく ----
                    
                    self.master.quit() #tkinterFrameの終了
                    
                    
                elif left_count > right_count:
                    diff_count = left_count - right_count
                    print("difference : " + str(diff_count) + " : " + "right_count")
                    # ---- 時計回りに戻すプログラムを記載していく ----
                    
                    self.master.quit() #tkinterFrameの終了
                    
                    
                else:
                    diff_count = 0
                    print("difference : " + str(diff_count) + " : " + "Same value")
                    
                    self.master.quit() #tkinterFrameの終了
                    
                    
                    
                
                
                
            elif res == "no":
                print("continue")
                
        
        else:
            res = messagebox.askquestion("title", "アプリケーションを終了しますか？", icon="warning")
            print("EndYesNo", res)
            if res == "yes":
                
                #status_file.write("一回目だよ")
                #status_file.close()
                
                self.master.quit() #tkinterFrameの終了
                #cmd="quit"
                #p = subprocess.Popen("exec " + cmd, shell=True)       
                #p.kill()                                            
                
            elif res == "no":
                print("continue")
                
        

# 実行
main_window = tk.Tk()        
myapp = Application(master=main_window)
myapp.master.title("太陽光発電システムを用いた金融教材") # メインウィンドウの名前
myapp.master.geometry("800x480") # ウィンドウの幅と高さピクセル単位で指定（width x height）
#myapp.master.geometry("1024x600")がラズパイ7インチモニターに多い解像度

myapp.mainloop()