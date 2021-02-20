from tkinter import *
import os
import math,time,datetime
import pickle
from colorama import Fore, Back, Style,init
#init(autoreset=True)
import random
global data
data = [0,0,0,0,0,0,0,0,0,0]
global key
key=None
def readData():
    global data
    with open("data.txt","rb") as f:
        data = pickle.load(f)
def writeData():
    global data
    with open("data.txt","wb") as f:
        pickle.dump(data,f)
def game():
    
main = Tk()
def left(event):
    global key
    key="left"

def right(event):
    global key
    key="right"
def up(event):
    global key
    key="up"
def down(event):
    global key
    key="down"
def q(event):
    global key
    key="q"
    import sys;sys.exit()
#main.bind('<Left>', left)
#main.bind('<Right>', right)
#main.bind("<Up>",up)
#main.bind("<Down>",down)
main.bind('a', left)
main.bind('d', right)
main.bind("w",up)
main.bind("s",down)
main.bind("q",q)
main.mainloop()

