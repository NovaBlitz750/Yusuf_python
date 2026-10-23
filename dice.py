import time
import random
num=[1,2,3,4,5,6]
def sp(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()
sp("Rolling dice...")
time.sleep(1)

no=random.choice(num)
if no==1:
    print("     ")
    print("  .  ")
    print("     ")
    print("\nYour number is", no)
if no==2:
    print(" .   ")
    print("     ")
    print("    .")
    print("\nYour number is", no)
if no==3:
    print("   . ")
    print("  .  ")
    print(".    ")
    print("\nYour number is", no)
if no==4:
    print(".   .")
    print("     ")
    print(".   .")
    print("\nYour number is", no)
if no==5:
    print(".   .")
    print("  .  ")
    print(".   .")
    print("\nYour number is", no)
if no==6:
    print(".   .")
    print(".   .")
    print(".   .")
    print("\nYour number is", no)