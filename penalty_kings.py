import random
import time
import os

# ══════════════════════════════════════════════════
#   ⚽  PENALTY KINGS — FC Mobile Style
#   Each round: You shoot, then you save!
# ══════════════════════════════════════════════════

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_print(text, delay=0.030):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def divider(char="═", n=50):
    print(char * n)

def pause(s=1.2):
    time.sleep(s)

# ══════════════════════════════════════════════════
#  TEAMS
# ══════════════════════════════════════════════════
TEAMS = {
    "PSG": {
        "emoji": "🔵🔴",
        "takers": [
            {"name": "Mbappé",    "power": 95, "accuracy": 88, "composure": 90},
            {"name": "Dembélé",   "power": 85, "accuracy": 82, "composure": 78},
            {"name": "Vitinha",   "power": 78, "accuracy": 85, "composure": 80},
            {"name": "Hakimi",    "power": 80, "accuracy": 78, "composure": 76},
            {"name": "Fabian",    "power": 76, "accuracy": 80, "composure": 74},
        ],
        "goalkeeper": {"name": "Donnarumma", "reflexes": 92, "reading": 85},
    },
    "Real Madrid": {
        "emoji": "⚪👑",
        "takers": [
            {"name": "Bellingham", "power": 90, "accuracy": 87, "composure": 88},
            {"name": "Vinicius",   "power": 88, "accuracy": 80, "composure": 82},
            {"name": "Modric",     "power": 78, "accuracy": 90, "composure": 92},
            {"name": "Valverde",   "power": 85, "accuracy": 82, "composure": 80},
            {"name": "Camavinga",  "power": 80, "accuracy": 78, "composure": 76},
        ],
        "goalkeeper": {"name": "Courtois", "reflexes": 91, "reading": 88},
    },
    "Man City": {
        "emoji": "🔵🌟",
        "takers": [
            {"name": "Haaland",   "power": 96, "accuracy": 85, "composure": 85},
            {"name": "De Bruyne", "power": 88, "accuracy": 92, "composure": 90},
            {"name": "Foden",     "power": 82, "accuracy": 88, "composure": 84},
            {"name": "Bernardo",  "power": 78, "accuracy": 88, "composure": 86},
            {"name": "Doku",      "power": 84, "accuracy": 78, "composure": 72},
        ],
        "goalkeeper": {"name": "Ederson", "reflexes": 88, "reading": 85},
    },
    "Barcelona": {
        "emoji": "🔴🔵",
        "takers": [
            {"name": "Lewandowski","power": 90, "accuracy": 88, "composure": 90},
            {"name": "Yamal",      "power": 80, "accuracy": 85, "composure": 82},
            {"name": "Pedri",      "power": 76, "accuracy": 88, "composure": 85},
            {"name": "Raphinha",   "power": 84, "accuracy": 82, "composure": 80},
            {"name": "Gavi",       "power": 75, "accuracy": 83, "composure": 78},
        ],
        "goalkeeper": {"name": "ter Stegen", "reflexes": 89, "reading": 86},
    },
    "Arsenal": {
        "emoji": "🔴⚪",
        "takers": [
            {"name": "Saka",       "power": 82, "accuracy": 88, "composure": 86},
            {"name": "Havertz",    "power": 85, "accuracy": 82, "composure": 80},
            {"name": "Odegaard",   "power": 80, "accuracy": 90, "composure": 88},
            {"name": "Martinelli", "power": 83, "accuracy": 78, "composure": 76},
            {"name": "Trossard",   "power": 78, "accuracy": 82, "composure": 78},
        ],
        "goalkeeper": {"name": "Raya", "reflexes": 86, "reading": 82},
    },
}

# ══════════════════════════════════════════════════
#  ZONES
# ══════════════════════════════════════════════════
SHOT_ZONES = {
    "1": ("Top Left",    0.82),
    "2": ("Top Center",  0.65),
    "3": ("Top Right",   0.82),
    "4": ("Mid Left",    0.78),
    "5": ("Mid Right",   0.78),
    "6": ("Bot Left",    0.72),
    "7": ("Bot Center",  0.55),
    "8": ("Bot Right",   0.72),
}

DIVE_ZONES = {
    "1": ("Dive Left",   ["1","4","6"]),
    "2": ("Stay Center", ["2","7"]),
    "3": ("Dive Right",  ["3","5","8"]),
    "4": ("Jump Left",   ["1","2"]),
    "5": ("Jump Right",  ["2","3"]),
}

