from tkinter import *
import os
import math,time,datetime
import pickle
import generateImage
from colorama import Fore, Back, Style,init
#init(autoreset=True)
board=[]
d=None
dimensions=[17,17]
snake=[[dimensions[0]//2,dimensions[1]//2 -dimensions[1]//3]]
apple=[dimensions[0]//2,dimensions[1]//2+dimensions[1]//3]
for i in range(dimensions[1]):
    board.append(" "*dimensions[0])
def lose():
    global snake
    clear()
    print("You lose")
    print("Score: ",len(snake))
    input()
    import sys;sys.exit()
    
def printboard():
    global board
    global dimensions
    clear()
    screen = []
    layer=""
    for i in range(dimensions[0]+2):
        layer+="."
    screen.append(layer)
    layer=""
    for i in range(len(board)):
        layer = "."
        for j in range(len(board[i])):
            if [i,j] in snake:
                layer+="."
            elif [i,j]==apple:
                layer+="@"
            else:
                layer+=" "
            
        layer+="."
        screen.append(layer)
        layer=""
    for i in range(dimensions[0]+2):
        layer+="."
    screen.append(layer)
    layer=""
    global d
    if d == "up":
        pp = "N"
    elif d == "down":
        pp="S"
    elif d == "right":
        pp = "E"
    else:
        pp = "w"
    m = [list(i) for i in screen]
    
    print(generateImage.generate(m,pp,block=".",prize="@",player=snake[0],hieght=3))
    print("\n".join(["".join(i) for i in m]))
def check(m,l):
    global dimensions
    global apple
    global snake
    if l[0] <0 or l[0]>=dimensions[0]:
        lose()
        return -1
    if l[1] <0 or l[1]>=dimensions[1]:
        lose()
        return -1
        
    square = board[l[0]][l[1]]
    if l==apple:
        while 1:
            apple=[random.randint(0,dimensions[0]-1),random.randint(0,dimensions[0]-1)]
            if not apple in snake:
                break
             
        
        return 1
    elif l in snake:
        lose()
    elif square==" ":
        return 0
    
    
def direction(di):
    global d
    d=di
def game():
    global d
    move = d
    global board
    global snake
    while not d:
        pass
    while 1:
        
        move = d
        if move == "up":
            m=[snake[0][0]-1,snake[0][1]]
            code=check(board,m)
            if code == -1:
                return
            if code:
                snake.insert(0,m)
            else:
                snake.insert(0,m)
                
                snake.pop()
        if move == "down":
            m=[snake[0][0]+1,snake[0][1]]
            code=check(board,m)
            if code == -1:
                return
            if code:
                snake.insert(0,m)
            else:
                snake.insert(0,m)
                snake.pop()
        if move == "right":
            m=[snake[0][0],snake[0][1]+1]
            code=check(board,m)
            if code == -1:
                return
            if code:
                snake.insert(0,m)
            else:
                snake.insert(0,m)
                snake.pop()
        if move == "left":
            m=[snake[0][0],snake[0][1]-1]
            code=check(board,m)
            if code == -1:
                return
            if code:
                snake.insert(0,m)
            else:
                snake.insert(0,m)
                snake.pop()
        
        printboard()
        time.sleep(0.030)
import random
clear = lambda:os.system("cls")
main = Tk()
def left(event):
    direction("left")

def right(event):
    direction("right")
def up(event):
    direction("up")
def down(event):
    direction("down")
def q(event):
    import sys;sys.exit()
main.bind('<Left>', left)
main.bind('<Right>', right)
main.bind("<Up>",up)
main.bind("<Down>",down)
main.bind('a', left)
main.bind('d', right)
main.bind("w",up)
main.bind("s",down)
main.bind("q",q)
clear()
printboard()
import _thread
_thread.start_new_thread(game,())

main.mainloop()
