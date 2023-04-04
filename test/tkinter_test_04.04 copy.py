# -*- coding: utf-8 -*-
from concurrent.futures import thread
import tkinter as tk
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
        pw_main = tk.PanedWindow(self.master, bg="cyan", orient='vertical')
        pw_main.pack(expand=True, fill = tk.BOTH, side="left")
        
        
        #左フレーム作成
        fm_main = tk.Frame(pw_main, bd=10, bg="#ffffff", relief="ridge")
        pw_main.add(fm_main)
        
        
        
        #各ラベル作成
        # padx, pady ：外側の横、縦の隙間
        # row, column : 行、列
        label_space = tk.Label(fm_main, text="", bg="#ffffff", height=1, width=10)
        label_space.grid(row=0, column=0, padx=40, pady=10)
        
        label_head = tk.Label(fm_main, text="   ~~計測された各値~~", bg="#ffffff", font=("Arial", 15, "bold"), height=2)
        label_head.grid(row=1, column=0, columnspan=3)
        
        label_head = tk.Label(fm_main, text=" ~~詳細設定~~", bg="#ffffff", font=("Arial", 15), height=2)
        label_head.grid(row=1, column=4, columnspan=3, sticky=tk.W)
        
        label_head = tk.Label(fm_main, text=" ~~実行・停止~~", bg="#ffffff", font=("Arial", 15), height=2)
        label_head.grid(row=6, column=4, columnspan=3, sticky=tk.SW)
        
        
        
        label_volt = tk.Label(fm_main, text="〇電圧値(V)", bg="#ffffff", font=("Arial", 10), height=2, width=10)
        label_volt.grid(row=2, column=0, padx=40, pady=10)
        label_V = tk.Label(fm_main, text="V", bg="#ffffff", font=("Arial", 10))
        label_V.grid(row=2, column=2, padx=10, pady=10)
        label_amp = tk.Label(fm_main, text="〇電流値(mA)", bg="#ffffff", font=("Arial", 10), height=2, width=10)
        label_amp.grid(row=3, column=0, padx=40, pady=10)
        label_A = tk.Label(fm_main, text="mA", bg="#ffffff", font=("Arial", 10))
        label_A.grid(row=3, column=2, padx=10, pady=10)
        label_watt = tk.Label(fm_main, text="〇電力(mW)", bg="#ffffff", font=("Arial", 10), height=2, width=10)
        label_watt.grid(row=4, column=0, padx=40, pady=10)
        label_W = tk.Label(fm_main, text="mW", bg="#ffffff", font=("Arial", 10))
        label_W.grid(row=4, column=2, padx=10, pady=10)
        label_temp = tk.Label(fm_main, text="〇温度(℃)", bg="#ffffff", font=("Arial", 10), height=2, width=10)
        label_temp.grid(row=5, column=0, padx=40, pady=10)
        label_T = tk.Label(fm_main, text="℃", bg="#ffffff", font=("Arial", 10))
        label_T.grid(row=5, column=2, padx=10, pady=10)
        label_count = tk.Label(fm_main, text="〇カウント", bg="#ffffff", font=("Arial", 10), height=2, width=10)
        label_count.grid(row=6, column=0, padx=10, pady=10)

        #各値の出力用
        box_volt = tk.Label(fm_main, font=("Arial", 10), height=2, width=3, textvariable=volt)
        box_volt.grid(row=2, column=1)
        box_amp = tk.Label(fm_main, font=("Arial", 10), height=2, width=3, textvariable=amp)
        box_amp.grid(row=3, column=1)
        box_watt = tk.Label(fm_main, font=("Arial", 10), height=2, width=3, textvariable=watt)
        box_watt.grid(row=4, column=1)
        box_temp = tk.Label(fm_main, font=("Arial", 10), height=2, width=3, textvariable=temp)
        box_temp.grid(row=5, column=1)
        box_count = tk.Label(fm_main, font=("Arial", 10), height=2, width=3, textvariable=count)
        box_count.grid(row=6, column=1)

        label_space = tk.Label(fm_main, text="", bg="#ffffff", height=2, width=15)
        label_space.grid(row=2, column=3, padx=10, pady=10)
        
        #ファイルの名前入力用
        label_filename=tk.Label(fm_main, text="ファイル名 ：", bg="#ffffff", font=("Arial", 10), height=2)
        label_filename.grid(row=2, column=4, padx=10, pady=10, sticky=tk.W)
        box_filename=tk.Entry(fm_main, bg="#e0ffff", font=("Arial", 13), width=13)#csvのファイル名を入力するところ
        box_filename.grid(row=2, column=5, padx=10, pady=10)#何も入力していないとエラーになる
        
        
        var = tk.IntVar()
        var.set(0)
        LRturn = tk.IntVar()
        LRturn.set(1)
        button_turn = tk.Radiobutton(fm_main, text="回転させる", variable=var, value=1)
        button_turn.grid(row=3, column=4)
        button_turn = tk.Radiobutton(fm_main, text="回転させない", variable=var, value=0)
        button_turn.grid(row=3, column=5, sticky=tk.W)
        button_turn = tk.Radiobutton(fm_main, text="時計回り", variable=LRturn, value=1)
        button_turn.grid(row=4, column=4)
        button_turn = tk.Radiobutton(fm_main, text="反時計回り", variable=LRturn, value=0)
        button_turn.grid(row=4, column=5, sticky=tk.W)
        
        #回転させる回数の入力用
        label_turn = tk.Label(fm_main, text="回転させる数 ：  ", bg="#ffffff", font=("Arial", 9), height=2)
        label_turn.grid(row=5, column=4)
        box_turn = tk.Entry(fm_main, bg="#e0ffff", font=("Arial", 13), width=4)
        box_turn.grid(row=5, column=5, sticky=tk.W)
        
        
        #実行・停止
        button_start = tk.Button(fm_main, text="スタート", bg="#dda0dd", font=("Arial", 12), width=10)#スタートボタンの配置、押したらdef start()が動く
        button_start.grid(row=7, column=4, columnspan=2, padx=20, pady=10, sticky=tk.SW)
        
        button_stop = tk.Button(fm_main, text="一時停止", bg="#dda0dd", font=("Arial", 12), width=10)
        button_stop.grid(row=7, column=5, columnspan=2, padx=40, pady=10, sticky=tk.SW)
        
        bln = tk.BooleanVar()
        bln.set(True)
        chk = tk.Checkbutton(fm_main, variable=bln, onvalue=True, offvalue=False, text="終了したとき初期位置に戻す", font=("Arial", 9))
        chk.grid(row=8, column=4, columnspan=2, padx=20, pady=10, sticky=tk.W)
        
        button_stop = tk.Button(fm_main, text="終了", bg="#dda0dd", font=("Arial", 12), width=10)
        button_stop.grid(row=9, column=5, columnspan=2, padx=45, pady=10, sticky=tk.W)
        
        
                
        print('DEBUG:----{}----'.format(sys._getframe().f_code.co_name)) if self.DEBUG_LOG else ""

