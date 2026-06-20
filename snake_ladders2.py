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
    while score<100 and score2<100:
        roll=input("P1,Enter r to roll dice")
        n=0
        if roll=="r" or roll=="R":
            try:
                dice=random.randint(1,6)
                dice2=random.randint(1,6)
                snakes=[random.randint(1, 100) for _ in range(5)]
                snakeloss=random.randint(1,25)
                ladders=[random.randint(1,30) for _ in range(5)]
                if score in snakes:
                    score-=snakeloss
                    print("A snake caught you! P1 score is now", score)
                    print("P1 score=", score)
                    print("P2 score=", score2)
                elif score in ladders:
                    print("You got a ladder! P1 score is now", score)
                    print("P1 score=", score)
                    print("P2 score=", score2)
                else:
                    score+=dice
                    print("Your number is", dice,)
                    print("P1 score=", score)
                    print("P2 score=", score2)
            except ValueError:
                print("idk")
        roll2=input("P2,Enter r to roll dice")
        if roll2=="R" or "r":
            if score2 in snakes:
                    score2-=snakeloss
                    print("A snake caught you! P2 score is now", score2)
                    print("P1 score=", score)
                    print("P2 score=", score2)
            elif score2 in ladders:
                print("You got a ladder! P2 score is now", score2)
                print("P1 score=", score)
                print("P2 score=", score2)
            else:
                    score2+=dice2
                    print("Your number is", dice2,)
                    print("P1 score=", score)
                    print("P2 score=", score2)
    while score>=100:
        print("P1 wins!")
        break
    while score2>=100:
        print("P2 wins!")
        break
elif no==3:
    while score>=100:
        print("P1 wins!")
        break
    while score2>=100:
        print("P2 wins!")
        break
    while score3>=100:
        print("P3 wins!")
        break
    while score<100 and score2<100 and score3<100:
        roll=input("P1,Enter r to roll dice")
        n=0
        if roll=="r" or roll=="R":
            try:
                dice=random.randint(1,6)
                dice2=random.randint(1,6)
                dice3=random.randint(1,6)
                snakes=[random.randint(1, 100) for _ in range(5)]
                snakeloss=random.randint(1,25)
                ladders=[random.randint(1,30) for _ in range(5)]
                if score in snakes:
                    score-=snakeloss
                    print("A snake caught you! P1 score is now", score)
                    print("P1 score=", score)
                    print("P2 score=", score2)
                    print("P3 score=", score3)
                elif score in ladders:
                    print("You got a ladder! P1 score is now", score)
                    print("P1 score=", score)
                    print("P2 score=", score2)
                    print("P3 score=", score3)
                else:
                    score+=dice
                    print("Your number is", dice,)
                    print("P1 score=", score)
                    print("P2 score=", score2)
                    print("P3 score=", score3)
            except ValueError:
                print("idk")
        roll2=input("P2,Enter r to roll dice")
        if roll2=="R" or "r":
            if score2 in snakes:
                    score2-=snakeloss
                    print("A snake caught you! P2 score is now", score2)
                    print("P1 score=", score)
                    print("P2 score=", score2)
                    print("P3 score=", score3)
            elif score2 in ladders:
                print("You got a ladder! P2 score is now", score2)
                print("P1 score=", score)
                print("P2 score=", score2)
                print("P3 score=", score3)
            else:
                    score2+=dice2
                    print("Your number is", dice2,)
                    print("P1 score=", score)
                    print("P2 score=", score2)
                    print("P3 score=", score3)
        roll3=input("P3,Enter r to roll")
        if roll3=="R" or "r":
            if score3 in snakes:
                score3-=snakeloss
                print("A snake caught you! P3 score is now", score3)
                print("P1 score=", score)
                print("P2 score=", score2)
                print("P3 score=", score3)
            elif score3 in ladders:
                print("You got a ladder! P3 score is now", score3)
                print("P1 score=", score)
                print("P2 score=", score2)
                print("P3 score=", score3)
            else:
                score3+=dice
                print("Your number is", dice3,)
                print("P1 score=", score)
                print("P2 score=", score2)
                print("P3 score=", score3)
