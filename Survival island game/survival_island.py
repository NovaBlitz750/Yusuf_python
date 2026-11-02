
import random
import time

structure_dice=[1,2,3,4,5,6]
current_animal=None
health=100
current_biome="Beach"
hearts=health//20
fishing_loot=["fish","seaweed","crab","empty","stone axe","empty bottle"]
unlocked_biomes={"Beach"}
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
def hunt():
    global current_animal

    if current_animal is None:
        sp("There are no animals nearby to hunt!")
        return

    if current_animal == "Monkey" or current_animal == "Tropical Bird":
        sp("This animal cannot be hunted!")
        return

    if inventory.get("Stone Knife", 0) <= 0:
        sp("You need a Stone Knife to hunt!")
        return

    sp(f"You attempt to hunt the {current_animal}!")

    if random.randint(1, 100) <= 60:
        sp("You successfully hunted the animal!")
        inventory["Raw Meat"] = inventory.get("Raw Meat", 0) + random.randint(1, 5)
    else:
        sp("The animal escaped!")

    inventory["Stone Knife"] -= 2
    current_animal = None

def animal_encounter():
    global current_animal

    encounter = random.randint(1, 100)

    if encounter <= 40:
        current_animal = random.choice(["Wild Boar", "Monkey", "Snake", "Tropical Bird"])

        sp(f"You encounter a {current_animal}!")
    else:
        sp("You explore the jungle but encounter no animals.")
def fishing():
    while True:
        loot=random.choice(fishing_loot)
        if loot=="empty":
            sp("attempt failed, nothing found. Try again? (y/n) ")
            try_again=input(" ")
            if try_again=="y":
                continue
            else:
                break
        elif loot=="stone axe":
            sp(f"Attempt successful!, {loot} found, add to inventory? (y/n) ")
            add_to_inv=input(" ").strip().lower()
        if add_to_inv=="y":
            inventory[loot]= inventory.get(loot,0)+1
        else:
            sp(f"Attempt successful!, {loot} found, add to inventory? (y/n) ")
            add_to_inv=input(" ").strip().lower()
        if add_to_inv=="y":
                inventory[loot] = inventory.get(loot, 0) + 1
        else:
            sp(f"{loot} discarded successfully")
    

def pi():
    sp(f"Inventory:{inventory}")

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

def crafting_recipes():
    sp("""
================================
       CRAFTING RECIPES
================================""")
    print("""
[1] STONE AXE
    2x Branches
    2x Stones
    2x Vines
    ----------------------------
    40 Durability
    -4 Durability per use
    Used for chopping trees.

[2] STONE KNIFE
    1x Sharp Stone
    1x Branch
    1x Vine
    ----------------------------
    35 Durability
    -2 Durability per attack
    Used for cutting materials.

[3] FISHING ROD
    2x Branches
    3x Vines
    ----------------------------
    25 Durability
    -2 Durability per fishing attempt
    Used for catching fish.

[4] BOW
    3x Branches
    3x Vines
    ----------------------------
    35 Durability
    -2 Durability per arrpw shot
    Use: Hunt animals from a distance.

[5] Arrow
    1x Branch
    1x Stone
    1x Vine
    Gives 3 per craft
    Use: Needed to attack with bow

[6] Campfire
    7x Branches
    2x Stone (won't be consumed while crafting)
    5x Vines
================================
    Infinite Durability
    Can only be placed down once
    Use: Cook food
""")
    crafted_item=input("Choose the number of which item you wanna craft: ")
    if crafted_item=="1":
        if inventory.get("Branches",0) >= 2 and inventory.get("Stones",0)>=2 and inventory.get("Vines",0)>=2:
            sp("You have enough materials to craft an axe, would u like to proceed? (y/n) ")
            craft_axe=input(" ").strip().lower()
            if craft_axe=="y" or craft_axe=="yes":
                inventory["Branches"]-=2
                inventory["Stones"]-=2
                inventory["Vines"]-=2
                inventory["Stone Axe"] = inventory.get("Stone Axe", 0) + 40
                sp("Crafted Stone Axe successfully")
            else:
                print("Failed to craft a Stone Axe")
        else:
            sp("You don't have enough materials to craft a stone axe")    
    elif crafted_item=="2":
        if inventory.get("Branches",0)>=1 and inventory.get("Stones",0)>=1 and inventory.get("Vines",0)>=1:
            sp("You have enough materials to craft a stone knife, would u like to proceed? (y/n) ")
            craft_knife=input(" ").strip().lower()
            if craft_knife=="y" or craft_knife=="yes":
                inventory["Branches"]-=1
                inventory["Stones"]-=1
                inventory["Vines"]-=1
                inventory["Stone Knife"] = inventory.get("Stone Knife", 0) + 35
                sp("Crafted Stone Knife successfully")
            else:
                sp("Failed to craft Stone Knife")
        else: 
            sp("You don't have enough materials to craft a stone knife")
    elif crafted_item=="3":
        if inventory.get("Branches",0)>=2 and inventory.get("Vines",0)>=3:
            sp("You have enough materials to craft a fishing rod, would u like to proceed? (y/n) ")
            craft_fishing_rod=input(" ").strip().lower()
            if craft_fishing_rod=="y" or craft_fishing_rod=="yes":
                inventory["Branches"]-=2
                inventory["Vines"]-=3
                inventory["Fishing Rod"] = inventory.get("Fishing Rod", 0) + 25
                sp("Crafted Fishing Rod Successfully")
            else: 
                sp("Failed to craft a Fishing Rod")
        else:
            sp("You don't have enough materials to craft a Fishing Rod")

    elif crafted_item=="4":
        if inventory.get("Branches",0)>=3 and inventory.get("Vines",0)>=3:
            sp("You have enough materials to craft a fishing rod, would u like to proceed? (y/n) ")
            craft_bow=input(" ").strip().lower()
            if craft_bow=="y" or craft_bow=="yes":
                inventory["Branches"]-=3
                inventory["Vines"]-=3
                inventory["Bow"]=inventory.get("Bow",0)+35
                sp("Bow crafted successfully")
            else:
                sp("Failed to craft Bow")
        else:
            sp("You don't have enough materials to craft a bow")
    elif crafted_item=="5":
        if inventory.get("Branches",0)>=1 and inventory.get("Stones",0)>=1 and inventory.get("Vines",0)>=1:
            sp("You have enough materials to craft arrows, woud u like to proceed? (y/n) ")
            craft_arrows=input(" ").strip().lower()
            if craft_arrows=="y" or craft_arrows=="yes":
                inventory["Branches"]-=1
                inventory["Stones"]-=1
                inventory["Vines"]-=1
                inventory["Arrow"]=inventory.get("Arrow",0)+3
                sp("3 Arrows crafted successfully")
            else:
                sp("Failed to craft arrows")
        else:
            sp("You don't have enough materials to craft arrows")
    elif crafted_item=="6":
        if inventory.get("Branches",0)>=7 and inventory.get("Vines",0)>=5 and inventory.get("Stones",0)>=2:
            sp("You have enough materials to craft a campfire, would u like to proceed? (y/n) ")
            craft_campfire=input(" ").strip().lower()
            if craft_campfire=="y" or craft_campfire=="yes":
                inventory["Branches"]-=7
                inventory["Vines"]-=5
                inventory["Campfire"]=inventory.get("Campfire",0)+99999
                sp("Campfire craft successfully")
            else:
                sp("Failed to craft Campfire")
        else:
            sp("You don't have enough materials to craft a campfire")
                