# 実行
main_window = tk.Tk()        
myapp = Application(master=main_window)
myapp.master.title("太陽光発電システムを用いた金融教材") # メインウィンドウの名前
myapp.master.geometry("760x580") # ウィンドウの幅と高さピクセル単位で指定（width x height）
#myapp.master.geometry("720x480")

myapp.mainloop()






'''
#メインウィンドウの作成
main_window = tk.Tk()#メインウィンドウの作成
main_window.title("太陽光発電システムを用いた金融教材")#メインウィンドウの名前
main_window.geometry("800x500")#メインウィンドウのサイズ



volt = tk.StringVar()
amp = tk.StringVar()
watt = tk.StringVar()
watth = tk.StringVar()
temp = tk.StringVar()
ohm = tk.StringVar()
count = tk.StringVar()
value = tk.StringVar()


#フレームの作成
frame = tk.Frame(main_window, bd=5, relief="ridge")#メインウィンドウの中にフレームを作成

frame.pack(padx=10,pady=10)#フレームの中にラベルなどを作っていく

#ラベル作成
label_volt=tk.Label(frame,text="電圧値(V)")
label_volt.grid(row=0,column=0)
label_V=tk.Label(frame,text="V")
label_V.grid(row=0,column=2)
label_amp=tk.Label(frame,text="電流値")
label_amp.grid(row=1,column=0)
label_A=tk.Label(frame,text="mA")
label_A.grid(row=1,column=2)
label_watt=tk.Label(frame,text="電力")
label_watt.grid(row=2,column=0)
label_W=tk.Label(frame,text="mW")
label_W.grid(row=2,column=2)
label_temp=tk.Label(frame,text="温度")
label_temp.grid(row=3,column=0)
label_T=tk.Label(frame,text="℃")
label_T.grid(row=3,column=2)
label_count=tk.Label(frame,text="カウント")
label_count.grid(row=4,column=0)
label_filename=tk.Label(frame,text="ファイル名")
label_filename.grid(row=5,column=0)

#テキストボックスの作成
box_volt=tk.Label(frame,textvariable=volt)#出力用
box_volt.grid(row=0,column=1)
box_amp=tk.Label(frame,textvariable=amp)#出力用
box_amp.grid(row=1,column=1)
box_watt=tk.Label(frame,textvariable=watt)#出力用
box_watt.grid(row=2,column=1)
box_temp=tk.Label(frame,textvariable=temp)#出力用
box_temp.grid(row=3,column=1)
box_count=tk.Label(frame,textvariable=count)#出力用
box_count.grid(row=4,column=1)
box_filename=tk.Entry(frame,width=10)#csvのファイル名を入力するところ
box_filename.grid(row=5,column=1)#何も入力していないとエラーになる

var=tk.IntVar()
var.set(0)
LRturn=tk.IntVar()
LRturn.set(1)
button_turn=tk.Radiobutton(frame,text="回転させる",variable=var,value=1)
button_turn.grid(row=0,column=3)
button_turn=tk.Radiobutton(frame,text="回転させない",variable=var,value=0)
button_turn.grid(row=1,column=3)
button_turn=tk.Radiobutton(frame,text="時計回り",variable=LRturn,value=1)
button_turn.grid(row=2,column=3)
button_turn=tk.Radiobutton(frame,text="反時計回り",variable=LRturn,value=0)
button_turn.grid(row=3,column=3)
box_turn=tk.Entry(frame,text="回転させる回数", width=5)
box_turn.grid(row=4,column=3)


#スタートボタンの作成
button=tk.Button(frame,text="スタート")#スタートボタンの配置、押したらdef start()が動く
button.grid(row=6,column=3)



#チェックボックスの作成
bln = tk.BooleanVar()
bln.set(True)

chk = tk.Checkbutton(
    main_window,
    variable=bln,
    onvalue=True,
    offvalue=False,
    text="終了したとき初期位置に戻る")
chk.place(x=100, y=180)


#終了するボタンの作成
button = tk.Button(frame, text="終了する")
button.grid(row=30,column=3)


main_window.mainloop()

'''