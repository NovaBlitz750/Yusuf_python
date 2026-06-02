import random
no= random.randint (1,50)
lives =5
print(no)
while lives>=1:
    gs=int(input("\nTry to guess the secret no."))
    if gs==no:
        print("You guessed the secret no, correctly!")
    elif gs in range(no-10,no+10):
        print("🔥 Hot")
        lives-=1
    elif gs in range(no-5,no+25):
        print("🌡️ Warm")
        lives-=1
    elif gs in range(no-35,no+35):
        print("🥶 cold")
        lives-=1
    else:
        print("🧊 Ice cold")
        lives-=1
    for i in range(0,lives):
        print("❤️ ", end="")
print("GameOver")