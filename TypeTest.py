import random,datetime,time
while 1:
    sentence = "hello, this is a test to count your wpm"
    print("Get ready to type!")
    time.sleep(1)
    print("Ready!")
    time.sleep(1)
    print("Set!")
    time.sleep(1)
    print("GO!!!")
    print(sentence)
    y = datetime.datetime.now()
    words=input()
    x=datetime.datetime.now()
    seconds = (x-y).total_seconds()
    w = words.split(" ")
    wpm = int(len(w) / seconds * 60)
    s = sentence.split(" ")
    correct = 0
    total = 0
    for i in sentence:
        if i ==" ":
            continue
        else:
            total +=1
    for i in range(len(s)):
        try:
            guess = w[i]
        except:
            break
        for j in range(len(s[i])):
            try:
                if guess[j] == s[i][j]:
                    correct+=1
            except:
                break
    accuracy = correct / total
    print("WPM: ",wpm)
    print("Accuracy",round(accuracy,2))
    break
    
