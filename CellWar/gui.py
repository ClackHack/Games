import tkinter as tk
import random
rows,cols=25,25
ATTACK=0.2
NEW=0.4
LOWER=1
class Cell:
    def __init__(self,color,attack,defense,attackprob,king=False):
        self.color=color
        self.attack=attack
        self.defense=defense
        self.attackprob=attackprob
        self.original=self.defense
        self.king=king
    @staticmethod
    def generate():
        color = "#"+"%06x" % random.randint(0x333333, 0xDDDDDD)
        attack = random.randint(10,65)
        defense = random.randint(20,120)
        prob=random.uniform(0,0.5)
        return Cell(color,attack,defense,prob,king=True)
    def attackother(self,other,l):
        if other.color==self.color:
            return
        other.defense=other.defense-self.attack
        if other.defense < 1:
            self.defense=self.original
            other.color=self.color
            other.attack=max(5,self.attack-l)
            other.defense=max(10,self.defense-l)
            other.king=False
            other.attackprob=self.attackprob
            


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=500, height=500, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.rows = 120
        self.columns = 120
        self.cellwidth = 10
        self.cellheight = 10
        self.delay=200
        self.table=[]
        self.rect = {}
        self.oval = {}
        self.title("Cell War")
        for column in range(self.columns):
            for row in range(self.rows):
                x1 = column*self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="blue", tags="rect",outline="")
                self.oval[row,column] = self.canvas.create_oval(x1+2,y1+2,x2-2,y2-2, fill="blue", tags="oval",outline="")

        #self.redraw(1000)
        for i in range(self.rows):
            row=[]
            for i in range(self.columns):
                row.append(Cell.generate())
            self.table.append(row)
        self.update()
        self.step()
    def fill(self,row,col,cell):
        #self.canvas.itemconfig("rect", fill="blue")
        #self.canvas.itemconfig("oval", fill="blue")
        item_id = self.rect[row,col]
        self.canvas.itemconfig(item_id, fill=cell.color)
        if cell.king:
            item_id = self.oval[row,col]
            self.canvas.itemconfig(item_id, fill="black")
        else:
            item_id = self.oval[row,col]
            self.canvas.itemconfig(item_id, fill=cell.color)
        #self.after(delay, lambda: self.redraw(delay))
    def update(self):
        for i,ii in enumerate(self.table):
            for j,jj in enumerate(ii):
                self.fill(i,j,jj)
    def step(self):
        for i,ii in enumerate(self.table):
            for j,jj in enumerate(ii):
                #self.fill(i,j,jj.color)
                
                if random.uniform(0,1)<=jj.attackprob:
                    n = self.neighbors(i,j)
                    #print(n)
                    jj.attackother(random.choice(n),LOWER)
        if random.uniform(0,1)<=NEW:
            self.table[random.randint(0,self.rows-1)][random.randint(0,self.columns-1)]=Cell.generate()
        self.update()
        self.after(self.delay,self.step)
    def neighbors(self,r,c):
        ds = [[r,c+1],[r,c-1],[r+1,c],[r-1,c]]
        out=[]
        for i in ds:
            #print(i)
            if self.validpos(i[0],i[1]):
                #print("ad")
                out.append(self.table[i[0]][i[1]])
        return out
    def validpos(self,r,c):
        #print(r,c)
        #print(self.rows,self.columns)
        return (0 <= r < self.rows) and ( 0 <= c < self.columns)
def run():
    app = App()
    app.mainloop()
if __name__ == "__main__":
    run()