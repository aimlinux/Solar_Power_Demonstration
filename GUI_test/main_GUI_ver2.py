# -*- coding: utf-8 -*-
from concurrent.futures import thread
import tkinter as tk
from tkinter import filedialog 
from tkinter import messagebox 
import re
import numpy as np
import datetime
import subprocess

from matplotlib.pyplot import box
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


BUTTON_OPTIONS = {
    "fg": "#fff0f5",
    "bg": "#0b0b33",
    "activebackground": "#77ffd4",
    "activeforeground": "#ff1493",
    "cursor": "xterm",
    "highlightbackground": "#483d8b",
}
main_cursors = "left_ptr"
button_cursors = "X_corsor"




# アプリケーション（GUI）クラス
class Application(tk.Frame):
    DEBUG_LOG = True
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        self.create_widgets()
        
    def create_widgets(self):
        
        
        
        volt = tk.StringVar()
        amp = tk.StringVar()
        watt = tk.StringVar()
        watth = tk.StringVar()
        temp = tk.StringVar()
        ohm = tk.StringVar()
        count = tk.StringVar()
        value = tk.StringVar()
        
        #ペインウィンドウ
        pw_main = tk.PanedWindow(self.master, bg="#add8e6", orient='vertical')
        pw_main.pack(expand=True, fill = tk.BOTH, side="left")
        
        
        #メインフレーム作成
        fm_main = tk.Frame(pw_main, bd=10, bg="#add8e6", relief="ridge")
        pw_main.add(fm_main)
        
        
        
        #各ラベル作成
        # padx, pady ：外側の横、縦の隙間
        # row, column : 行、列
        label_space = tk.Label(fm_main, text="", bg="#add8e6", height=1, width=10)
        label_space.grid(row=0, column=0, padx=40, pady=10)
        
        label_head = tk.Label(fm_main, text="   ~~計測された各値~~", bg="#add8e6", font=("Arial", 15), height=2)
        label_head.grid(row=1, column=0, columnspan=3)
        
        label_head = tk.Label(fm_main, text=" ~~詳細設定~~", bg="#add8e6", font=("Arial", 15), height=2)
        label_head.grid(row=1, column=4, columnspan=3, sticky=tk.W)
        
        label_head = tk.Label(fm_main, text=" ~~実行・停止~~", bg="#add8e6", font=("Arial", 15), height=2)
        label_head.grid(row=6, column=4, columnspan=3, sticky=tk.SW)
        
        
        
        label_volt = tk.Label(fm_main, text="〇電圧値(V)", bg="#add8e6", font=("Arial", 10), height=2, width=10)
        label_volt.grid(row=2, column=0, padx=40, pady=10)
        label_V = tk.Label(fm_main, text="V", bg="#add8e6", font=("Arial", 10))
        label_V.grid(row=2, column=2, padx=10, pady=10)
        label_amp = tk.Label(fm_main, text="〇電流値(mA)", bg="#add8e6", font=("Arial", 10), height=2, width=10)
        label_amp.grid(row=3, column=0, padx=40, pady=10)
        label_A = tk.Label(fm_main, text="mA", bg="#add8e6", font=("Arial", 10))
        label_A.grid(row=3, column=2, padx=10, pady=10)
        label_watt = tk.Label(fm_main, text="〇電力(mW)", bg="#add8e6", font=("Arial", 10), height=2, width=10)
        label_watt.grid(row=4, column=0, padx=40, pady=10)
        label_W = tk.Label(fm_main, text="mW", bg="#add8e6", font=("Arial", 10))
        label_W.grid(row=4, column=2, padx=10, pady=10)
        label_temp = tk.Label(fm_main, text="〇温度(℃)", bg="#add8e6", font=("Arial", 10), height=2, width=10)
        label_temp.grid(row=5, column=0, padx=40, pady=10)
        label_T = tk.Label(fm_main, text="℃", bg="#add8e6", font=("Arial", 10))
        label_T.grid(row=5, column=2, padx=10, pady=10)
        label_count = tk.Label(fm_main, text="〇カウント", bg="#add8e6", font=("Arial", 10), height=2, width=10)
        label_count.grid(row=6, column=0, padx=10, pady=10)

        #各値の出力用
        box_volt = tk.Label(fm_main, bg="#f0ffff", font=("Arial", 10), height=2, width=3, textvariable=volt)
        box_volt.grid(row=2, column=1)
        box_amp = tk.Label(fm_main, bg="#f0ffff", font=("Arial", 10), height=2, width=3, textvariable=amp)
        box_amp.grid(row=3, column=1)
        box_watt = tk.Label(fm_main, bg="#f0ffff", font=("Arial", 10), height=2, width=3, textvariable=watt)
        box_watt.grid(row=4, column=1)
        box_temp = tk.Label(fm_main, bg="#f0ffff", font=("Arial", 10), height=2, width=3, textvariable=temp)
        box_temp.grid(row=5, column=1)
        box_count = tk.Label(fm_main, bg="#f0ffff", font=("Arial", 10), height=2, width=3, textvariable=count)
        box_count.grid(row=6, column=1)

        label_space = tk.Label(fm_main, text="", bg="#add8e6", height=2, width=15)
        label_space.grid(row=2, column=3, padx=10, pady=10)
        
        
        #ファイルの名前入力用
        label_filename=tk.Label(fm_main, text="ファイル名を選択：", bg="#add8e6", font=("Arial", 10), height=2)
        label_filename.grid(row=2, column=4, padx=10, pady=10, sticky=tk.W)
        box_filename=tk.Entry(fm_main, bg="#e0ffff", font=("Arial", 13), width=13)#csvのファイル名を入力するところ
        box_filename.grid(row=2, column=5, padx=10, pady=10)#何も入力していないとエラーになる
        
        var = tk.IntVar()
        var.set(0)
        LRturn = tk.IntVar()
        LRturn.set(1)
        button_turn = tk.Radiobutton(fm_main, bg="#add8e6", text="回転させる", variable=var, value=1)
        button_turn.grid(row=3, column=4)
        button_turn = tk.Radiobutton(fm_main, bg="#add8e6", text="回転させない", variable=var, value=0)
        button_turn.grid(row=3, column=5, sticky=tk.W)
        button_turn = tk.Radiobutton(fm_main, bg="#add8e6", text="時計回り", variable=LRturn, value=1)
        button_turn.grid(row=4, column=4)
        button_turn = tk.Radiobutton(fm_main, bg="#add8e6", text="反時計回り", variable=LRturn, value=0)
        button_turn.grid(row=4, column=5, sticky=tk.W)
        
        #回転させる回数の入力用
        label_turn = tk.Label(fm_main, text="回転させる数 ：  ", bg="#add8e6", font=("Arial", 9), height=2)
        label_turn.grid(row=5, column=4)
        box_turn = tk.Entry(fm_main, fg="#191970", bg="#e0ffff", font=("Arial", 13), width=4)
        box_turn.grid(row=5, column=5, sticky=tk.W)
        
        
        #実行・停止
        button_start = tk.Button(fm_main, text="スタート", **BUTTON_OPTIONS, font=("Arial", 12), width=10)#スタートボタンの配置、押したらdef start()が動く
        button_start.grid(row=7, column=4, columnspan=2, padx=20, pady=10, sticky=tk.SW)
        
        button_stop = tk.Button(fm_main, text="一時停止", **BUTTON_OPTIONS, font=("Arial", 12), width=10)
        button_stop.grid(row=7, column=5, columnspan=2, padx=40, pady=10, sticky=tk.SW)
        
        bln = tk.BooleanVar()
        bln.set(False)
        chk = tk.Checkbutton(fm_main, bg="#add8e6", variable=bln, onvalue=True, offvalue=False, text="終了したとき初期位置に戻す", font=("Arial", 10))
        chk.grid(row=8, column=4, columnspan=2, padx=20, pady=10, sticky=tk.W)
        
        button_stop = tk.Button(fm_main, text="終了", **BUTTON_OPTIONS, font=("Arial", 12), width=10, command=self.exit_tk)
        button_stop.grid(row=9, column=5, columnspan=2, padx=45, pady=10, sticky=tk.W)
        
        
                
        print('DEBUG:----{}----'.format(sys._getframe().f_code.co_name)) if self.DEBUG_LOG else ""
        
        
        
                
    def exit_tk(self):
        
        if bln.get():
            messagebox.showinfo("初期位置に戻るプログラムを実行します。")
        else:
            #第三引数のオプションについて：
            #detail : 詳細メッセージ 
            #icon : アイコン設定（info, warning, error, question）
            res = messagebox.askquestion("title", "アプリケーションを終了しますか？", icon="warning")
            print("askyesno", res)

            if res == "yes":
                self.master.quit()
                #main_window.destroy
            elif res == "no":
                messagebox.showinfo("戻る", "アプリケーションを続けます。", icon="info")
            
        

# 実行
main_window = tk.Tk()        
myapp = Application(master=main_window)
myapp.master.title("太陽光発電システムを用いた金融教材") # メインウィンドウの名前
myapp.master.geometry("760x580") # ウィンドウの幅と高さピクセル単位で指定（width x height）
#myapp.master.geometry("1024x600")がラズパイ7インチモニターに多い解像度

myapp.mainloop()