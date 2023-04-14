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
import RPi.GPIO as GPIO #ラズパイのピン指定用(windowsじゃ動かない)
import smbus #(windowsじゃ動かない)
import threading

#csvの保存先
dir_op_path = '/home/pi/kakuda/csv'#''の中に保存先のディレクトリを指定

#ピンのセットアップa
direction = 20
step = 21

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(direction, GPIO.OUT)
GPIO.setup(step, GPIO.OUT)#highとlowを入れるとこ
#GPIO.output(direction, 0)#回転の向き

bus = smbus.SMBus(1)
address_adt7420 = 0x48
register_adt7420 = 0x00
configration_adt7420 = 0x03

csv_label = []#csvファイルの最初の行
csv_label.append("count")
csv_label.append("volt")
csv_label.append("amp")
csv_label.append("watt")
csv_label.append("watth")
csv_label.append("temp")
csv_label.append("ohm")

def filename():
    fn = str(box_filename.get())
    return fn

def turn():
    GPIO.output(step, GPIO.HIGH)
    sleep(0.001)
    GPIO.output(step, GPIO.LOW)

    #startボタンが押されたときの処理
def start():
    file_name = filename()#ファイル名
    print("ファイル名="+str(file_name))
    value=var.get()
    LR=LRturn.get()
    intturn=int(box_turn.get())
    #ここでcsvのファイルを作る
    with open(os.path.join(dir_op_path,file_name),"w") as f:
        writer = csv.writer(f)
        writer.writerow(csv_label)
        b_res = 0
        b_resA = 0
        for Count in range(1,intturn+1):#モーターを回したり電流電圧を測定する回数(rangeの中は1回目からn+1回分)
            csv_value = []#csvに入れるために配列にしてる
            
            GPIO.output(direction, LR)#回転の向き

            if value==1:#モーターを回すにチェックが入っているとき
                turn()#モーターを1ステップ動かす

            check = subprocess.getoutput("i2cget -y 1 0x40 0x02 w") #checkに値を入れる
            if check == "Error: Read failed": #たまにエラーが起きるのでエラーの文字を受け取ったとき
                res = b_res #前回の値を代入
            else:
                res =(int(check[4:6],16)*256+int(check[2:4],16))*1.25/1000 #エラーはかずにちゃんと値が取れた時
            Volt = res #電圧の代入
            b_res = res #エラーの時の代入用
            volt.set(str(Volt))

            check = subprocess.getoutput("i2cget -y 1 0x40 0x01 w")
            if check == "Error: Read failed":
                resA = b_resA
            elif int(check[4:6],16)<128:
                resA = (int(check[4:6],16)*256+int(check[2:4],16))
            else:
                resA = (int(check[4:6],16)*256+int(check[2:4],16)-256*256)
            Amp = resA#電流の代入
            b_resA = resA
            amp.set(str(Amp))

            if Count==1 or Count%15==0 or Count==intturn:
                sleep(0.1)
                bus.write_word_data(address_adt7420, configration_adt7420, 0x00)
                word_data = bus.read_word_data(address_adt7420, register_adt7420)
                rdata = (word_data & 0xff00) >> 8 | (word_data & 0xff) << 8
                sdata = rdata >> 3
                data=sdata/16
                resT = round(data,1)#小数点以下1桁まで
                Temp = resT#温度の入力
                temp.set(str(Temp))
                #csv_value.append(Temp)

            Watt = Volt*Amp#電圧*電流
            watt.set(str(Watt))
            
            count.set(str(Count))

            print(Count)
            
            csv_value.append(Count)#配列に各要素を入力
            csv_value.append(Volt)
            csv_value.append(Amp)
            csv_value.append(Watt)
            csv_value.append(temp.get())
            
            writer.writerow(csv_value)#csv_valueの中身を入力

            sleep(1)
        
        f.close()#csvファイルを閉じる(入力終了)


def dual_thread():#
    thread = threading.Thread(target=start)
    thread.start()        


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
button=tk.Button(frame,text="スタート",command=dual_thread)#スタートボタンの配置、押したらdef start()が動く
button.grid(row=6,column=1)


main_window.mainloop()