elif no==4:

    while score<100 and score2<100 and score3<100 and score4<100:
        roll=input("P1,Enter r to roll dice")
        n=0
        if roll=="r" or roll=="R":
            try:
                dice=random.randint(1,6)
                dice2=random.randint(1,6)
                dice3=random.randint(1,6)
                dice4=random.randint(1,6)
                snakes=[random.randint(1, 100) for _ in range(5)]
                snakeloss=random.randint(1,25)
                ladders=[random.randint(1,30) for _ in range(5)]
                if score in snakes:
                    score-=snakeloss
                    print("A snake caught you! P1 score is now", score)
                    print("P1 score=", score)
                    print("P2 score=", score2)
                    print("P3 score=", score3)
                    print("P4 score=", score4)
                elif score in ladders:
                    print("You got a ladder! P1 score is now", score)
                    print("P1 score=", score)
                    print("P2 score=", score2)
                    print("P3 score=", score3)
                    print("P4 score=", score4)
                else:
                    score+=dice
                    print("Your number is", dice,)
                    print("P1 score=", score)
                    print("P2 score=", score2)
                    print("P3 score=", score3)
                    print("P4 score=", score4)
            except ValueError:
                print("idk")
        roll2=input("P2,Enter r to roll dice")
        if roll2=="R" or "r":
            if score2 in snakes:
                    score2-=snakeloss
                    print("A snake caught you! P2 score is now", score2)
                    print("P1 score=", score)
                    print("P2 score=", score2)
                    print("P3 score=", score3)
                    print("P4 score=", score4)
            elif score2 in ladders:
                print("You got a ladder! P2 score is now", score2)
                print("P1 score=", score)
                print("P2 score=", score2)
                print("P3 score=", score3)
                print("P4 score=", score4)
            else:
                    score2+=dice2
                    print("Your number is", dice2,)
                    print("P1 score=", score)
                    print("P2 score=", score2)
                    print("P3 score=", score3)
                    print("P4 score=", score4)
        roll3=input("P3,Enter r to roll")
        if roll3=="R" or "r":
            if score3 in snakes:
                score3-=snakeloss
                print("A snake caught you! P3 score is now", score3)
                print("P1 score=", score)
                print("P2 score=", score2)
                print("P3 score=", score3)
                print("P4 score=", score4)
            elif score3 in ladders:
                print("You got a ladder! P3 score is now", score3)
                print("P1 score=", score)
                print("P2 score=", score2)
                print("P3 score=", score3)
                print("P4 score=", score4)
            else:
                score3+=dice3
                print("Your number is", dice3,)
                print("P1 score=", score)
                print("P2 score=", score2)
                print("P3 score=", score3)
                print("P4 score=", score4)
        roll4=input("P4,Enter r to roll")
        if roll4=="R" or "r":
            if score4 in snakes:
                score4-=snakeloss
                print("A snake caught you! P4 score is now", score4)
                print("P1 score=", score)
                print("P2 score=", score2)
                print("P3 score=", score3)
                print("P4 score=", score4)
            elif score4 in ladders:
                print("You got a ladder! P4 score is now", score4)
                print("P1 score=", score)
                print("P2 score=", score2)
                print("P3 score=", score3)
                print("P4 score=", score4)
            else:
                score4+=dice4
                print("Your number is", dice4,)
                print("P1 score=", score)
                print("P2 score=", score2)
                print("P3 score=", score3)
                print("P4 score=", score4)
    while score>=100:
        print("P1 wins!")
        break
    while score2>=100:
        print("P2 wins!")
        break
    while score3>=100:
        print("P3 wins!")
        break
    while score4>=100:
        print("P4 wins!")
        break
