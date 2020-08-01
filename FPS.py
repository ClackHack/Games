import time
import os
clear = lambda: os.system("cls")
print("Hey")
time.sleep(1)
clear()
input()
h=40
w=120
a = 0.0
m=[]
p=[7.0,7.0]
lastPos=[7,7]
m.append("#########.......")
m.append("#...............")
m.append("#.......########")
m.append("#..............#")
m.append("#......##......#")
m.append("#......##......#")
m.append("#..............#")
m.append("###............#")
m.append("##.............#")
m.append("#......####..###")
m.append("#......#.......#")
m.append("#......#.......#")
m.append("#..............#")
m.append("#......#########")
m.append("#..............#")
m.append("################")
def updateMap():
    global m
    global p
    global lastPos
    place=[]
    place=list(m[lastPos[1]])
    place[lastPos[0]]="."
    place="".join(place)
    m[lastPos[1]]=place
    
    place=[]
    place=list(m[int(p[1])])
    place[int(p[0])] = "p"
    place="".join(place)
    m[int(p[1])]=place
