import random
score=0
while score<100:
    roll=input("Enter r to roll")
    if roll=="r" or roll=="R":
        try:
            dice=random.randint(1,6)
            snakes=[random.randint(1, 100) for _ in range(5)]
            snakeloss=random.randint(1,25)
            ladders=[random.randint(1,30) for _ in range(5)]
   # roll=input(f"Your number is {dice}, and your score is {score}")
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