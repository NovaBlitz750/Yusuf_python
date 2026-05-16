import time
import getpass
guessed= []
def sp(text, delay=0.05):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()
def sp1(text, delay=0.09):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()
sp("Enter a word for your friend to guess")
word=input("")
print ("\n"*50)
i=8
while i>1:
    for letter in word:
        if letter in guessed:
            print(letter, end=" ")
        else:
            print("_", end=" ")
    print()
    guess=input("Guess a letter in the word")
    if guess in word:
        guessed.append(guess)
        sp("Correct letter guessed!")
        if all(letter in guessed for letter in word):
            sp("You guessed the word!")
            break
    else:
        i-=1
        sp("Wrong letter guessed")
    if i==7:
        print("----")
        print("|  I")
        print("I")
    elif i==6:
        print("----")
        print("I  I")
        print("I  O")
        print("I")
    elif i==5:
        print("----")
        print("|  |")
        print("|  O")
        print("|  l")
        print("|")
    elif i==4:
        print("----")
        print("|  |")
        print("|  O")
        print("|  l")
        print("|   )")
        print("|")
    elif i==3:
        print("----")
        print("|  |")
        print("|  O")
        print("|  l")
        print("| ( ) ")
        print("|")
    elif i==2:
        print("----")
        print("|  |")
        print("|  O")
        print("|  l")
        print("| ( ) ")
        print("|    }")
        print("|")
    elif i==1:
        print("----")
        print("|  |")
        print("|  O")
        print("|  l")
        print("| ( ) ")
        print("| { }")
        print("|")
        sp1("Game Over!")
        break