import random
score=0
score2=0
score3=0
score4=0
no=int(input("Enter the number of players playing(1-4 only)"))
if no==1:
    while score<100:
        roll=input("P1,Enter r to roll")
        if roll=="r" or roll=="R":
            try:
                dice=random.randint(1,6)
                snakes=[random.randint(1, 100) for _ in range(5)]
                snakeloss=random.randint(1,25)
                ladders=[random.randint(1,30) for _ in range(5)]
                if score in snakes:
                    score-=snakeloss
                    print("A snake caught you!, your score is now", score)
                elif score in ladders:
                 print("You got a ladder! your score is now", score)
                else:
                    score+=dice
                    print("Your number is", dice, "and your score is", score)
            except ValueError:
                print("nothing")
elif no==2:
    while score<100 or score2<100 and n%2 !=0:
        roll=input("P1,Enter r to roll")
        n=0
        if roll=="r" or roll=="R" and n%2 !=0:
            try:
                dice=random.randint(1,6)
                snakes=[random.randint(1, 100) for _ in range(5)]
                snakeloss=random.randint(1,25)
                ladders=[random.randint(1,30) for _ in range(5)]
                if score in snakes:
                    score-=snakeloss
                    print("A snake caught you!, your score is now", score)
                elif score in ladders:
                 print("You got a ladder! your score is now", score)
                else:
                    score+=dice
                    print("Your number is", dice, "and your score is", score)
                n+=1
            except ValueError:
                print("nothing")
        elif roll=="r" or roll=="R" and n%2 ==0:
            try:
                dice=random.randint(1,6)
                snakes=[random.randint(1, 100) for _ in range(5)]
                snakeloss=random.randint(1,25)
                ladders=[random.randint(1,30) for _ in range(5)]
                if score2 in snakes:
                    score2-=snakeloss
                    print("A snake caught you!, your score is now", score2)
                elif score2 in ladders:
                 print("You got a ladder! your score is now", score2)
                else:
                    score2+=dice
                    print("Your number is", dice, "and your score is", score2)
                n+=1
            except ValueError:
                print("nothing")
            n+=1
    while score<100 or score2<100 and n%2==0:
        roll=input("P2,Enter r to roll")
        n=0
        if roll=="r" or roll=="R" and n%2 !=0:
            try:
                dice=random.randint(1,6)
                snakes=[random.randint(1, 100) for _ in range(5)]
                snakeloss=random.randint(1,25)
                ladders=[random.randint(1,30) for _ in range(5)]
                if score in snakes:
                    score-=snakeloss
                    print("A snake caught you!, your score is now", score)
                elif score in ladders:
                 print("You got a ladder! your score is now", score)
                else:
                    score+=dice
                    print("Your number is", dice, "and your score is", score)
                n+=1
            except ValueError:
                print("nothing")
        elif roll=="r" or roll=="R" and n%2 ==0:
            try:
                dice=random.randint(1,6)
                snakes=[random.randint(1, 100) for _ in range(5)]
                snakeloss=random.randint(1,25)
                ladders=[random.randint(1,30) for _ in range(5)]
                if score2 in snakes:
                    score2-=snakeloss
                    print("A snake caught you!, your score is now", score2)
                elif score2 in ladders:
                 print("You got a ladder! your score is now", score2)
                else:
                    score2+=dice
                    print("Your number is", dice, "and your score is", score2)
                n+=1
            except ValueError:
                print("nothing")
            n+=1