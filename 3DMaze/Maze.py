from tkinter import *
import os
import math,time,datetime
import pickle
from colorama import Fore, Back, Style,init
#init(autoreset=True)
import generateImage
import random

# Easy to read representation for each cardinal direction.
N, S, W, E = ('n', 's', 'w', 'e')

class Cell(object):
    """
    Class for each individual cell. Knows only its position and which walls are
    still standing.
    """
    def __init__(self, x, y, walls):
        self.x = x
        self.y = y
        self.walls = set(walls)

    def __repr__(self):
        # <15, 25 (es  )>
        return '<{}, {} ({:4})>'.format(self.x, self.y, ''.join(sorted(self.walls)))

    def __contains__(self, item):
        # N in cell
        return item in self.walls

    def is_full(self):
        """
        Returns True if all walls are still standing.
        """
        return len(self.walls) == 4

    def _wall_to(self, other):
        """
        Returns the direction to the given cell from the current one.
        Must be one cell away only.
        """
        assert abs(self.x - other.x) + abs(self.y - other.y) == 1, '{}, {}'.format(self, other)
        if other.y < self.y:
            return N
        elif other.y > self.y:
            return S
        elif other.x < self.x:
            return W
        elif other.x > self.x:
            return E
        else:
            assert False

    def connect(self, other):
        """
        Removes the wall between two adjacent cells.
        """
        other.walls.remove(other._wall_to(self))
        self.walls.remove(self._wall_to(other))

class Maze(object):
    """
    Maze class containing full board and maze generation algorithms.
    """

    # Unicode character for a wall with other walls in the given directions.
    UNICODE_BY_CONNECTIONS = {'ensw': '┼',
                              'ens': '├',
                              'enw': '┴',
                              'esw': '┬',
                              'es': '┌',
                              'en': '└',
                              'ew': '─',
                              'e': '╶',
                              'nsw': '┤',
                              'ns': '│',
                              'nw': '┘',
                              'sw': '┐',
                              's': '╷',
                              'n': '╵',
                              'w': '╴'}

    def __init__(self, width=20, height=10):
        """
        Creates a new maze with the given sizes, with all walls standing.
        """
        self.width = width
        self.height = height
        self.cells = []
        for y in range(self.height):
            for x in range(self.width):
                self.cells.append(Cell(x, y, [N, S, E, W]))

    def __getitem__(self, index):
        """
        Returns the cell at index = (x, y).
        """
        x, y = index
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[x + y * self.width]
        else:
            return None

    def neighbors(self, cell):
        """
        Returns the list of neighboring cells, not counting diagonals. Cells on
        borders or corners may have less than 4 neighbors.
        """
        x = cell.x
        y = cell.y
        for new_x, new_y in [(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)]:
            neighbor = self[new_x, new_y]
            if neighbor is not None:
                yield neighbor

    def _to_str_matrix(self):
        """
        Returns a matrix with a pretty printed visual representation of this
        maze. Example 5x5:
        OOOOOOOOOOO
        O       O O
        OOO OOO O O
        O O   O   O
        O OOO OOO O
        O   O O   O
        OOO O O OOO
        O   O O O O
        O OOO O O O
        O     O   O
        OOOOOOOOOOO
        """
        str_matrix = [['O'] * (self.width * 2 + 1)
                      for i in range(self.height * 2 + 1)]

        for cell in self.cells:
            x = cell.x * 2 + 1
            y = cell.y * 2 + 1
            str_matrix[y][x] = ' '
            if N not in cell and y > 0:
                str_matrix[y - 1][x + 0] = ' '
            if S not in cell and y + 1 < self.width:
                str_matrix[y + 1][x + 0] = ' '
            if W not in cell and x > 0:
                str_matrix[y][x - 1] = ' '
            if E not in cell and x + 1 < self.width:
                str_matrix[y][x + 1] = ' '

        return str_matrix

    def __repr__(self):
        """
        Returns an Unicode representation of the maze. Size is doubled
        horizontally to avoid a stretched look. Example 5x5:
        ┌───┬───────┬───────┐
        │   │       │       │
        │   │   ╷   ╵   ╷   │
        │   │   │       │   │
        │   │   └───┬───┘   │
        │   │       │       │
        │   └───────┤   ┌───┤
        │           │   │   │
        │   ╷   ╶───┘   ╵   │
        │   │               │
        └───┴───────────────┘
        """
        # Starts with regular representation. Looks stretched because chars are
        # twice as high as they are wide (look at docs example in
        # `Maze._to_str_matrix`).
        skinny_matrix = self._to_str_matrix()

        # Simply duplicate each character in each line.
        double_wide_matrix = []
        for line in skinny_matrix:
            double_wide_matrix.append([])
            for char in line:
                double_wide_matrix[-1].append(char)
                double_wide_matrix[-1].append(char)

        # The last two chars of each line are walls, and we will need only one.
        # So we remove the last char of each line.
        matrix = [line[:-1] for line in double_wide_matrix]

        def g(x, y):
            """
            Returns True if there is a wall at (x, y). Values outside the valid
            range always return false.
            This is a temporary helper function.
            """
            if 0 <= x < len(matrix[0]) and 0 <= y < len(matrix):
                return matrix[y][x] != ' '
            else:
                return False

        # Fix double wide walls, finally giving the impression of a symmetric
        # maze.
        for y, line in enumerate(matrix):
            for x, char in enumerate(line):
                if not g(x, y) and g(x - 1, y):
                    matrix[y][x - 1] = ' '

        # Right now the maze has the correct aspect ratio, but is still using
        # 'O' to represent walls.

        # Finally we replace the walls with Unicode characters depending on
        # their context.
        for y, line in enumerate(matrix):
            for x, char in enumerate(line):
                if not g(x, y):
                    continue

                connections = set((N, S, E, W))
                if not g(x, y + 1): connections.remove(S)
                if not g(x, y - 1): connections.remove(N)
                if not g(x + 1, y): connections.remove(E)
                if not g(x - 1, y): connections.remove(W)

                str_connections = ''.join(sorted(connections))
                # Note we are changing the matrix we are reading. We need to be
                # careful as to not break the `g` function implementation.
                matrix[y][x] = Maze.UNICODE_BY_CONNECTIONS[str_connections]

        # Simple double join to transform list of lists into string.
        return '\n'.join(''.join(line) for line in matrix) + '\n'

    def randomize(self):
        """
        Knocks down random walls to build a random perfect maze.
        Algorithm from http://mazeworks.com/mazegen/mazetut/index.htm
        """
        cell_stack = []
        cell = random.choice(self.cells)
        n_visited_cells = 1

        while n_visited_cells < len(self.cells):
            neighbors = [c for c in self.neighbors(cell) if c.is_full()]
            if len(neighbors):
                neighbor = random.choice(neighbors)
                cell.connect(neighbor)
                cell_stack.append(cell)
                cell = neighbor
                n_visited_cells += 1
            else:
                cell = cell_stack.pop()

    @staticmethod
    def generate(width=20, height=10):
        """
        Returns a new random perfect maze with the given sizes.
        """
        m = Maze(width, height)
        m.randomize()
        return m
                    

