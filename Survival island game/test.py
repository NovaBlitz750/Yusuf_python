import random
fishing_loot=["fish","seaweed","crab","empty","stone axe","empty bottle",]
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
                continue
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