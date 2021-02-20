import math, copy
def rotate90(A):
    N = len(A[0])
    for i in range(N // 2):
        for j in range(i, N - i - 1):
            temp = A[i][j]
            A[i][j] = A[N - 1 - j][i]
            A[N - 1 - j][i] = A[N - 1 - i][N - 1 - j]
            A[N - 1 - i][N - 1 - j] = A[j][N - 1 - i]
            A[j][N - 1 - i] = temp

def rotate(map,direction):
    d = ["N","W","S","E"].index(direction.upper())
    updatedMap=copy.deepcopy(map)
    for i in range(d):
        try:
            rotate90(updatedMap)
        except KeyBoardInterrupt as e:
            print(e)
    return updatedMap
def withinMap(map,position):
    x,y=position
    return not (y>=len(map) or y<0 or x<0 or x>=len(map[0]))
def lowerhalf(map,player,angles,xMult,block="X",prize="",fog=10):
    distances=[]
    px,py = player
    for dx in angles:
        ##May want to edit handling of out of bounds cases
        val = fog
        for i in range(1,5):
            newPoint=(px+i*dx*xMult,py-i)
            if not withinMap(map,newPoint):
                val=math.dist((px,py),newPoint)
                break
            if map[newPoint[1]][newPoint[0]]==block:
                val = math.dist((px,py),newPoint)
                break
            if map[newPoint[1]][newPoint[0]]==prize:
                val=-1*i
                break
            if math.dist((px,py),newPoint) > fog:
                break
        distances.append(min(val,fog))
    return distances
def upperhalf(map,player,angles,xMult,block="X",prize="",fog=10):
    distances=[]
    px,py = player
    for dy in angles:
        ##May want to edit handling of out of bounds cases
        val = fog
        for i in range(1,5):
            newPoint=(px+i*xMult,py-i*dy)
            if not withinMap(map,newPoint):
                val=math.dist((px,py),newPoint)
                break
            if map[newPoint[1]][newPoint[0]]==block:
                val = math.dist((px,py),newPoint)
                break
            if map[newPoint[1]][newPoint[0]]==prize:
                val=-1*i
                break
            if math.dist((px,py),newPoint) > fog:
                break
        distances.append(min(val,fog))
    return distances
def raycast(player,map,direction,block="X",prize="▓",fog=10):
    px,py = player
    c = copy.deepcopy(map)
    c[py][px]='P'
    #print("\n".join(["".join(i) for i in c]))
    map = rotate(c,direction)
    for y,i in enumerate(map):
            for x,j in enumerate(i):
                if j=="P":
                    px,py=x,y
                    break
    #print(px,py)
    #print("\n".join(["".join(i) for i in map]))
    distances=[]
    xMult=-1
    val=fog
    #Left Raycast
    for i in range(1,fog+1):
        newPoint=(px+i*xMult,py)
        #print(map[newPoint[1]][newPoint[0]])
        if not withinMap(map,newPoint):
            val=i
            break
        if map[newPoint[1]][newPoint[0]]==block:
            val=i
            break
        if map[newPoint[1]][newPoint[0]]==prize:
            val=-1*i
            break
    distances.append(min(val,fog))
    #Lower Left Raycast
    angles=list(range(2,9))
    angles.reverse()
    distances.extend(lowerhalf(map,player,angles,xMult,block,prize,fog))
    #Middle Left Raycast
    val = fog
    for i in range(1,7):
            newPoint=(px+i*xMult,py-i)
            if not withinMap(map,newPoint):
                val=math.dist((px,py),newPoint)
                break
            if map[newPoint[1]][newPoint[0]]==block:
                val = math.dist((px,py),newPoint)
                break
            if map[newPoint[1]][newPoint[0]]==prize:
                val=-1*i
                break
            if math.dist((px,py),newPoint) > fog:
                break
    distances.append(min(val,10))
    #Upper Left Raycast
    angles.reverse()
    distances.extend(upperhalf(map,player,angles,xMult,block,prize,fog))
    #Forward raycast
    val = fog
    for i in range(1,fog+1):
        #print(map[py+i][px])
        if not withinMap(map,(px,py-i)):
            #print("UhOH?")
            val = i
            break
        if map[py-i][px]==block:
            val = i
            #print(val)
            break
        if map[py-i][px]==prize:
            val=-1*i
            break
    distances.append(val)
        
    angles.reverse()
    xMult=1
    #Right Upper Raycast
    distances.extend(upperhalf(map,player,angles,xMult,block,prize,fog))
    #Middle Right Raycast
    val = 10
    for i in range(1,7):
            newPoint=(px+i*xMult,py-i)
            #print(map[newPoint[1]][newPoint[0]])
            if not withinMap(map,newPoint):
                val=math.dist((px,py),newPoint)
                break
            if map[newPoint[1]][newPoint[0]]==block:
                val = math.dist((px,py),newPoint)
                break
            if map[newPoint[1]][newPoint[0]]==prize:
                val=-1*i
                break
            if math.dist((px,py),newPoint) > fog:
                break
    distances.append(min(val,fog))
    #Bottom Right Raycast
    angles.reverse()
    distances.extend(lowerhalf(map,player,angles,xMult,block,prize,fog))
    #RightRaycast
    val = fog
    for i in range(1,fog+1):
        newPoint=(px+i*xMult,py)
        if not withinMap(map,newPoint):
            val=i
            break
        if map[newPoint[1]][newPoint[0]]==block:
            val=i
            break
        if map[newPoint[1]][newPoint[0]]==prize:
            val=-1*i
            break
    distances.append(min(val,fog))
    left = distances[0]
    mleft=distances[8]==1.4142135623730951
    up = distances[16]
    #print(up)
    mright = distances[24]==1.4142135623730951
    right = distances[32]
    #if left==1:
        #distances[1:8]=[1 for i in range(7)]
    for i in range(1,8):
        if left<=i:
            distances[1:9-i]=[left for j in range(8-i)]
            break
    for i in range(1,8):
        if up <=i:
            distances[8+i:16]=[up for j in range(8-i)]
            distances[17:25-i]=[up for j in range(8-i)]
            break
        
    for i in range(1,8):
        if right<=i:
            distances[24+i:32]=[up for j in range(8-i)]
            break
    #if right==1:
        #distances[25:32]=[1 for i in range(7)]
    return distances
def generate(map,direction,block="X",player="o",prize="░",width = 1, hieght=3,fog=10):
    multipliers = [1,1,1,1,2,2,3,3,3,4,4,4,5,6,8,10,12,10,8,6,5,4,4,4,3,3,3,2,2,1,1,1,1]
    #multipliers=[4 for i in range(33)]
    #print(len(multipliers),sum(multipliers))
    m = copy.deepcopy(map)
    #print(m)
    #print(player)
    if len(player) != 2:
        for y,i in enumerate(rotate(m,direction)):
            for x,j in enumerate(i):
                if j==player:
                    player = (x,y)
                    break
    #print("\n".join(["".join(i) for i in map]))
    d=raycast(player,map,direction,block,prize=prize,fog=fog)
    #print(len(d))
    #print(d)
    #print("Dadj")
    dAdj = [math.floor(i) for i in d]
    #print(direction)
    print(dAdj)
    out=""
    back=""
    gold=False
    for i in range(1,fog):
        line = ""
        #print(i)
        for pos,jj in enumerate(dAdj):
            if jj <0:
                gold = True
            else:
                gold=False
            if jj <= i:
                if not gold:
                    #print(multipliers[pos],end=",")
                    line+="░"*width*multipliers[pos]
                else:
                    line+="?"*width*multipliers[pos]
            else:
                line+=" "*width*multipliers[pos]
        for j in range(hieght):
            out+=line+"\n"
            back="\n"+line+back
    return out.strip("\n")+"".join(back)
            
if __name__=="__main__":
    map = """XXXXXXXXXXXXXXXXXXXX
X                  X
X                  X
X                  X
X          X       X
X          X       X
XX      XX       XXX
X       XoX       XX
XXX X   XX       XXX
X   X    X X X     X
X   XXXX X X X     X
X   XXX  X XX      X
X         XX       X
X                  X
X                  X
X                  X
X                  X
X                  X
X                  X
XXXXXXXXXXXXXXXXXXXX"""
    direction = "S"

    m=map.split("\n")
    
    m = [list(i) for i in m]
    #upMap = rotate(m,direction)
    for y,i in enumerate(m):
        for x,j in enumerate(i):
            if j=="o":
                player = (x,y)
                break
    #print(player)
    #print(len(m[0]))
    #mo  = copy.deepcopy(m)
    d=raycast(player,m,direction)
    print(d)
    print(len(d))
    print(d[16])
    #print(mo == m)
    #print(m[9][9])
    #g = generate(m,direction,"X","o")
    #print(g)
    #print(d)
    '''
    print("Left Raycast: ",d[0])
    print("Lower Left Raycast: ")
    for i in d[1:8]:
        print(i)
    print("MidLeft Raycast: ",d[8])
    print("Upper Left Raycast: ")
    for i in d[9:16]:
        print(i)
    print("Upper Raycast: ",d[16])
    print("Upper Right Raycast: ")
    for i in d[17:24]:
        print(i)
    print("MidRight Raycast:",d[24])
    print("Lower Right Raycast: ")
    for i in d[25:32]:
        print(i)
    #print("?",d[29])
    print("Right Raycast: ",d[32])
    print("ArrayLength:", len(d))
    position = (9,9)
    x,y=position'''
    '''print(y>=len(map) or y<0 or x<0 or x>=len(map[0]))
    print(x>=len(map[0]))
    print(len(map[0]))'''