import random


phrases = open("words.txt",'r').read().split()
secret = random.choice(phrases)
#practice loops, break
#rock paper scissors
#Learn mod operator
#print syntax sep and end
#classes
#web scraping???
#basic web project


def draw(num):
    if num == 0:
        print('''__________''')
    elif num == 1:
        print('''
        
        
        
        |    
        |
        __________
        ''')
    elif num == 2:
        print('''
        |     
        |    
        |    
        |
        __________
        ''')
    elif num == 3:
        print('''
        _______
        |     
        |     
        |    
        |    
        |
        __________
        ''')
    elif num == 4:
        print('''
        _______
        |     |
        |     
        |    
        |    
        |
        __________
        ''')
    elif num == 5:
        print('''
        _______
        |     |
        |     O
        |    
        |    
        |
        __________
        ''')
    elif num == 6:
        print('''
        _______
        |     |
        |     O
        |     |
        |    
        |
        __________
        ''')
    
    elif num == 7:
        print('''
        _______
        |     |
        |     O
        |   _/|
        |    
        |
        __________
        ''')

    

    elif num == 8:
        print('''
        _______
        |     |
        |     O
        |   _/|\_
        |    
        |
        __________
        ''')

    elif num == 9:
        print('''
        _______
        |     |
        |     O
        |   _/|\_
        |    /
        |
        __________
        ''')

    elif num == 10:
        print('''
        _______
        |     |
        |     O
        |   _/|\_
        |    /\\
        |
        __________
        ''')
        


for i in range(len(secret)):
    if secret[i] == " ":
        print("      ", end=" ")
    else:
        print("_",end=" ")
print("")
complete = False
guessed = []
count = -1
n = 10
while not complete:
    if count >=n:
        complete = True
        print("You lose!!!")
        continue
    place = True
    for i in secret.lower():
        if i == " ": 
            continue
        if not i in guessed:
            
            place = False
    if place:
        print("You win!!!")
        complete = True
        continue
    count = count + 1
    print("You have "+ str(n-count)+ " guesses left...")
    
    let = input("\nLetter: ")
    if len(let) > 1:
        count = count-1
        print("Enter 1 letter at a time!")
        continue
    if not let in guessed:
        guessed.append(let.lower())
    else:
        print("You already entered that")
        draw(count)
        continue
    if let in secret.lower():
        count = count - 1
    else:
        draw(count)
    for i in secret:
        doesnt_match = True
        for b in guessed:
            if i.lower() ==b:
                print(i,end=" ")
                doesnt_match = False
        if doesnt_match and i != " ":
            print("_",end=" ")
        elif i == " ":
            print("      ",end= "")
    print("")
    print('Guessed: ')
    
    for i in guessed:
        print(i,end=' ')
    print("\n\n")
                
