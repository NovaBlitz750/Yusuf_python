```python
import random
import time

\
choices=[]
inventory={}
possibilities_for_entering=["1","2","3"]
entered=0
new_branches=random.randint(1,10)

def sp(text, delay=0.03):
    for character in text:
        print(character, end='', flush=True)
        time.sleep(delay)
    print()

def pi():
    print("Inventory:",inventory)

def new_explore(new_branches):
    sp("You notice some fallen branches nearby and pick them up")
    inventory["Branches"] = inventory.get("Branches", 0) + new_branches

def instructions():
    sp("""
----- SURVIVAL ISLAND -----
       INSTRUCTIONS

WELCOME, SURVIVOR!

You are stranded on a tropical island
after a helicopter crash.

Your goal is to survive, explore the
island, collect resources and repair
the helicopter to escape.

----- COMMANDS -----

[1] Explore
    Explore your surroundings and
    discover useful materials.

[2] Instructions
    Display this help screen.

[3] Show Inventory
    Check the items you are carrying.

----- SURVIVAL TIPS -----

- Collect resources regularly.
- Watch your hunger and health.
- Build a shelter before nightfall.
- Be careful around dangerous animals.
- Explore to discover useful locations.

----- MAIN OBJECTIVE -----

Find these three items:

- Gasoline tank
- Helicopter manual
- Duct tape

Repair the helicopter and escape!

---------------------------
""")

while True:
    print("-----SURVIVAL ISLAND-----")
    ask=input("Choose an action by entering its corresponding number:\n[1] Explore\n[2] Instructions\n[3] Show Inventory ")
    if ask not in possibilities_for_entering:
        sp("Please enter a valid input ?????")
    elif ask=="1" or ask.strip().capitalize()=="Explore":
        new_explore(new_branches)
        entered+=1
    elif ask=="3" or ask.strip().capitalize()=="Show Inventory":
        if not inventory:
            sp("Your inventory is empty, start exploring to gather items")
        else:
            pi()
    elif ask=="2" or ask.strip().capitalize()=="Instructions":
        instructions()