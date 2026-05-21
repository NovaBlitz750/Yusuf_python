import random
import time
would_you_rathers = [
    "Would you rather be able to fly or be invisible?", "Would you rather fight 100 duck-sized horses or 1 horse-sized duck?",
    "Would you rather have the ability to teleport or the ability to read minds?",
    "Would you rather live without music or without movies?",
    "Would you rather have a pause button for your life or a rewind button for your life?",
    "Would you rather be able to talk to animals or speak all human languages?",
    "Would you rather have super strength or super speed?",
    "Would you rather have the ability to breathe underwater or fly?",
    "Would you rather be able to control fire or water?",
    "Would you rather live in a world without technology or a world without nature?"
]

def play_again():
    p = "y"
    while p == "y":
        ty = random.choice(would_you_rathers)
        print(ty)
        p = input("Play again? (y/n)")

ty = random.choice(would_you_rathers)
def slow_print(text, delay=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()
slow_print(ty)
play_again()