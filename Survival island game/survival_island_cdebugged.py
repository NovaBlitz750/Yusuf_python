import random
import time

hunger=100
hill_boar_fight=False
current_biome = "Beach"
current_animal = None
hunger = 100
FOOD_VALUES = {"Bread": 10, "Fish": 15, "Crab": 10, "Cooked Meat": 30, "Raw Meat": 5}
structure_dice=[1,2,3,4,5,6]
aft_looting_boathouse=""
health=100
hearts=health//20
fishing_loot=["Fish","Seaweed","Crab","empty","stone axe","Empty Bottle"]
unlocked_biomes={"Beach"}
choices=[]
inventory={}
possibilities_for_entering=["1","2","3","4","5","6","7","8","9"]
entered=0
new_branches=random.randint(1,10)
COOKABLE = {"Raw Meat": "Cooked Meat", "fish": "Fish", "crab": "Crab"}

def clean_inventory():
    for item in [k for k, v in inventory.items() if v <= 0]:
        del inventory[item]

def cook():
    if inventory.get("Campfire", 0) <= 0:
        sp("You need a Campfire to cook! Craft one first.")
        return

    items = [f for f in COOKABLE if inventory.get(f, 0) > 0]
    if not items:
        sp("You have nothing to cook!")
        return

    sp("What do you want to cook?")
    for i, f in enumerate(items, 1):
        sp(f"[{i}] {f} x{inventory[f]}")
    choice = input(" ").strip()

    if choice.isdigit() and 1 <= int(choice) <= len(items):
        raw = items[int(choice) - 1]
        cooked = COOKABLE[raw]
        amount = inventory[raw]          # cook the whole stack
        del inventory[raw]
        inventory[cooked] = inventory.get(cooked, 0) + amount
        sp(f"You cook {amount} {raw} over the campfire and get {amount} {cooked}.")
    else:
        sp("Invalid choice.")

def update_hunger(amount=5):
    global hunger, health
    hunger = max(0, hunger - amount)
    if hunger == 0:
        sp("You're starving! You lose 10 health.")
        health -= 10
    elif hunger <= 10:
        sp("You're weak with hunger... you lose 2 health.")
        health -= 2
    elif hunger <= 25:
        sp("Your stomach growls... you need to eat soon.")

