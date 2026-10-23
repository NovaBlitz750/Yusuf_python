import random
no= random.choice(1-100)
hts=3
gs=0
temp=3
ts=0
while temp>0:
    ty=input("Guess the number between 1 - 100, if you want a hint, press 0        Hints remaining:", hts)
    if ty==no:
        temp-=100
        print(f"Congrats! u correclty guessed the number({no}), you took{ts}tries to guess the number correctly")
    elif ty==0:
        print("")