# ══════════════════════════════════════════════════
#  ANIMATION
# ══════════════════════════════════════════════════
def animate_shot(zone_name, scored, taker_name, keeper_name, dive_dir=None):
    zone_pos = {
        "Top Left":   (0, 0), "Top Center":  (0, 1), "Top Right":  (0, 2),
        "Mid Left":   (1, 0),                         "Mid Right":  (1, 2),
        "Bot Left":   (2, 0), "Bot Center":  (2, 1), "Bot Right":  (2, 2),
    }
    row, col = zone_pos.get(zone_name, (1, 1))

    keeper_map = {
        "Dive Left":   "left",
        "Stay Center": "center",
        "Dive Right":  "right",
        "Jump Left":   "left",
        "Jump Right":  "right",
    }
    keeper_side = keeper_map.get(dive_dir, None)

    def make_goal(ball_pos=None, k_side=None, is_saved=False):
        # 3x3 grid: row 0=top, row 1=mid, row 2=bot | col 0=left, col 1=center, col 2=right
        slots = [
            [" · ", " · ", " · "],
            [" · ", "   ", " · "],
            [" · ", " · ", " · "],
        ]
        if ball_pos:
            br, bc = ball_pos
            slots[br][bc] = "⚽ "

        if k_side == "left":
            for r in range(3):
                slots[r][0] = "🧤✋" if is_saved else "🧤 "
        elif k_side == "right":
            for r in range(3):
                slots[r][2] = "✋🧤" if is_saved else " 🧤"
        elif k_side == "center":
            for r in range(3):
                slots[r][1] = " 🧤"

        lines = ["  ╔═══════════════════════════════╗"]
        for r in range(3):
            lines.append(f"  ║   {slots[r][0]}     {slots[r][1]}     {slots[r][2]}   ║")
        lines.append("  ╚══════════════╧═══════════════╝")
        lines.append("                 |")
        return "\n".join(lines)

    frames = [
        (make_goal(),                                      f"  🦵 {taker_name} runs up..."),
        (make_goal(k_side=keeper_side),                    f"  🧤 {keeper_name} gets set..."),
        (make_goal(ball_pos=(row, col), k_side=keeper_side),f"  ⚽  Ball heading {zone_name}!"),
    ]
    if scored:
        frames.append((make_goal(ball_pos=(row, col)),     "  🔥  G O A A A L ! ! !"))
    else:
        frames.append((make_goal(ball_pos=(row, col), k_side=keeper_side, is_saved=True),
                       f"  🧤  SAVED by {keeper_name}!"))

    for art, caption in frames:
        clear()
        divider()
        print(art)
        divider()
        slow_print(caption, delay=0.04)
        pause(0.72)
    pause(0.5)


def celebrate_goal(name):
    for msg in ["  🎉🎉  G O A L !  🎉🎉", f"  🏆  {name.upper()} SCORES!  🏆"]:
        clear(); divider("*"); print(); slow_print(msg, delay=0.05); print(); divider("*"); pause(0.55)


def celebrate_save(name):
    for msg in ["  🧤  WHAT A SAVE!", f"  🌟  {name.upper()} IS UNBEATABLE!  🌟"]:
        clear(); divider("-"); print(); slow_print(msg, delay=0.05); print(); divider("-"); pause(0.55)


