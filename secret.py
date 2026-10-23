import time

def sp(text, delay=0.05): # Increased default delay slightly so you can actually see it print slow
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # Adds a final newline at the end


name=input("Enter ur name: ")
no=int(input("Whats ur favourite number: "))

if name.strip().capitalize()=="Yusuf":
    print("Ur name isnt Yusuf u stupid piece of shit, write ur own name dumbass")
elif name.strip().capitalize()=="Yichen":
    print("Ur name isnt Yichen u stupid piece of shit, write ur own name u dumbass")
elif name.strip().capitalize()=="Charlie":
    ap=input("I don't wanna do ts Charlie, are u sure u wanna proceed? (y/n): ")
    if "y" in ap or "Y" in ap:
        for i in range(0, no): # Changed to 'no' so it loops exactly the number of times requested
            sp(f"{i} {name} is a stupid piece of shit") # Used an f-string to combine text
            sp(f"{i} {name} is a fucking dumbass")
    else:
        print("Good choice bro")
else:
    for i in range(0, no):
        sp(f"{i} {name} is a stupid piece of shit")
        sp(f"{i} {name} is a fucking dumbass")