clear = lambda:os.system("cls")
hard=input("Hard (y/n): ").lower()=="y"
radius=8
generate=True
leaderboard=False
cheats= True
goal =False
if leaderboard:
    h = 10
    w =  20
else: 
    h = int(input("Hieght: "))
    w= int(input("Width: "))
moves=0
if generate:
    m=Maze.generate(w,h)
    m=m._to_str_matrix()
    place = []
    for i in m:
        place.append(''.join(i).replace("O","#").replace(" ","."))
    m=place
    del place
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == ".":
                p=[j,i]
    while 1:
        tx = random.randint(0,w-1)
        ty= random.randint(0,h-1)
        if m[ty][tx] ==".":
            place = list(m[ty])
            place[tx] = "▓"
            place = "".join(place)
            m[ty]=place
            del place
            break
        else:
            continue
        
else:
    
    m=[]
    map = """XXXXXXXXXXXXXXXXXXXX
X                  X
X                  X
X                  X
X          X       X
X          X       X
XXXXXXXXXXXXXXXXXXXX
X X X  X o X X X  XX
XXX X XX X X X X XXX
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
    direction = "W"

    m=map.split("\n")
    
    ma = [list(i) for i in m]
    upMap = generateImage.rotate(ma,direction)
    for y,i in enumerate(upMap):
        for x,j in enumerate(i):
            if j=="o":
                player = (x,y)
                break
    p=player
def win():
    main.quit()
    clear()
    y=datetime.datetime.now()
    td=(y-begin).total_seconds()
    print(h,"x",w)
    print(f"You Win in {moves} moves!")
    print("Solved in",td,"seconds!")
    if leaderboard:
        try:
            with open("MazeLeaderBoard.txt","rb") as f:
                leader = pickle.load(f)
        except:
            pass
        for i in  range(len(leader)):
            if td < leader[i]:
                leader.insert(i,td)
                leader.pop()
                print("You made the leaderboard!")
                break
        with open("MazeLeaderBoard.txt","wb") as f:
            pickle.dump(leader,f)
        for i in range(1,6):
            print(f"{i}. {leader[i-1]}")
    print("Press q to exit...")
    input()
def printScreenOld(m,p):
    #global hard\
    hard=True
    if hard:
        for i in range(len(m)):
            for j in range(len(m[i])):
                if [j,i] == p:
                    print("@",end="")
                elif int(math.dist(p,[j,i])) <= radius:
                    if m[i][j] == "▓":
                        print(Fore.YELLOW+"▓",end="")
                        print(Style.RESET_ALL,end="")
                    else:
                        print(m[i][j],end="")
                else:
                    if goal and m[i][j]=="▓":
                        print("▓",end="")
                    else:
                        print(" ",end="")
               
            print()
    else:
        for i in range(len(m)):
            for j in range(len(m[i])):
                if [j,i] == p:
                    print("@",end="")
                else:
                    print(m[i][j],end="")
            print()    
def printScreen(m,p):
    global hard,direction
    clear()
    mapToPass = [list(i) for i in m]
    #print(mapToPass[0])
    
    print()
    print(generateImage.generate(mapToPass,direction,"#",p,1,2,radius))
    print("\n",direction,"\n")
    if not hard:
        printScreenOld(m,p)
def checkWall(m,l):
    if m[l[1]][l[0]] == "#":
        return False
    elif m[l[1]][l[0]] == "▓":
        win()
    else:
        return True
def game(move):
    global moves,direction
    moves+=1
    global m
    global p
    if move == "left":
        direction = list("NESW")[(list("NESW").index(direction)-1) %4]
        printScreen(m,p)
    elif move=="right":
        #print(list("NESW").index(direction)+1 %4)
        direction = list("NESW")[(list("NESW").index(direction)+1) %4]
        printScreen(m,p)
    elif move =="up":
        if direction == "N":
            if checkWall(m,[p[0],p[1]-1]):
                p = [p[0],p[1]-1]
        if direction == "S":
                if checkWall(m,[p[0],p[1]+1]):
                    p = [p[0],p[1]+1]
        if direction == "E":
                if checkWall(m,[p[0]+1,p[1]]):
                    p = [p[0]+1,p[1]]
        if direction == "W":
                if checkWall(m,[p[0]-1,p[1]]):
                    p = [p[0]-1,p[1]]
        printScreen(m,p)
    elif move == "down":
        if direction == "S":
            if checkWall(m,[p[0],p[1]-1]):
                p = [p[0],p[1]-1]
        if direction == "N":
                if checkWall(m,[p[0],p[1]+1]):
                    p = [p[0],p[1]+1]
        if direction == "W":
                if checkWall(m,[p[0]+1,p[1]]):
                    p = [p[0]+1,p[1]]
        if direction == "E":
                if checkWall(m,[p[0]-1,p[1]]):
                    p = [p[0]-1,p[1]]
        printScreen(m,p)
main = Tk()
direction = "N"
if leaderboard:
    cheats=False
 
def left(event):
    game("left")

def right(event):
    game("right")
def up(event):
    game("up")
def down(event):
    game("down")
def q(event):
    import sys;sys.exit()
if cheats:
    def l(event):
        mapToPass = [list(ii) for ii in m]
        print(p)
        print(generateImage.raycast(p,mapToPass,direction,"#"))
        print(direction)
    def r(event):
        mapToPass = generateImage.rotate([list(ii) for ii in m],direction)

        print("\n".join([' '.join(i) for i in mapToPass]))
    def g(event):
        global goal
        if goal:
            goal=False
        else:
            goal=True

main.bind('<Left>', left)
main.bind('<Right>', right)
main.bind("<Up>",up)
main.bind("<Down>",down)
main.bind('a', left)
main.bind('d', right)
main.bind("w",up)
main.bind("s",down)
main.bind("q",q)
if cheats:
    main.bind("l",l)
    main.bind("r",r)
    main.bind("g",g)
#main.withdraw()
print("Welcome to pyMaze!\nPress q to quit at anytime!\n")
begin = datetime.datetime.now()
time.sleep(1.5)
print(m)
#clear()
printScreen(m,p)
main.mainloop()

