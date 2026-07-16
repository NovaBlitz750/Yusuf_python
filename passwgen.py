import time 
import random
import string
def sp(text, delay=0.05):
    for char in text:
        print(char, end="" , flush=True)
        time.sleep(delay)
    print()
def sp2(text, delay=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()
def loop():
    sp("How many characters do you want your password to be?(reccomended 8+)")
    no=int(input(""))
    sp(f"Generating a password for you of {no} characters")
    if no<=7:
        sp2(f"Password is too weak, are you sure you want to proceed with a password with only {no} characters?(y/n)")
        ok=input("")
        if ok=="y":
            sp(f"Generating a password for you of {no} characters...")
            characters = string.ascii_letters + string.digits
            result = ''.join(random.choice(characters) for _ in range(no))
            sp(result)
    elif no>=15:
        sp2(f"Great!, but a password of {no} characters can be hard to remember, are you sure you want to proceed?(y/n)")
        ok1=input("")
        if ok1=="y":
            if ok=="y":
                sp(f"Generating a password for you of {no} characters...")
                characters = string.ascii_letters + string.digits
                result = ''.join(random.choice(characters) for _ in range(no))
                sp(result)
        else:
            loop()
sp("How many characters do you want your password to be?(reccomended 8+)")
no=int(input(""))
if no<=7:
    sp2(f"Password is too weak, are you sure you want to proceed with a password of only {no} characters?(y/n)")
    ok=input("")
    if ok=="y":
        sp(f"Generating a password for you of {no} characters...")
        characters = string.ascii_letters + string.digits
        result = ''.join(random.choice(characters) for _ in range(no))
        sp(result)
    else:
        loop()
elif no>=15:
        sp2(f"Great!, but a password of {no} characters can be hard to remember, are you sure you want to proceed?(y/n)")
        ok1=input("")
        if ok1=="y":
            if ok1=="y":
                sp(f"Generating a password for you of {no} characters...")
                characters = string.ascii_letters + string.digits
                result = ''.join(random.choice(characters) for _ in range(no))
                sp(result)
        else:
            loop()
else:
    sp(f"Generating a password for you of {no} characters...")
    time.sleep(3)
    characters = string.ascii_letters + string.digits
    result = ''.join(random.choice(characters) for _ in range(no))
    sp(result)