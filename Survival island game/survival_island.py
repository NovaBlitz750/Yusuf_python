
import random
import time

unlocked_location={"Beach"}
choices=[]
inventory={}
possibilities_for_entering=["1","2","3","4","5"]
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


""")

def crafting_recipes(crafted_item):
    sp("""
================================
       CRAFTING RECIPES
================================""")
    print(""")
[1] STONE AXE
    2x Branches
    2x Stones
    2x Vines
    ----------------------------
    Used for chopping trees.

[2] STONE KNIFE
    1x Sharp Stone
    1x Branch
    1x Vine
    ----------------------------
    Used for cutting materials.

[3] WOODEN SPEAR
    2x Branches
    1x Sharp Stone
    2x Vines
    ----------------------------
    Used for hunting.

[4] FISHING ROD
    2x Branches
    3x Vines
    ----------------------------
    Used for catching fish.

[5] BOW
    3x Branches
    3x Vines
    Durability: 35
    Use: Hunt animals from a distance.

================================
""")
    crafted_item=input("Choose the number of which item you wanna craft: ")
    if crafted_item=="1":
        if inventory.get("Branches",0) >= 2 and inventory.get("Stones",0)>=2 and inventory.get("Vines",0)>=2:
            sp("You have enough materials to craft an axe, would u like to proceed? (y/n)").strip().lower()
            craft_axe=input(" ")
            if craft_axe=="y" or craft_axe=="y":
                inventory["Branches"]-=2
                inventory["Stones"]-=2
                inventory["Vines-=2"]
        else:
            sp("You don't have enough materials to craft a stone axe")    
while True:
    print("-----SURVIVAL ISLAND-----")
    ask=input("Choose an action by entering its corresponding number:\n[1] Explore\n[2] Instructions\n[3] Show Inventory\n[4] View Crafting Recipes")
    if ask not in possibilities_for_entering:
        sp("Please enter a valid input ?????")
    elif ask=="1" or ask.strip().capitalize()=="Explore" and entered<1:
        new_explore(new_branches)
        entered+=1
    elif ask=="1" or ask.strip().capitalize()=="Explore" and entered>1 and entered<5:
        print("You enter a jungle and pick up stones from the ground and vines dangling from trees")
        ran_stones=random.randint(1,5)
        ran_vines=random.randint(1,8)
        inventory["Stones"] = inventory.get("Stones", 0) + ran_stones
        inventory["Vines"]=inventory.get("Vines",0)+ran_vines
    elif ask=="3" or ask.strip().capitalize()=="Show Inventory":
        if not inventory:
            sp("Your inventory is empty, start exploring to gather items")
        else:
            pi()
    elif ask=="2" or ask.strip().capitalize()=="Instructions":
        instructions()
    elif ask=="4" or ask.strip().capitalize()=="View Crafting Recipes":
        crafting_recipes()