def main():
    global entered, current_biome
    while True:
        print("Health:",health, "❤️ " * (health // 20))
        print("-----SURVIVAL ISLAND-----")
        ask=input("Choose an action by entering its corresponding number:\n[1] Explore\n[2] Instructions\n[3] Show Inventory\n[4] View Crafting Recipes\n[5] Go Fishing\n[6] Chop Trees ")
        if ask not in possibilities_for_entering:
            sp("Please enter a valid input ?????")
        elif (entered == 0 and ask == "1") or (entered == 0 and ask.strip().capitalize() == "Explore"):
            new_explore(new_branches)
            entered += 1

        elif (entered <= 3 and ask == "1") or (entered >= 1 and ask.strip().capitalize() == "Explore"):
            sp("You enter a jungle and pick up stones from the ground and vines dangling from trees")
            ran_stones = random.randint(1,5)
            ran_vines = random.randint(1,8)
            inventory["Stones"] = inventory.get("Stones", 0) + ran_stones
            inventory["Vines"] = inventory.get("Vines", 0) + ran_vines
            entered += 1
            current_biome="Jungle"
        elif (entered > 3 and ask == "1") or (entered >= 1 and ask.strip().capitalize() == "Explore"):
            current_biome="Jungle"
            sp("Would you like to: \n[1] Explore deeper into the jungle?\n[2] Explore the beach shore more")
            jungle_or_beach=input(" ")
            if jungle_or_beach=="1":
                sp("You explore deeper into the jungle...")
                deeper_explore=random.choice(structure_dice)
                if deeper_explore==3:
                    sp("""You notice something in between the trees


You discovered:
AN ABANDONED CABIN!

Would u like to enter? (y/n) """)
                    enter=input(" ").strip().lower()
                    if enter=="y" or enter=="yes":
                        sp("You find wooden planks, bread, duct tape and a helicopter manual inside!")
                        inventory["Planks"]=15
                        inventory["Bread"]=30
                        inventory["Duct Tape"]=1
                        inventory["Helicopter Manual"]=1
                    else:
                        sp("You leave the cabin and continue exploring...")
                        pass
                else:
                    animal_encounter()

        elif ask=="3" or ask.strip().capitalize()=="Show Inventory":
            if not inventory:
                sp("Your inventory is empty, start exploring to gather items")
            else:
                pi()
        elif ask=="2" or ask.strip().capitalize()=="Instructions":
            instructions()
        elif ask=="4" or ask.strip().capitalize()=="View Crafting Recipes":
            crafting_recipes()
        elif ask=="5" or ask.strip().capitalize()=="Go Fishing":
            if "Fishing Rod" in inventory and current_biome=="Beach":
                fishing()
            elif current_biome!="Beach":
                sp(f"Travel to a beach to start fishing, u cannot fish in {current_biome}")
            elif "Fishing Rod" not in inventory:
                sp("Acquire fishing rod first to start fishing")
            else:
                sp("Acquire fishing rod and travel to a beach biome to start fishing")


main()