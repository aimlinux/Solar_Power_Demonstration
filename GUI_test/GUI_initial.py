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


#メインウィンドウの作成
main_window = tk.Tk()#メインウィンドウの作成
main_window.title("太陽光発電システムを用いた金融教材")#メインウィンドウの名前
main_window.geometry("600x300")#メインウィンドウのサイズ

volt = tk.StringVar()
amp = tk.StringVar()
watt = tk.StringVar()
watth = tk.StringVar()
temp = tk.StringVar()
ohm = tk.StringVar()
count = tk.StringVar()
value = tk.StringVar()


#フレームの作成
frame = tk.Frame(main_window)#メインウィンドウの中にフレームを作成
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
button.grid(row=6,column=1)

main_window.mainloop()