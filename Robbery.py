import random
import pickle
class Player (object):
    def __init__(self):
        self.money = float(random.randint(1,6)*100)
        self.stuff = []
        self.damage=1
        self.hp = 100
    def buy(self,money):
        self.money -= money
    def setWeapon(self,w):
        self.damage += w[2]
    def addHp(self,val):
        self.hp+=val
p = Player()
print("You have $"+str(p.money))
armory = {"Kevlar":[300.0,"a",75],"Shotgun":[200.0,"w",13],"Pistol":[100.0,"w",9],"AK-47":[400.0,"w",20],"Helmet":[100.0,"a",30],"Crowbar":[30.0,"w",3],"Bandages":[20.0,"s",25]}
sentence=20
hasWeapon = False
while 1:
    print()
    found=False
    for i,j in armory.items():
        print(f"%8s ....... $%.2f"%(i,j[0]))
    print("You have $"+str(p.money))
    print("Press Enter to Leave...")
    item = input("Buy: ")
    if item =="":
        break
    for i,j in armory.items():
        if item.lower() in i.lower():
            found = True
            print(f"%8s ....... $%2.f"%(i,j[0]))
            if p.money >= j[0]:
                if not hasWeapon and j[1]=='w':
                    print("Bought!")
                    hasWeapon = True
                    p.buy(j[0])
                    p.stuff.append(i)
                    p.setWeapon(j)
                elif j[1] in "a":
                    print("Bought!")
                    p.buy(j[0])
                    p.stuff.append(i)
                    p.addHp(j[2])
                elif j[1] in "s":
                    print("Bought!")
                    p.buy(j[0])
                    p.stuff.append(i) 
                    
                elif j[1]=="w":
                    print("You already have a weapon")
            else:
                print("You do not have enough money!")
            break
    if not found:
        print("Item not found...")
if True:
    print("You Burst into the bank Guns Blazing")
    numCops = random.randint(1,3)
    copHp = 80
    print("There are",numCops,"cops!")
    hasShot = False
    lose = False
    while 1:
        print()
        print(f"Hp: {p.hp}")
        print("Press a to attack\nPress h to heal\nPress s to surrender")
        i = input().lower()
        if i=="s":
            lose = True
            if hasShot:
                print("You stand up to surrender, and an injured cop shoots you twice")
                roll = random.choice([1,0])
                if roll:
                    print("You bleed out on the floor, your family does not attend your funeral...")
                    break
                else:
                    print("You are taken to the hospital, and then prison...")
                    break
            else:
                print("An angry judge gives you 45 in maximum security prison...")
                break
        elif i=="h":
            try:
                pos = p.stuff.index("Bandages")
                del p.stuff[pos]
                p.hp += random.randint(5,20)
                continue
            except:
                print("You dont have any bandages")
                continue
        elif i =="a":
            hasShot=True
            damage = int(random.uniform(0.75,1.25) * p.damage)
            copHp -= damage
            print("You Did",damage,"damage")
            intake = random.randint(10,23)
            print("You took",intake,"damage")
            p.hp-=intake
            if p.hp <=0:
                print("Bullet ridden, you bleed out on the floor")
                lose=True
                break
            if copHp < 0:
                print()
                print("You Killed a cop!")
                sentence+=10
                numCops-=1
                if numCops==0:
                    break
    if lose:
        print("You lose!")
        exit()
    lose=False
    v= input("Press v to go for the vault\nPress t to go for the teller\n")
    if v == "v":
        print("You Run for the backroom")
        while 1:
            print("Press s to stay for money\nPress l to leave")
            i = input()
            if i == "s":
                money = random.randint(300,600)
                p.money+=money
                print(f"You made ${money}")
                roll = random.randint(1,3)
                sentence +=1
                if roll ==1:
                    print("The cops roll up, your surrounded")
                    print("Press r to run\nPress s to surrender")
                    x = input()
                    if x =="s":
                        print(f"Your arrested, convicted, and sentenced to {sentence} years")
                        lose=True
                        break
                    elif x == "r":
                        roll = random.randint(1,6)
                        if roll != 1:
                            print("You are shot and killed, your funeral is a closed casket because your bullet ridden body costs too much to be made recognizable...")
                            lose=True
                            break
                        else:
                            print("You-you made it. Well your bleeding, badly, but you made it!")
                            break
            if i == "l":
                print("You Roll up just in time to evade the cops")
                break
    if v =="t":
        print("You Stroll up to the teller and ask for some money!")
        scare = False
        if hasWeapon:
            print("You put your weapon on the desk for extra intimidation!")
            num = random.randint(0,14)
            if p.damage > num:
                scare = True
                print('It Worked!')
            p.money += random.randint(300,900)+int(scare)*500
            print("You Grab the money and run...")
    if lose:
        print("You lose")
        exit()
clean = random.choice([False,True])
def win():    
    global p
    print("You made $",p.money,sep="")
    with open("RobberyLeaderboard.txt","rb") as f:
        leader = pickle.load(f)
    for i in  range(len(leader)):
        if p.money > leader[i]:
            leader.insert(i,p.money)
            leader.pop()
            print("You made the leaderboard!")
            break
    with open("RobberyLeaderboard.txt","wb") as f:
        pickle.dump(leader,f)
    for i in range(1,6):
        print(f"{i}. ${leader[i-1]}")      
if clean:
    print("You made it away... cleanly, and are now at the safehouse")
    win()
else:
    print("You driving away and, your being followed!")
    print()
    print("Press e to evade\nPress f to fight")
    i = input()
    if i =="e":
        roll = random.randint(1,6)
        if roll <=2:
            print("You made it out safely!")
            win()
        else:
            print("After countless pleas from the police, you are shot and lose control of the wheel. You die in a firey crash")
            print("You lose!")
            exit()
    if i == "f":
        print("While trying to aim your weapon you crash into a tree")
        print("You are pulled from the car, and arrested!")
        print("You lose!")
        
