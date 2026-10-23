import random

# --- Game Data ---
rooms = ["a dark cave", "an ancient library", "a haunted hallway", "a treasure vault", "a dragon's lair"]
enemies = ["Goblin", "Skeleton", "Vampire", "Troll", "Ghost"]
weapons = ["Sword", "Bow", "Staff", "Dagger", "Axe"]
potions = ["Health Potion", "Strength Potion", "Shield Potion"]
treasures = ["Gold Coins", "Ancient Gem", "Magic Ring", "Old Map"]

weapon_damage = {"Sword": 25, "Bow": 20, "Staff": 30, "Dagger": 15, "Axe": 35}
enemy_hp_range = {"Goblin": (20,40), "Skeleton": (30,50), "Vampire": (40,60), "Troll": (50,70), "Ghost": (35,55)}

def print_divider():
    print("\n" + "="*40 + "\n")

def show_stats(name, hp, score, inventory):
    print(f"[ {name} | HP: {hp} | Score: {score} | Inventory: {', '.join(inventory) if inventory else 'Empty'} ]")

def use_potion(inventory, player_hp):
    available = [i for i in inventory if "Potion" in i]
    if not available:
        print("You have no potions!")
        return player_hp, inventory
    print("Potions available:", ", ".join(available))
    choice = input("Which potion? ").strip()
    if choice in available:
        if choice == "Health Potion":
            player_hp = min(100, player_hp + 30)
            print(f"You used a Health Potion! HP restored to {player_hp}.")
        elif choice == "Strength Potion":
            print("Strength Potion ready — your next attack deals double damage!")
        elif choice == "Shield Potion":
            print("Shield Potion used — you take no damage this round!")
        inventory.remove(choice)
    else:
        print("Invalid potion name.")
    return player_hp, inventory

def fight(name, weapon, player_hp, inventory, enemy, score):
    e_hp = random.randint(*enemy_hp_range[enemy])
    strength_boost = False
    shield_active = False

    print(f"\nA wild {enemy} appears with {e_hp} HP!")

    while e_hp > 0 and player_hp > 0:
        print()
        show_stats(name, player_hp, score, inventory)
        print(f"{enemy} HP: {e_hp}")
        print("\nWhat do you do?")
        print("  1. Attack")
        print("  2. Use Potion")
        print("  3. Run")
        action = input("Choose (1/2/3): ").strip()

        if action == "1":
            dmg = weapon_damage[weapon]
            if strength_boost:
                dmg *= 2
                strength_boost = False
                print("DOUBLE DAMAGE from Strength Potion!")
            dmg = random.randint(dmg - 5, dmg + 10)
            e_hp -= dmg
            print(f"You attack the {enemy} for {dmg} damage!")

            if e_hp > 0:
                enemy_dmg = random.randint(5, 20)
                if shield_active:
                    print(f"The {enemy} attacks but your shield blocks it!")
                    shield_active = False
                else:
                    player_hp -= enemy_dmg
                    print(f"The {enemy} hits you for {enemy_dmg} damage!")

        elif action == "2":
            prev_inv = inventory[:]
            player_hp, inventory = use_potion(inventory, player_hp)
            if "Strength Potion" not in prev_inv and "Strength Potion" in [i for i in prev_inv if i not in inventory]:
                strength_boost = True
            if "Shield Potion" not in prev_inv and "Shield Potion" in [i for i in prev_inv if i not in inventory]:
                shield_active = True

        elif action == "3":
            escape = random.choice([True, False])
            if escape:
                print(f"You escaped from the {enemy}!")
                return player_hp, score, inventory
            else:
                enemy_dmg = random.randint(10, 25)
                player_hp -= enemy_dmg
                print(f"Failed to escape! The {enemy} hits you for {enemy_dmg} damage!")
        else:
            print("Invalid choice, try again.")

    if e_hp <= 0:
        print(f"\nYou defeated the {enemy}! +15 points")
        score += 15
        loot = random.choice(potions + treasures)
        print(f"You found: {loot}!")
        inventory.append(loot)

    return player_hp, score, inventory

# --- Main Game ---
print_divider()
print("       ⚔️  DUNGEON ADVENTURE  ⚔️")
print_divider()

name = input("Enter your hero's name: ").strip()
weapon = random.choice(weapons)
player_hp = 100
score = 0
inventory = []

print(f"\nWelcome, {name}! You have been given a {weapon} (damage: {weapon_damage[weapon]}).")
print("Survive 5 rooms to win!\n")

for round_num in range(1, 6):
    print_divider()
    room = random.choice(rooms)
    print(f"Round {round_num}/5 — You enter {room}...")

    event = random.choices(["enemy", "treasure", "trap"], weights=[60, 25, 15])[0]

    if event == "enemy":
        enemy = random.choice(enemies)
        player_hp, score, inventory = fight(name, weapon, player_hp, inventory, enemy, score)

    elif event == "treasure":
        found = random.choice(treasures + potions)
        print(f"No enemies here... you find {found}!")
        inventory.append(found)
        score += 5

    elif event == "trap":
        dmg = random.randint(10, 20)
        print(f"It's a trap! You take {dmg} damage.")
        player_hp -= dmg

    if player_hp <= 0:
        print_divider()
        print(f"💀 {name} has fallen. Game over!")
        print(f"Final score: {score}")
        break
else:
    print_divider()
    print(f"🏆 {name} conquered the dungeon!")
    print(f"Final HP: {player_hp} | Final Score: {score}")
    print(f"Items collected: {', '.join(inventory) if inventory else 'None'}")