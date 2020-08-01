from tkinter import *
import os
import math,time,datetime,random
import pickle,_thread
from colorama import Fore, Back, Style,init
clear = lambda:os.system("cls")
main = Tk()
height,width=14,14
l,r,u,d,q=False,True,False,False,False
def lose(snake):
    clear()
    print("You Died!!!")
    print("Score: ",len(snake))
    input()
    import sys;sys.exit()
def collision(snake):
    global height,width
    for x,y in snake:
        if snake.count([x,y]) > 1:
            
            return False
        if x>=width:
            return False
        if x<0:
            return False
        if y >=height:
            return False
        if y<0:
            return False
    return True
def move(snake,l,r,u,d,apple):
    if l:
        snake.insert(0,[snake[0][0]-1,snake[0][1]])
       
    elif r:
        snake.insert(0,[snake[0][0]+1,snake[0][1]])
        
    elif u:
        snake.insert(0,[snake[0][0],snake[0][1]-1])
        
    elif d:
        snake.insert(0,[snake[0][0],snake[0][1]+1])
    if not snake[0]==apple:
        snake.pop()
    else:
        apple=[random.randint(0,width-1),random.randint(0,height-1)]
    if collision(snake):
        return snake,apple
    else:
        lose(snake)
def game():
    
    global l,r,u,d,q,height,width
    
    snake=[[width//3,height//2]]
    apple=[random.randint(0,width-1),random.randint(0,height-1)]
    while not q:
        clear()
        
        print("# "*(width-2))
        for y in range(height):
            print("#",end="")
            c=0
            for x in range(width):
                
                if c==1:
                    c=0
                    print(" ",end="")
                else:
                    c=1
                if [x,y] in snake:
                    print("@",end="")
                elif [x,y]== apple:
                    print("$",end="")
                else:
                    print(" ",end="")
            print("#")
        print("# "*(width-2))
        snake,apple=move(snake,l,r,u,d,apple)
        #time.sleep(0.03)
    return
def left(event):
    global l,r,u,d
    l,r,u,d=True,False,False,False

def right(event):
    global l,r,u,d
    l,r,u,d=False,True,False,False

def up(event):
    global l,r,u,d
    l,r,u,d=False,False,True,False

def down(event):
    global l,r,u,d
    l,r,u,d=False,False,False,True
def qui(event):
    global q
    q=True
    import sys
    sys.exit()
main.bind('<Left>', left)
main.bind('<Right>', right)
main.bind("<Up>",up)
main.bind("<Down>",down)
main.bind('a', left)
main.bind('d', right)
main.bind("w",up)
main.bind("s",down)
main.bind("q",qui)
time.sleep(3)
_thread.start_new_thread(game,())

main.mainloop()
