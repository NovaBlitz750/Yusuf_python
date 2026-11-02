import random
import time
def sp(text, delay=0.03):
    for character in text:
        print(character, end='', flush=True)
        time.sleep(delay)
    print()
def boathouse():
    sp("You enter the boathouse, what next?\n[1] Investigate locked cupboard\n[2] Pick up available items")
    boathouse_ask=input(" ")
    if boathouse_ask=="1":
        key_attempts=random.randint(1,10)
        for i in range(0,key_attempts):
            key_attempt=input("Press enter to try and open cupboard")
            if i<7:
                print("Attempt failed, try again")
        sp("Attempt successful")
def beach_explore():
    sp("You explore further along the beach...")

    beach_dice = random.randint(3,4)

    if beach_dice == 3 or beach_dice==4:
        sp("""
You notice a strange wooden building
near the shoreline...

ABANDONED BOATHOUSE!

Would you like to enter? (y/n)
""")

        enter = input(" ").strip().lower()

        if enter == "y" or enter == "yes":
            boathouse()
        else:
            sp("You leave the boathouse and continue exploring...")
    else:
        sp("You find some shells and driftwood along the shore.")
beach_explore()