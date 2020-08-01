import random
usage= "etaoinsrhdlucmfywgpbvkxqjz"
words = open("words.txt","r").read().split()
temp = []
print("Welcome to hangman!\nThe computer will guess! \nRules are you must pick an english word")
length = int(input("What is the length of your word?: "))
for i in words:
    if len(i) == length and not "-" in i:
        temp.append(i.lower())
lives = 6
words = temp
temp = []
print(len(words))
guessed = []
word = ["" for i in range(length)]
def guess(letter):
    x = input("Is '"+letter+"' your word? (y/n): ")
    if x.lower() == "y":
        x = input("What position(s) is '"+letter+"' at? (Start at index 1): ")
        x=x.split()
        x = [int(i) -1 for i in x]
        return x
    elif x.lower() == "n":
        return []
def printlives(lives):
    for i in range(lives): 
        print("♥",end="")


while "" in word:
   if lives <=0:
      break
   if len(words) == 0:
       print("You sure you put in an english word?")
       import sys
       sys.exit()
   if len(words) == 1:
       print("Is",words[0],"your word? (y/n): ")
       x = input()
       if x.lower() == "y":
           lives = 1
           break
       else:
           lives = 0
           print("Not sure thats an english word but ok...")
           break
   letterprob = {}
   empty = []
   for i in range(len(word)):
       if word[i] == "":
           empty.append(i)
   for i in words:
        for j in empty:
            if i[j].lower() in guessed:
                continue
            elif i[j].lower() in letterprob.keys():
                letterprob[i[j].lower()] = letterprob[i[j].lower()]+1

            else:
                letterprob[i[j].lower()] = 1
   maxletter=""
   maxnum=0
   for i,j in letterprob.items():
       if j > maxnum:
           maxletter = i
           maxnum = j
   guessed.append(maxletter)
   g = guess(maxletter)
   for i in g:
       word[i] = maxletter
   if g:
      for i in words:
           works = True
           for j in g:
               if i[j] != maxletter:
                   works = False
           for j in range(len(i)):
               if j in g:
                   continue
               else:
                   if i[j] == maxletter:
                      works = False
           if works:
                temp.append(i)
      words = temp
      temp = []
   else:
      lives -=1
      for i in words:
            if not maxletter in i:
                temp.append(i)
      words = temp
      temp = []
   print("Possible Words: ",len(words))
   for i in word:
       if i == "":
           print("_",end=" ")
       else:
           print(i,end=" ")
   print()
   printlives(lives)
   print("\n")
if lives <=0:
    print("You win, you have bested me")
else:
    print("HAHA, I win! Try again if you dare!")
