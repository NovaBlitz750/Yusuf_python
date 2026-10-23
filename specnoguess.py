no=75
ts=0
gs=2
hs=4
h1="It is between 50 and 100"
h2="Its a multiple of 5"
h3="Its between 70 and 85"
while 0<gs:
    guess=int(input(f"Try to guess the number(its between 1 to 100). If you want a hint, press 0           Hints remaining: {hs-1} "))     
    if guess==no:
        gs-=100
        print("Congrats! u correclty guessed the number(75), you took", ts, "tries to guess the number correctly")
    elif guess==0:
        hs-=1
        if hs==0:
            print("You have already used your 3 hints")
            hs+=1
    elif guess<=80 and guess>=70:
        print("You are reallllllllly close! Take a hint next turn, you might get it! ")
        gs+=1
    else:
        gs+=1
        ts+=1
        print("No, the number isn't", guess)
    if hs==3:
        print(h1)
    elif hs==2:
        print(h2)
    elif hs==1:
        print(h3)