# ══════════════════════════════════════════════════
#  POWER BAR
# ══════════════════════════════════════════════════
def power_bar():
    import threading
    print("\n  ⚡ POWER BAR — Press ENTER at the right moment!\n")
    pause(0.4)
    steps = 28
    lo, hi = 17, 25
    pressed_at = [steps]  # default to end if they don't press

    stop = threading.Event()

    def wait_for_enter():
        input()
        stop.set()

    t = threading.Thread(target=wait_for_enter, daemon=True)
    t.start()

    i = 0
    while i <= steps and not stop.is_set():
        bar  = "█" * i + "░" * (steps - i)
        zone = "🟢 PERFECT" if lo <= i <= hi else ("🟡 GOOD   " if i >= lo - 4 else "🔴 WEAK   ")
        print(f"  {zone} [{bar}] {int((i/steps)*100)}%", end="\r", flush=True)
        time.sleep(0.07)
        i += 1

    pressed_at[0] = i - 1
    print()

    diff = abs(pressed_at[0] - (lo + hi) // 2)
    if diff <= 4:
        return "⚡ Perfect power!", 1.00
    elif diff <= 8:
        return "👍 Good power.",    0.85
    elif diff <= 13:
        return "😬 Weak shot.",     0.70
    else:
        return "❌ Poor timing!",   0.50


# ══════════════════════════════════════════════════
#  SCOREBOARD
# ══════════════════════════════════════════════════
def show_scoreboard(my_score, opp_score, rnd, my_team, opp_team, total):
    divider("─")
    print(f"  📊 Round {rnd}/{total}")
    print(f"  {TEAMS[my_team]['emoji']} {my_team:<14} {my_score}  —  {opp_score}  {opp_team} {TEAMS[opp_team]['emoji']}")
    divider("─")
    print()


# ══════════════════════════════════════════════════
#  SHOOT (player takes penalty)
# ══════════════════════════════════════════════════
def goal_net_grid():
    print("""
    ┌──────────┬──────────┬──────────┐
    │ [1] T-L  │ [2] T-C  │ [3] T-R  │
    ├──────────┼──────────┼──────────┤
    │ [4] M-L  │          │ [5] M-R  │
    ├──────────┼──────────┼──────────┤
    │ [6] B-L  │ [7] B-C  │ [8] B-R  │
    └──────────┴──────────┴──────────┘
""")


def player_shoot(taker, opp_keeper, difficulty):
    divider()
    slow_print(f"  🦵 YOUR TURN TO SHOOT")
    slow_print(f"  {taker['name']} steps up to the spot...")
    pause(0.6)
    goal_net_grid()

    zone_key = input("  Choose zone (1-8): ").strip()
    if zone_key not in SHOT_ZONES:
        zone_key = str(random.randint(1, 8))
        slow_print(f"  Invalid! Auto-shot zone {zone_key}.")

    zone_name, base_chance = SHOT_ZONES[zone_key]
    timing_msg, power_mod  = power_bar()
    slow_print(f"\n  {timing_msg}")
    pause(0.4)

    acc_mod  = taker["accuracy"]  / 100
    comp_mod = taker["composure"] / 100
    chance   = base_chance * power_mod * acc_mod * comp_mod

    # CPU keeper guesses
    keeper_guess = str(random.randint(1, 8))
    correct      = keeper_guess == zone_key
    ref_mod      = opp_keeper["reflexes"] / 100
    save_ch      = ref_mod * (0.72 if correct else 0.12)
    saved        = random.random() < save_ch

    scored = (random.random() < chance) and not saved

    dive_dir = ("Dive Left" if int(keeper_guess) in [1,4,6]
                else "Dive Right" if int(keeper_guess) in [3,5,8]
                else "Stay Center")

    animate_shot(zone_name, scored, taker["name"], opp_keeper["name"], dive_dir=dive_dir)

    if scored:
        celebrate_goal(taker["name"])
    else:
        celebrate_save(opp_keeper["name"])

    return scored


# ══════════════════════════════════════════════════
#  SAVE (player dives to keep)
# ══════════════════════════════════════════════════
def dive_grid():
    print("""
    ┌───────────────────────────────────┐
    │  [1] Dive Left   [2] Stay Centre  │
    │  [3] Dive Right                   │
    │  [4] Jump Left   [5] Jump Right   │
    └───────────────────────────────────┘
""")


def player_save(my_keeper, cpu_taker, difficulty):
    divider()
    slow_print(f"  🧤 YOUR TURN TO SAVE")
    slow_print(f"  {cpu_taker['name']} is stepping up...")
    pause(0.8)
    dive_grid()

    dive_key = input("  Choose your dive (1-5): ").strip()
    if dive_key not in DIVE_ZONES:
        dive_key = "1"
        slow_print("  Invalid! Defaulting to Dive Left.")

    dive_label, covers = DIVE_ZONES[dive_key]

    # CPU picks a zone
    diff_mod = {"Easy": 0.55, "Medium": 0.72, "Hard": 0.90}[difficulty]
    zone_key  = str(random.randint(1, 8))
    zone_name, base_chance = SHOT_ZONES[zone_key]
    shot_power = base_chance * diff_mod * (cpu_taker["accuracy"] / 100)

    correct_dive = zone_key in covers
    ref_mod      = my_keeper["reflexes"] / 100

    save_chance   = ref_mod * (0.82 if correct_dive else 0.08)
    scored_anyway = random.random() < shot_power * 0.45
    saved         = (random.random() < save_chance) and not scored_anyway
    cpu_scored    = not saved

    animate_shot(zone_name, cpu_scored, cpu_taker["name"], my_keeper["name"], dive_dir=dive_label)

    if saved:
        celebrate_save(my_keeper["name"])
        slow_print(f"  {'✅ Correct dive!' if correct_dive else '🤞 Lucky guess!'}")
    else:
        celebrate_goal(cpu_taker["name"])
        if not correct_dive:
            slow_print(f"  ℹ️  Ball went {zone_name} — you chose {dive_label}.")

    return saved  # True = CPU did NOT score


# ══════════════════════════════════════════════════
#  SUDDEN DEATH
# ══════════════════════════════════════════════════
def sudden_death(hero_team, opp_team, difficulty, my_score, opp_score):
    slow_print("\n  ⚡ SUDDEN DEATH! Shoot AND save each round!")
    pause(1.0)

    my_takers  = TEAMS[hero_team]["takers"]
    opp_takers = TEAMS[opp_team]["takers"]
    my_keeper  = TEAMS[hero_team]["goalkeeper"]
    opp_keeper = TEAMS[opp_team]["goalkeeper"]
    rnd = 1

    while True:
        clear()
        slow_print(f"  ⚡ SUDDEN DEATH — Round {rnd}")
        show_scoreboard(my_score, opp_score, "SD", hero_team, opp_team, "SD")

        taker     = my_takers[(rnd - 1) % len(my_takers)]
        opp_taker = opp_takers[(rnd - 1) % len(opp_takers)]

        my_scored  = player_shoot(taker, opp_keeper, difficulty)
        cpu_missed = player_save(my_keeper, opp_taker, difficulty)
        cpu_scored = not cpu_missed

        if my_scored:
            my_score += 1
        if cpu_scored:
            opp_score += 1

        if my_scored and not cpu_scored:
            return "win", my_score, opp_score
        elif cpu_scored and not my_scored:
            return "lose", my_score, opp_score

        input("\n  Both scored / both missed. Press Enter for next SD round...")
        rnd += 1


# ══════════════════════════════════════════════════
#  TEAM SELECT
# ══════════════════════════════════════════════════
def pick_team(prompt, exclude=None):
    team_list = [t for t in TEAMS if t != exclude]
    print(f"\n  {prompt}\n")
    for i, t in enumerate(team_list, 1):
        gk = TEAMS[t]["goalkeeper"]["name"]
        print(f"  [{i}] {TEAMS[t]['emoji']} {t:<14} (GK: {gk})")
    print()
    try:
        return team_list[int(input("  > ").strip()) - 1]
    except:
        return team_list[0]


# ══════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════
def main():
    clear()
    divider("═")
    slow_print("  ⚽  PENALTY KINGS  ⚽")
    slow_print("  Shoot and Save every round!")
    divider("═")
    pause(0.4)

    hero_team = pick_team("Your team:")
    opp_team  = pick_team("Opponent:", exclude=hero_team)

    print("\n  Difficulty:\n")
    print("  [1] Easy   [2] Medium   [3] Hard\n")
    difficulty = {"1":"Easy","2":"Medium","3":"Hard"}.get(input("  > ").strip(), "Medium")

    my_keeper  = TEAMS[hero_team]["goalkeeper"]
    opp_keeper = TEAMS[opp_team]["goalkeeper"]
    my_takers  = TEAMS[hero_team]["takers"]
    opp_takers = TEAMS[opp_team]["takers"]

    clear()
    divider("═")
    slow_print(f"  {TEAMS[hero_team]['emoji']} {hero_team}  vs  {TEAMS[opp_team]['emoji']} {opp_team}")
    slow_print(f"  Difficulty: {difficulty}   |   5 rounds each")
    slow_print(f"  🦵 You shoot with {my_takers[0]['name']}...")
    slow_print(f"  🧤 You save with {my_keeper['name']}!")
    divider("═")
    pause(1.5)

    my_score  = 0
    opp_score = 0
    total     = 5

    for r in range(1, total + 1):
        clear()
        show_scoreboard(my_score, opp_score, r, hero_team, opp_team, total)

        taker     = my_takers[r - 1]
        opp_taker = opp_takers[r - 1]

        # Step 1: Player shoots
        my_scored = player_shoot(taker, opp_keeper, difficulty)
        if my_scored:
            my_score += 1

        input("\n  Press Enter — now SAVE their penalty...")

        # Step 2: Player saves
        cpu_missed = player_save(my_keeper, opp_taker, difficulty)
        if not cpu_missed:
            opp_score += 1

        show_scoreboard(my_score, opp_score, r, hero_team, opp_team, total)
        input("  Press Enter for next round...")

    # Result
    clear()
    divider()
    show_scoreboard(my_score, opp_score, "FT", hero_team, opp_team, total)

    if my_score == opp_score:
        slow_print("  ⚡ TIED! Going to Sudden Death...")
        pause(1.5)
        result, my_score, opp_score = sudden_death(
            hero_team, opp_team, difficulty, my_score, opp_score)
    elif my_score > opp_score:
        result = "win"
    else:
        result = "lose"

    clear()
    divider("═")
    if result == "win":
        slow_print(f"\n  🏆 {hero_team.upper()} WIN THE SHOOTOUT!")
        slow_print("  You're a PENALTY KING! 👑⚽")
    else:
        slow_print(f"\n  💔 {opp_team.upper()} WIN THE SHOOTOUT!")
        slow_print("  Keep training! 💪")
    divider("═")
    print(f"\n  Final: {hero_team} {my_score} — {opp_score} {opp_team}\n")
    pause(0.8)

    again = input("  Play again? (y/n): ").strip().lower()
    if again == "y":
        main()
    else:
        slow_print("\n  Thanks for playing Penalty Kings! ⚽\n")


if __name__ == "__main__":
    main()