def eat():
    global hunger
    foods = [f for f in FOOD_VALUES if inventory.get(f, 0) > 0]
    if not foods:
        sp("You have no food!")
        return
    for i, f in enumerate(foods, 1):
        sp(f"[{i}] {f} x{inventory[f]} (+{FOOD_VALUES[f]} hunger)")
    choice = input(" ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(foods):
        food = foods[int(choice) - 1]
        inventory[food] -= 1
        if inventory[food] == 0:
            del inventory[food]
        hunger = min(100, hunger + FOOD_VALUES[food])
        sp(f"You eat the {food}. Hunger is now {hunger}.")
    else:
        sp("Invalid choice.")
def sp(text, delay=0.03):
    for character in text:
        print(character, end='', flush=True)
        time.sleep(delay)
    print()
def hunt():
    global current_animal

    # animal_encounter() always resets current_animal to None, so hunting
    # could never start. Pick an animal here instead.
    current_animal = random.choice(["Wild Boar", "Rabbit", "Monkey", "Tropical Bird"])

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
    global current_animal, health

    encounter = random.randint(4, 100)

    if encounter >= 1:
        current_animal = random.choice(["Wild Boar", "Monkey", "Snake", "Vulture"])

        sp(f"You encounter a {current_animal}!")

        if current_animal == "Wild Boar" or current_animal == "Snake" or current_animal=="Vulture":
            sp("This animal is dangerous! What will you do?")
            sp("[1] Fight")
            sp("[2] Run away")

            choice = input(" ").strip()

            if choice == "1":
                if (inventory.get("Bow", 0) >= 20 and inventory.get("Arrow", 0) >= 20):
                    sp("You use your bow and arrows to fight and obtain raw meat")
                    inventory["Bow"] -= 2
                    inventory["Arrow"] -= 20
                    inventory["Raw Meat"]=inventory.get("Raw Meat", 0)+random.randint(1,6)
                elif inventory.get("Stone Axe", 0) >= 20:
                    sp("You use your Stone Axe to fight!")
                    inventory["Stone Axe"] -= 20
                    health-=random.randint(20,60)
                    inventory["Raw Meat"] = inventory.get("Raw Meat", 0) + random.randint(2, 10)

                elif inventory.get("Stone Knife", 0) >= 20:
                    sp("You use your Stone Knife to fight!")
                    inventory["Stone Knife"] -= 20
                    health-=random.randint(20,60)
                
                    inventory["Raw Meat"]=inventory.get("Raw Meat", 0)+random.randint(2,10)
                else:
                    sp("You don't have a weapon with enough durability or arrows!")
                    sp("You try to escape instead...")
                    if random.randint(1, 2) == 1:
                        sp("The animal catches you! You have been killed!")
                        health = 0
                        die()
                    else:
                        sp("You successfully escaped!")

            elif choice == "2":
                if random.randint(1, 2) == 1:
                    sp("The animal catches you! You have been killed!")
                    health = 0
                else:
                    sp("You successfully escaped!")

            else:
                sp("Invalid choice! The animal attacks while you hesitate!")
                health = 0
                die()
        else:
            sp("The animal isn't dangerous and leaves you alone.")

    else:
        sp("You explore the jungle but encounter no animals.")

    current_animal = None
def fishing():
    while True:
        loot = random.choice(fishing_loot)
        fish=input("Press enter to attempt fishing, enter stop to stop fishing")
        
        if fish=="stop":
            break
        else:
            pass
        inventory["Fishing Rod"]-=2
        if loot == "empty":
            sp("Attempt failed, nothing found. Try again? (y/n)")
            try_again = input(" ").strip().lower()

            if try_again == "y":
                pass
            else:
                break

        elif loot == "stone axe":
            sp(f"Attempt successful! {loot} found, add to inventory? (y/n)")
            add_to_inv = input(" ").strip().lower()

            if add_to_inv == "y":
                inventory["Stone Axe"] = inventory.get("Stone Axe", 0) + 40
            else:
                sp("Stone Axe discarded successfully")

        else:
            sp(f"Attempt successful! {loot} found, add to inventory? (y/n)")
            add_to_inv = input(" ").strip().lower()

            if add_to_inv == "y":
                inventory[loot] = inventory.get(loot, 0) + 1
            else:
                sp(f"{loot} discarded successfully")
        if inventory.get("Fishing Rod",0)<=0:
            sp("Your fishing rod broke! acquire a new one to start fishing again")
            break
def boathouse():
    global aft_looting_boathouse
    sp("You enter the boathouse, what next?\n[1] Investigate locked cupboard\n[2] Pick up available items")
    boathouse_ask=input(" ")
    if boathouse_ask=="1":
        global aft_looting_boathouse
        key_attempts=random.randint(1,10)
        for i in range(0,key_attempts):
            print("You insert the key you found at the shore into the lock, its pretty rusty and old so you try to yank it open")
            key_attempt=input("Press enter to try opening the cupboard")
            if i<7:
                print("Attempt failed, try again")
        sp("Attempt successful, inside you find a gasoline can, duct tape and engine oil")
        inventory["Engine Oil"]=1
        inventory["Duct Tape"]=1
        inventory["Gasoline Can"]=1
        sp("You explore the rest of the boathouse and find a map and 20 pieces of bread")
        inventory["Map"]=1
        inventory["Bread"]=20
        sp("You leave the boathouse, what next?\n[1] Open Map \n[2] Follow map")
        aft_looting_boathouse=input(" ")
        if aft_looting_boathouse=="1":
            open_map()
    elif boathouse_ask=="2":
        sp("You explore the rest of boathouse and find a map and 20 pieces of bread")
        inventory["Map"]=1
        inventory["Bread"]=inventory.get("Bread", 0)+20
        
    else:
        print("Please enter a valid input")
def open_map():
    global current_biome
    places = sorted(unlocked_biomes)

    sp(f"You are in: {current_biome}")
    sp("Where do you want to travel?")
    for i, place in enumerate(places, 1):
        sp(f"[{i}] {place}")

    choice = input(" ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(places):
        destination = places[int(choice) - 1]
        if destination == current_biome:
            sp("You're already here!")
        else:
            sp(f"You travel to the {destination}...")
            current_biome = destination
            update_hunger(10)
    else:
        sp("You stay where you are.")
def die():
    global current_animal, health, current_biome, unlocked_biomes
    global inventory, entered, new_branches, aft_looting_boathouse

    sp("You Died!")

    current_animal = None
    health = 100
    current_biome = "Beach"
    unlocked_biomes = {"Beach"}
    inventory = {}
    entered = 0
    new_branches = random.randint(1, 10)
    aft_looting_boathouse = ""
    exit()
def pi():
    sp(f"Inventory:{inventory}")
def beach_explore():
    sp("You explore further along the beach...")

    beach_dice = random.randint(1, 6)

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
REQUIRED_ITEMS = ["Gasoline Can", "Duct Tape", "Helicopter Manual"]

def crash_site():
    sp("You stand in front of the wrecked helicopter...")

    missing = [item for item in REQUIRED_ITEMS if inventory.get(item, 0) <= 0]

    if missing:
        sp("You can't repair it yet. You still need:")
        for item in missing:
            sp(f"- {item}")
        return
    if "Helicopter Manual" not in inventory:
        sp("You don't know how to control the helicopter, find the manual and read it first")

    sp("You have everything you need! Start the repair? (y/n)")
    answer = input(" ").strip().lower()
    if answer == "y" or answer == "yes":
        sp("Press enter to pour in gasoline.....................")
        gasoline_pour=input(" ")
        sp("Tank full!")
        for i in range(0,random.randint(0,10)):
            sp("Press enter to fix copter blades")
            blade_fix=input(" ")
        sp("You get into the helicopter, they key is already there")
        for i in range(0,random.randint(0,7)):
            sp("Press enter to try and start helicopter....")
            helicopter_start=input("")
        sp("The Helciopter starts and the engine roars to life, you escape the island and reach a city\n     YOU WIN!")
    else:
        sp("You step back from the helicopter.")

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
    45 Durability
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
    Can be used forever
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
                inventory["Bow"]=inventory.get("Bow",0)+45
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
    global entered, current_biome, health, aft_looting_boathouse, hill_boar_fight
    while True:
        
        print("Health:",health, "❤️ " * (health // 20))
        print("Hunger:", hunger, "🍗" * (hunger//20))
        print("-----SURVIVAL ISLAND-----")
        ask=input("Choose an action by entering its corresponding number:\n[1] Explore\n[2] Instructions\n[3] Show Inventory\n[4] View Crafting Recipes\n[5] Go Fishing\n[6] Open Map\n[7] Eat\n[8] Hunt\n[9] Cook food ")
        if ask not in possibilities_for_entering:
            sp("Please enter a valid input ?????")
            continue
        update_hunger(5)
        if (entered == 0 and ask == "1") or (entered == 0 and ask.strip().capitalize() == "Explore"):
            new_explore(new_branches)
            entered += 1

        elif (entered <= 2 and ask == "1") or (entered >= 1 and ask.strip().capitalize() == "Explore"):
            sp("You enter a jungle and pick up stones from the ground and vines dangling from trees")
            ran_stones = random.randint(1,5)
            ran_vines = random.randint(1,8)
            inventory["Stones"] = inventory.get("Stones", 0) + ran_stones
            inventory["Vines"] = inventory.get("Vines", 0) + ran_vines
            entered += 1
            current_biome="Jungle"
            unlocked_biomes.add("Jungle")
        elif (entered >= 3 and ask == "1") or (entered >= 1 and ask.strip().capitalize() == "Explore"):
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
                        sp("You find wooden planks, bread and a helicopter manual inside!\n You read the manual and now can control a helicopter")
                        inventory["Planks"]=15
                        inventory["Bread"]=30
                        
                        inventory["Helicopter Manual"]=1
                    else:
                        sp("You leave the cabin and continue exploring...")
                        pass
                else:
                    animal_encounter()
            else:
                sp("""You keep walking along the edge of the beach and see something hidden in the sand...' 
                Its a Key!""")
                current_biome="Beach"
                inventory["Key"]=1
                sp("..........")
                beach_explore()
                if aft_looting_boathouse =="1" and not hill_boar_fight:
                    sp("You follow the map up large hills")
                    unlocked_biomes.add("Large Hills")
                    current_biome="Large Hills"
                    sp("You encounter a wild boar! What will be your next decision?\n[1] Run Away\n[2] Fight it")
                    fight_or_flight=input(" ")
                    if fight_or_flight=="1":
                        sp("You started running and make the boar aggressive, it chases you and hits you down the hill")
                    elif fight_or_flight=="2":
                        if (inventory.get("Bow",0)>=40 and inventory.get("Arrow",0)>=20):
                            sp("You bow the arrow from a distance and kill the boar but consume 20 arrows in the process, raw meat obtained")
                            inventory["Bow"]-=40
                            inventory["Arrow"]-=20
                            inventory["Raw Meat"]=random.randint(1,6)
                        elif inventory.get("Stone Knife",0)>=20:
                            sp("You rapidly attack the boar with your stone knife and obtain all of its raw meat")
                            inventory["Stone Knife"]-=20
                            inventory["Raw Meat"]=inventory.get("Raw Meat",0)+30
                            health-=25
                        elif inventory.get("Stone Axe",0)>=20:
                            sp("You swing at the boar with your stone axe and obtain raw meat")
                            inventory["Stone Axe"]-=20
                            inventory["Raw Meat"]=inventory.get("Raw Meat",0)+random.randint(1,20)
                            health-=40
                    hill_boar_fight=True

                    sp("After the journey up the mountain, you find.... THE HELCIPOTER CRASH SITE")
                    crash_site()
                elif aft_looting_boathouse=="2" and hill_boar_fight:
                    crash_site()


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
        elif ask=="6":
            open_map()
        elif ask == "7":
            eat()
        elif ask=="8" and (current_biome=="Jungle" or current_biome=="Large Hills") and "Stone Knife" in inventory:
            hunt()
        elif "Stone Knife" not in inventory and ask=="8":
            sp("Acquire a stone knife to start hunting")
        elif ask=="8":
            if current_biome!="Jungle" or current_biome!="Large Hills":
                sp("Go to Large Hills or a Jungle biome to start hunting")
        elif ask=="9":
            cook()
        clean_inventory()
        if health<=0:
            die()
        
main()