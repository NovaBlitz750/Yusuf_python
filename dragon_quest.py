import random
import time
import os

# ══════════════════════════════════════════════════
#   🐉  DRAGON QUEST  — EXPANDED EDITION
#   New: Equipment · Status Effects · Skills
#        Treasure Chests · Bosses · Inn · 15 Floors
# ══════════════════════════════════════════════════

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_print(text, delay=0.028):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def divider(char="═", n=50):
    print(char * n)

def pause(s=1.2):
    time.sleep(s)

# ══════════════════════════════════════════════════
#  STATUS EFFECTS
# ══════════════════════════════════════════════════
STATUS = {
    "poison":  {"emoji": "☠️",  "desc": "Loses HP each turn"},
    "burn":    {"emoji": "🔥",  "desc": "Loses HP, ATK lowered"},
    "stun":    {"emoji": "⚡",  "desc": "Skips a turn"},
    "frozen":  {"emoji": "❄️",  "desc": "Cannot act, takes bonus damage"},
    "bleed":   {"emoji": "🩸",  "desc": "Loses HP, cannot heal fully"},
    "cursed":  {"emoji": "💜",  "desc": "Halves all damage dealt"},
    "blessed": {"emoji": "✨",  "desc": "Heals a little each turn"},
    "berserk": {"emoji": "😡",  "desc": "+50% ATK, -30% DEF"},
    "shielded":{"emoji": "🛡️", "desc": "Block next attack"},
    "death_mark":{"emoji":"💀", "desc": "Next attack triples"},
    "resurrection_ready":{"emoji":"🌟","desc":"Revive on death"},
}

# ══════════════════════════════════════════════════
#  EQUIPMENT DATA
# ══════════════════════════════════════════════════
WEAPONS = [
    {"name": "Rusty Sword",    "atk": 0,  "price": 0,   "desc": "Starting blade"},
    {"name": "Iron Sword",     "atk": 6,  "price": 20,  "desc": "Reliable steel"},
    {"name": "Shadow Blade",   "atk": 12, "price": 45,  "desc": "Ignores 3 DEF"},
    {"name": "Flame Sword",    "atk": 18, "price": 80,  "desc": "Burns on hit (20%)"},
    {"name": "Dragon Fang",    "atk": 28, "price": 140, "desc": "Legendary weapon"},
]
ARMORS = [
    {"name": "Cloth Robe",     "def": 0,  "price": 0,   "desc": "Starting armor"},
    {"name": "Leather Armor",  "def": 5,  "price": 18,  "desc": "Basic protection"},
    {"name": "Chain Mail",     "def": 10, "price": 40,  "desc": "Good defense"},
    {"name": "Shadow Cloak",   "def": 14, "price": 75,  "desc": "Dodge chance +10%"},
    {"name": "Dragon Scale",   "def": 22, "price": 130, "desc": "Near-impenetrable"},
]
ACCESSORIES = [
    {"name": "None",            "bonus": {},                  "price": 0,  "desc": "Nothing"},
    {"name": "Lucky Charm",     "bonus": {"crit": 10},        "price": 25, "desc": "+10% crit chance"},
    {"name": "Mana Ring",       "bonus": {"mp_regen": 3},     "price": 30, "desc": "+3 MP per turn"},
    {"name": "Warrior's Band",  "bonus": {"atk": 5},          "price": 35, "desc": "+5 ATK"},
    {"name": "Guardian Amulet", "bonus": {"block": 15},       "price": 40, "desc": "+15% block chance"},
    {"name": "Sage's Pendant",  "bonus": {"spell_power": 15}, "price": 50, "desc": "+15% spell damage"},
]

# ══════════════════════════════════════════════════
#  ALL CLASS SKILLS
# ══════════════════════════════════════════════════
ALL_SKILLS = {
    "Warrior": [
        {"name":"Shield Bash",  "mp":8,  "desc":"Dmg + stun",          "unlocked_at":1},
        {"name":"Whirlwind",    "mp":14, "desc":"2–4 quick hits",       "unlocked_at":3},
        {"name":"Berserk Mode", "mp":20, "desc":"+50% ATK for 3 turns", "unlocked_at":5},
        {"name":"Earthquake",   "mp":28, "desc":"Massive single blow",  "unlocked_at":8},
    ],
    "Mage": [
        {"name":"Fireball",     "mp":10, "desc":"Burns enemy (25%)",    "unlocked_at":1},
        {"name":"Blizzard",     "mp":14, "desc":"Freezes enemy (30%)",  "unlocked_at":3},
        {"name":"Thunder",      "mp":18, "desc":"Stuns enemy (35%)",    "unlocked_at":5},
        {"name":"Meteor Strike","mp":30, "desc":"Devastating blow",     "unlocked_at":8},
    ],
    "Rogue": [
        {"name":"Shadowstep",   "mp":8,  "desc":"Ignores defense",      "unlocked_at":1},
        {"name":"Poison Blade", "mp":12, "desc":"Poisons enemy",        "unlocked_at":3},
        {"name":"Smoke Bomb",   "mp":10, "desc":"Escape + bleed",       "unlocked_at":5},
        {"name":"Death Mark",   "mp":25, "desc":"Next attack x3",       "unlocked_at":8},
    ],
    "Paladin": [
        {"name":"Holy Strike",    "mp":10, "desc":"Dmg + self-heal",      "unlocked_at":1},
        {"name":"Divine Shield",  "mp":12, "desc":"Block next attack",    "unlocked_at":3},
        {"name":"Smite",          "mp":20, "desc":"Dmg + curse enemy",    "unlocked_at":5},
        {"name":"Resurrection",   "mp":40, "desc":"Revive if fallen",     "unlocked_at":8},
    ],
}

# ══════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════
class Hero:
    def __init__(self, name, cls):
        self.name  = name
        self.cls   = cls
        self.level = 1
        self.xp    = 0
        self.xp_next = 35
        self.gold  = 15
        self.potions = 2
        self.elixirs = 0
        self.statuses = {}
        self.kills    = 0
        self.floors_cleared = 0

        self.weapon    = WEAPONS[0].copy()
        self.armor     = ARMORS[0].copy()
        self.accessory = ACCESSORIES[0].copy()

        base = {
            "Warrior": {"hp":130,"atk":16,"defense":10,"mp":25,"sp":1.0},
            "Mage":    {"hp":75, "atk":10,"defense":4, "mp":70,"sp":1.4},
            "Rogue":   {"hp":100,"atk":20,"defense":6, "mp":35,"sp":1.1},
            "Paladin": {"hp":115,"atk":14,"defense":12,"mp":40,"sp":1.2},
        }[cls]

        self.max_hp   = base["hp"]
        self.hp       = base["hp"]
        self.base_atk = base["atk"]
        self.base_def = base["defense"]
        self.mp       = base["mp"]
        self.max_mp   = base["mp"]
        self.sp_power = base["sp"]

        self.skills = [s.copy() for s in ALL_SKILLS[cls] if s["unlocked_at"] <= 1]

    @property
    def atk(self):
        a = self.base_atk + self.weapon["atk"] + self.accessory["bonus"].get("atk", 0)
        if "berserk" in self.statuses:
            a = int(a * 1.5)
        return a

    @property
    def defense(self):
        d = self.base_def + self.armor["def"]
        if "berserk" in self.statuses:
            d = int(d * 0.7)
        if "frozen" in self.statuses:
            d = int(d * 0.6)
        return d

    def is_alive(self):
        return self.hp > 0

    def unlock_skills(self):
        current_names = {s["name"] for s in self.skills}
        for s in ALL_SKILLS[self.cls]:
            if s["unlocked_at"] <= self.level and s["name"] not in current_names:
                self.skills.append(s.copy())
                slow_print(f"  🌟 NEW SKILL UNLOCKED: {s['name']}! — {s['desc']}")

    def apply_status_tick(self):
        to_remove = []
        for st, turns in list(self.statuses.items()):
            if st == "poison":
                dmg = random.randint(4, 8)
                self.hp = max(0, self.hp - dmg)
                slow_print(f"  ☠️  Poison deals {dmg} damage!")
            elif st == "burn":
                dmg = random.randint(3, 6)
                self.hp = max(0, self.hp - dmg)
                slow_print(f"  🔥 Burn deals {dmg} damage!")
            elif st == "bleed":
                dmg = random.randint(2, 5)
                self.hp = max(0, self.hp - dmg)
                slow_print(f"  🩸 Bleed deals {dmg} damage!")
            elif st == "blessed":
                heal = random.randint(4, 8)
                self.hp = min(self.max_hp, self.hp + heal)
                slow_print(f"  ✨ Blessing restores {heal} HP!")
            elif st == "mp_regen":
                self.mp = min(self.max_mp, self.mp + self.accessory["bonus"].get("mp_regen", 0))
            if st not in ("death_mark", "resurrection_ready", "shielded"):
                self.statuses[st] = turns - 1
                if self.statuses[st] <= 0:
                    to_remove.append(st)
        for st in to_remove:
            del self.statuses[st]
            slow_print(f"  ✅ {st.capitalize()} wore off.")

    def add_status(self, status, turns):
        self.statuses[status] = turns
        emoji = STATUS.get(status, {}).get("emoji", "❓")
        slow_print(f"  {emoji} You are now {status}! ({turns} turns)")

    def show_stats(self):
        status_str = " ".join([STATUS.get(s,{}).get("emoji","?") for s in self.statuses]) or "—"
        print(f"  🧙 {self.name} [{self.cls}]  Lv.{self.level}  {status_str}")
        print(f"  ❤️  HP : {self.hp}/{self.max_hp}    💎 MP : {self.mp}/{self.max_mp}")
        print(f"  ⚔️  ATK: {self.atk}   🛡️  DEF: {self.defense}")
        print(f"  🗡️  {self.weapon['name']} (+{self.weapon['atk']} ATK)  |  🥋 {self.armor['name']} (+{self.armor['def']} DEF)")
        print(f"  💍 {self.accessory['name']}")
        print(f"  ✨ XP: {self.xp}/{self.xp_next}   💰 Gold: {self.gold}   🧪 Potions: {self.potions}   💊 Elixirs: {self.elixirs}")
        if self.skills:
            print(f"  🌟 Skills: {', '.join([s['name'] for s in self.skills])}")

    def normal_attack(self, enemy):
        if self.armor["name"] == "Shadow Cloak" and random.random() < 0.10:
            slow_print(f"  💨 {enemy.name} attacks — but you dodge!")
            return 0
        if self.accessory["bonus"].get("block") and random.random() < self.accessory["bonus"]["block"] / 100:
            slow_print(f"  🛡️  Blocked!")
            return 0
        crit_chance = 0.15 + self.accessory["bonus"].get("crit", 0) / 100
        crit = random.random() < crit_chance
        ignore_def = 3 if self.weapon["name"] == "Shadow Blade" else 0
        dmg = max(1, self.atk - max(0, enemy.defense - ignore_def) + random.randint(-3, 6))
        if crit:
            dmg = int(dmg * 1.9)
            slow_print(f"  💥 CRITICAL! {self.name} deals {dmg} damage!")
        else:
            slow_print(f"  ⚔️  {self.name} attacks for {dmg} damage!")
        if self.weapon["name"] == "Flame Sword" and random.random() < 0.20:
            enemy.add_status("burn", 3)
        enemy.hp -= dmg
        return dmg

    def use_skill(self, skill, enemy):
        if self.mp < skill["mp"]:
            slow_print(f"  ❌ Not enough MP! Need {skill['mp']}.")
            return False
        self.mp -= skill["mp"]
        name = skill["name"]
        sp   = self.sp_power * (1 + self.accessory["bonus"].get("spell_power", 0) / 100)

        if name == "Shield Bash":
            dmg = int((self.atk * 1.2 + random.randint(8, 15)))
            slow_print(f"  🛡️  Shield Bash! {dmg} damage!")
            enemy.hp -= dmg
            if random.random() < 0.4:
                enemy.add_status("stun", 1)

        elif name == "Whirlwind":
            hits  = random.randint(2, 4)
            total = sum(max(1, int(self.atk * 0.6 + random.randint(3, 8))) for _ in range(hits))
            slow_print(f"  🌀 Whirlwind hits {hits}x for {total} total damage!")
            enemy.hp -= total

        elif name == "Berserk Mode":
            self.statuses["berserk"] = 3
            slow_print(f"  😡 BERSERK MODE! +50% ATK for 3 turns!")

        elif name == "Earthquake":
            dmg = int((self.atk * 2.5 + random.randint(20, 35)) * sp)
            slow_print(f"  🌍 EARTHQUAKE! {dmg} damage!")
            enemy.hp -= dmg

        elif name == "Fireball":
            dmg = int((40 + random.randint(-8, 12)) * sp)
            slow_print(f"  🔥 Fireball! {dmg} damage!")
            enemy.hp -= dmg
            if random.random() < 0.25:
                enemy.add_status("burn", 3)

        elif name == "Blizzard":
            dmg = int((38 + random.randint(-6, 10)) * sp)
            slow_print(f"  ❄️  Blizzard! {dmg} damage!")
            enemy.hp -= dmg
            if random.random() < 0.30:
                enemy.add_status("frozen", 2)

        elif name == "Thunder":
            dmg = int((44 + random.randint(-8, 14)) * sp)
            slow_print(f"  ⚡ Thunder! {dmg} damage!")
            enemy.hp -= dmg
            if random.random() < 0.35:
                enemy.add_status("stun", 1)

        elif name == "Meteor Strike":
            dmg = int((90 + random.randint(-10, 20)) * sp)
            slow_print(f"  ☄️  METEOR STRIKE! {dmg} damage!")
            enemy.hp -= dmg

        elif name == "Shadowstep":
            dmg = self.atk * 2 + random.randint(10, 20)
            slow_print(f"  🌑 Shadowstep! Bypass defense — {dmg} damage!")
            enemy.hp -= dmg

        elif name == "Poison Blade":
            dmg = max(1, self.atk - enemy.defense + random.randint(5, 10))
            slow_print(f"  🗡️  Poison Blade! {dmg} damage + poison!")
            enemy.hp -= dmg
            enemy.add_status("poison", 4)

        elif name == "Smoke Bomb":
            enemy.add_status("bleed", 3)
            slow_print(f"  💨 Smoke Bomb! Enemy bleeding for 3 turns!")
            return "escape_ready"

        elif name == "Death Mark":
            self.statuses["death_mark"] = 1
            slow_print(f"  💀 DEATH MARK charged! Next attack x3!")

        elif name == "Holy Strike":
            dmg = int((self.atk * 1.4 + random.randint(10, 18)) * sp)
            slow_print(f"  ✝️  Holy Strike! {dmg} damage!")
            enemy.hp -= dmg
            heal = random.randint(8, 16)
            self.hp = min(self.max_hp, self.hp + heal)
            slow_print(f"  ✨ Restored {heal} HP!")

        elif name == "Divine Shield":
            self.statuses["shielded"] = 1
            slow_print(f"  🛡️  Divine Shield! Next attack blocked!")

        elif name == "Smite":
            dmg = int((50 + random.randint(-10, 15)) * sp)
            slow_print(f"  ⚡ SMITE! {dmg} damage!")
            enemy.hp -= dmg
            enemy.add_status("cursed", 3)

        elif name == "Resurrection":
            self.statuses["resurrection_ready"] = 99
            slow_print(f"  🌟 Resurrection charged! You'll rise if you fall!")

        return True

    def use_potion(self):
        if self.potions <= 0:
            slow_print("  ❌ No potions!")
            return
        heal = random.randint(28, 45)
        self.hp = min(self.max_hp, self.hp + heal)
        self.potions -= 1
        slow_print(f"  🧪 Potion used! +{heal} HP ({self.potions} left)")

    def use_elixir(self):
        if self.elixirs <= 0:
            slow_print("  ❌ No elixirs!")
            return
        self.hp  = self.max_hp
        self.mp  = self.max_mp
        self.elixirs -= 1
        slow_print(f"  💊 Elixir! Fully restored! ({self.elixirs} left)")

    def gain_xp(self, amount):
        self.xp += amount
        slow_print(f"  ✨ +{amount} XP!")
        while self.xp >= self.xp_next:
            self.level_up()

    def level_up(self):
        self.level   += 1
        self.xp      -= self.xp_next
        self.xp_next  = int(self.xp_next * 1.45)
        hp_g  = random.randint(12, 20)
        atk_g = random.randint(2,  5)
        def_g = random.randint(1,  3)
        mp_g  = random.randint(6, 12)
        self.max_hp  += hp_g
        self.hp       = self.max_hp
        self.base_atk += atk_g
        self.base_def += def_g
        self.max_mp  += mp_g
        self.mp       = self.max_mp
        divider()
        slow_print(f"  🎉 LEVEL UP! Now Level {self.level}!")
        slow_print(f"     +{hp_g} HP  +{atk_g} ATK  +{def_g} DEF  +{mp_g} MP")
        self.unlock_skills()
        divider()


# ══════════════════════════════════════════════════
#  ENEMY
# ══════════════════════════════════════════════════
class Enemy:
    def __init__(self, name, hp, atk, defense, xp, gold, emoji,
                 skills=None, weakness=None, boss=False):
        self.name     = name
        self.hp       = hp
        self.max_hp   = hp
        self.atk      = atk
        self.defense  = defense
        self.xp       = xp
        self.gold     = gold
        self.emoji    = emoji
        self.skills   = skills or []
        self.weakness = weakness
        self.boss     = boss
        self.statuses = {}

    def is_alive(self):
        return self.hp > 0

    def add_status(self, status, turns):
        self.statuses[status] = turns
        emoji = STATUS.get(status, {}).get("emoji", "❓")
        slow_print(f"  {emoji} {self.name} is now {status}!")

    def apply_status_tick(self):
        to_remove = []
        for st, turns in list(self.statuses.items()):
            if st in ("poison", "burn", "bleed"):
                dmg = random.randint(5, 10)
                self.hp = max(0, self.hp - dmg)
                slow_print(f"  {STATUS.get(st,{}).get('emoji','💥')} {self.name} takes {dmg} from {st}!")
            self.statuses[st] = turns - 1
            if self.statuses[st] <= 0:
                to_remove.append(st)
        for st in to_remove:
            del self.statuses[st]

    def attack(self, hero):
        if "stun" in self.statuses or "frozen" in self.statuses:
            slow_print(f"  {self.name} is immobilised!")
            return 0
        if "shielded" in hero.statuses:
            slow_print(f"  🛡️  Divine Shield blocks the attack!")
            del hero.statuses["shielded"]
            return 0
        miss = random.random() < 0.08
        if miss:
            slow_print(f"  💨 {self.name} missed!")
            return 0
        if self.boss and self.skills and random.random() < 0.35:
            return self._boss_skill(hero)
        dmg = max(1, self.atk - hero.defense + random.randint(-3, 5))
        if "cursed" in self.statuses:
            dmg = max(1, dmg // 2)
        slow_print(f"  {self.emoji} {self.name} attacks for {dmg} damage!")
        hero.hp -= dmg
        return dmg

    def _boss_skill(self, hero):
        skill = random.choice(self.skills)
        slow_print(f"  {self.emoji} {self.name} uses {skill['name']}!")
        pause(0.4)
        dmg = skill.get("dmg", 0)
        if dmg:
            actual = max(1, dmg - hero.defense // 2 + random.randint(-5, 8))
            hero.hp -= actual
            slow_print(f"  💥 {actual} damage!")
        if "status" in skill:
            hero.add_status(skill["status"], skill.get("turns", 2))
        return dmg

    def hp_bar(self):
        bar_len = 22
        filled  = int((max(0, self.hp) / self.max_hp) * bar_len)
        bar     = "█" * filled + "░" * (bar_len - filled)
        st_str  = " ".join([STATUS.get(s,{}).get("emoji","?") for s in self.statuses]) if self.statuses else ""
        print(f"  {self.emoji} {self.name}  [{bar}] {max(0,self.hp)}/{self.max_hp} HP  {st_str}")
        if self.weakness:
            print(f"     🔍 Weak to: {self.weakness}")


# ══════════════════════════════════════════════════
#  ENEMY POOL
# ══════════════════════════════════════════════════
def normal_enemies():
    return [
        Enemy("Slime",        35,  6, 1, 10,  3,  "🟢"),
        Enemy("Goblin",       50,  9, 2, 16,  5,  "👺"),
        Enemy("Skeleton",     60, 13, 3, 22,  8,  "💀", weakness="fire"),
        Enemy("Orc Warrior",  80, 16, 6, 30, 11,  "🐗"),
        Enemy("Witch",        65, 20, 2, 35, 13,  "🧙‍♀️", weakness="frost"),
        Enemy("Vampire",      85, 22, 5, 42, 16,  "🧛"),
        Enemy("Golem",       110, 18,14, 48, 18,  "🗿", weakness="thunder"),
        Enemy("Dark Knight",  95, 25, 8, 55, 20,  "🖤"),
        Enemy("Werewolf",     90, 28, 7, 52, 19,  "🐺"),
        Enemy("Shadow Mage",  75, 30, 3, 60, 22,  "🌑"),
        Enemy("Lich",        105, 27, 6, 65, 25,  "☠️", weakness="holy"),
        Enemy("Demon",       120, 32,10, 72, 28,  "😈"),
    ]

def make_bosses():
    return {
        3:  Enemy("Cave Troll",   180, 22,  8,  80,  35, "🗿", boss=True,
                  skills=[{"name":"Rock Slam","dmg":28},
                           {"name":"Tremor","dmg":18,"status":"stun","turns":1},
                           {"name":"Boulder Hurl","dmg":35}]),
        6:  Enemy("Shadow Drake", 260, 28, 12, 120,  55, "🐍", boss=True,
                  skills=[{"name":"Poison Breath","dmg":20,"status":"poison","turns":4},
                           {"name":"Tail Whip","dmg":32},
                           {"name":"Shadow Bite","dmg":40}]),
        10: Enemy("Vampire Lord", 340, 35, 14, 160,  80, "🧛‍♂️", boss=True,
                  skills=[{"name":"Blood Drain","dmg":38},
                           {"name":"Curse","dmg":15,"status":"cursed","turns":3},
                           {"name":"Bat Storm","dmg":28,"status":"bleed","turns":3},
                           {"name":"Nightmare","dmg":45}]),
        15: Enemy("Dragon Lord",  500, 45, 18, 260, 150, "🐲", boss=True,
                  skills=[{"name":"Dragon Breath","dmg":55,"status":"burn","turns":4},
                           {"name":"Tail Crush","dmg":48},
                           {"name":"Fear Roar","dmg":20,"status":"cursed","turns":2},
                           {"name":"Inferno","dmg":70}]),
    }

def get_enemy(floor):
    pool = normal_enemies()
    if floor <= 2:
        return random.choice(pool[:3])
    elif floor <= 5:
        return random.choice(pool[2:6])
    elif floor <= 9:
        return random.choice(pool[4:9])
    else:
        return random.choice(pool[7:])


# ══════════════════════════════════════════════════
#  TREASURE CHEST
# ══════════════════════════════════════════════════
def open_treasure(hero):
    divider()
    slow_print("  📦 You found a TREASURE CHEST!")
    pause(0.5)
    roll = random.random()
    if roll < 0.22:
        gold = random.randint(15, 35)
        hero.gold += gold
        slow_print(f"  💰 Found {gold} gold!")
    elif roll < 0.42:
        hero.potions += random.randint(1, 2)
        slow_print("  🧪 Found potions!")
    elif roll < 0.55:
        hero.elixirs += 1
        slow_print("  💊 Found an Elixir!")
    elif roll < 0.68:
        g = random.randint(3, 7)
        hero.base_atk += g
        slow_print(f"  ⚔️  Power gem! +{g} ATK!")
    elif roll < 0.80:
        g = random.randint(3, 6)
        hero.base_def += g
        slow_print(f"  🛡️  Armor shard! +{g} DEF!")
    elif roll < 0.90:
        g = random.randint(10, 20)
        hero.max_mp += g
        hero.mp = min(hero.max_mp, hero.mp + g)
        slow_print(f"  💎 Mana crystal! +{g} MP!")
    else:
        slow_print("  💀 MIMIC! It bites you!")
        dmg = random.randint(15, 30)
        hero.hp = max(1, hero.hp - dmg)
        slow_print(f"  Took {dmg} damage!")
    divider()
    pause(1.2)


# ══════════════════════════════════════════════════
#  INN
# ══════════════════════════════════════════════════
def visit_inn(hero):
    cost = 8 + hero.level * 2
    clear()
    divider()
    slow_print("  🏨 TRAVELER'S INN")
    divider()
    slow_print(f"  Full restore (HP, MP, remove debuffs) for {cost} gold?")
    print(f"\n  [1] Rest ({cost}g)   [2] Leave\n")
    divider()
    c = input("  > ").strip()
    if c == "1":
        if hero.gold >= cost:
            hero.gold -= cost
            hero.hp = hero.max_hp
            hero.mp = hero.max_mp
            hero.statuses.clear()
            slow_print("  😴 You rest deeply... Fully restored! All statuses cleared.")
        else:
            slow_print("  ❌ Not enough gold.")
    pause(1.2)


# ══════════════════════════════════════════════════
#  SHOP
# ══════════════════════════════════════════════════
def visit_shop(hero):
    while True:
        clear()
        divider()
        slow_print("  🏪 BLACKSMITH & ITEM SHOP")
        divider()
        print("  ── CONSUMABLES ──")
        print("  [1] Potion         8g   Restore 28-45 HP")
        print("  [2] Elixir        25g   Full HP & MP")
        print("  [3] Antidote       6g   Remove all debuffs")
        print()
        print("  ── WEAPONS ──")
        for i, w in enumerate(WEAPONS[1:], 4):
            eq = " ◄ EQUIPPED" if hero.weapon["name"] == w["name"] else ""
            print(f"  [{i}] {w['name']:<16} {w['price']}g  +{w['atk']} ATK  {w['desc']}{eq}")
        print()
        print("  ── ARMOR ──")
        for i, a in enumerate(ARMORS[1:], 8):
            eq = " ◄ EQUIPPED" if hero.armor["name"] == a["name"] else ""
            print(f"  [{i}] {a['name']:<16} {a['price']}g  +{a['def']} DEF  {a['desc']}{eq}")
        print()
        print("  ── ACCESSORIES ──")
        for i, ac in enumerate(ACCESSORIES[1:], 12):
            eq = " ◄ EQUIPPED" if hero.accessory["name"] == ac["name"] else ""
            print(f"  [{i}] {ac['name']:<16} {ac['price']}g  {ac['desc']}{eq}")
        print()
        print("  [0] Leave shop")
        divider()
        print(f"  💰 Gold: {hero.gold}")
        divider()

        c = input("  Choose: ").strip()
        if c == "0":
            break
        elif c == "1":
            if hero.gold >= 8:
                hero.gold -= 8; hero.potions += 1
                slow_print("  🧪 Bought a Potion!")
            else:
                slow_print("  ❌ Not enough gold.")
        elif c == "2":
            if hero.gold >= 25:
                hero.gold -= 25; hero.elixirs += 1
                slow_print("  💊 Bought an Elixir!")
            else:
                slow_print("  ❌ Not enough gold.")
        elif c == "3":
            if hero.gold >= 6:
                hero.gold -= 6; hero.statuses.clear()
                slow_print("  🍵 Antidote used! Debuffs cleared.")
            else:
                slow_print("  ❌ Not enough gold.")
        else:
            try:
                idx = int(c)
                if 4 <= idx <= 7:
                    w = WEAPONS[idx - 3]
                    if hero.gold >= w["price"]:
                        if hero.weapon["atk"] >= w["atk"]:
                            slow_print(f"  ⚠️  Already have better weapon.")
                        else:
                            hero.gold -= w["price"]
                            hero.weapon = w.copy()
                            slow_print(f"  ⚔️  Equipped {w['name']}!")
                    else:
                        slow_print("  ❌ Not enough gold.")
                elif 8 <= idx <= 11:
                    a = ARMORS[idx - 7]
                    if hero.gold >= a["price"]:
                        if hero.armor["def"] >= a["def"]:
                            slow_print(f"  ⚠️  Already have better armor.")
                        else:
                            hero.gold -= a["price"]
                            hero.armor = a.copy()
                            slow_print(f"  🥋 Equipped {a['name']}!")
                    else:
                        slow_print("  ❌ Not enough gold.")
                elif 12 <= idx <= 16:
                    ac = ACCESSORIES[idx - 11]
                    if hero.gold >= ac["price"]:
                        hero.gold -= ac["price"]
                        hero.accessory = ac.copy()
                        slow_print(f"  💍 Equipped {ac['name']}!")
                    else:
                        slow_print("  ❌ Not enough gold.")
                else:
                    slow_print("  ❓ Invalid.")
            except ValueError:
                slow_print("  ❓ Invalid.")
        pause(1.0)


# ══════════════════════════════════════════════════
#  RANDOM FLOOR EVENT
# ══════════════════════════════════════════════════
def floor_event(hero, floor):
    roll = random.random()
    if roll < 0.20:
        open_treasure(hero)
    elif roll < 0.32:
        clear(); divider()
        slow_print("  🛒 A wandering merchant appears!")
        print("  [1] Potion (6g)  [2] Elixir (20g)  [3] Ignore")
        c = input("  > ").strip()
        if c == "1" and hero.gold >= 6:
            hero.gold -= 6; hero.potions += 1; slow_print("  🧪 Bought!")
        elif c == "2" and hero.gold >= 20:
            hero.gold -= 20; hero.elixirs += 1; slow_print("  💊 Bought!")
        pause(1.2)
    elif roll < 0.42:
        clear(); divider()
        slow_print("  🏛️  A healing shrine glows softly...")
        heal = random.randint(15, 30)
        mp_r = random.randint(8, 18)
        hero.hp = min(hero.max_hp, hero.hp + heal)
        hero.mp = min(hero.max_mp, hero.mp + mp_r)
        slow_print(f"  ✨ Restored {heal} HP and {mp_r} MP!")
        divider(); pause(1.2)
    elif roll < 0.48:
        clear(); divider()
        slow_print("  ⚠️  A trap springs!")
        dmg = random.randint(10, 22)
        hero.hp = max(1, hero.hp - dmg)
        slow_print(f"  💥 You take {dmg} damage!")
        divider(); pause(1.2)


# ══════════════════════════════════════════════════
#  BATTLE
# ══════════════════════════════════════════════════
def battle(hero, enemy):
    clear()
    divider()
    if enemy.boss:
        slow_print(f"  ⚠️  BOSS: {enemy.emoji} {enemy.name}!")
        slow_print("  Prepare for a tough fight!")
    else:
        slow_print(f"  ⚔️  A wild {enemy.emoji} {enemy.name} appears!")
    divider()
    pause(1.0)

    turn = 0
    while hero.is_alive() and enemy.is_alive():
        turn += 1

        hero.apply_status_tick()
        enemy.apply_status_tick()
        if not hero.is_alive():
            break

        # Mana Ring regen
        if hero.accessory["bonus"].get("mp_regen"):
            hero.mp = min(hero.max_mp, hero.mp + hero.accessory["bonus"]["mp_regen"])

        clear()
        print(f"\n  ─── Turn {turn} ───")
        enemy.hp_bar()
        print()
        hero.show_stats()
        divider()
        print("  [1] Attack           [2] Use Skill")
        print("  [3] Use Potion       [4] Use Elixir")
        print("  [5] Defend (-40% dmg)[6] Run Away")
        divider()

        action = input("  Action: ").strip()
        defending = False

        if action == "1":
            if "death_mark" in hero.statuses:
                slow_print("  💀 DEATH MARK TRIGGERS!")
                base_dmg = hero.normal_attack(enemy)
                bonus    = base_dmg * 2
                enemy.hp -= bonus
                slow_print(f"  ⚡ +{bonus} bonus damage from Death Mark!")
                del hero.statuses["death_mark"]
            else:
                hero.normal_attack(enemy)

        elif action == "2":
            if not hero.skills:
                slow_print("  ❌ No skills!"); continue
            print()
            for i, s in enumerate(hero.skills, 1):
                print(f"  [{i}] {s['name']:<16} {s['mp']} MP  {s['desc']}")
            print("  [0] Cancel")
            sc = input("  Skill: ").strip()
            if sc == "0":
                continue
            try:
                skill  = hero.skills[int(sc) - 1]
                result = hero.use_skill(skill, enemy)
                if result == "escape_ready":
                    slow_print("  💨 Escaped with Smoke Bomb!")
                    pause(1); return "escaped"
                if not result:
                    continue
            except:
                slow_print("  ❓ Invalid."); continue

        elif action == "3":
            hero.use_potion()
        elif action == "4":
            hero.use_elixir()
        elif action == "5":
            defending = True
            slow_print("  🛡️  Bracing for impact...")
        elif action == "6":
            if enemy.boss:
                slow_print("  ❌ You can't flee from a boss!")
            elif random.random() < 0.38:
                slow_print("  🏃 Escaped!"); pause(1); return "escaped"
            else:
                slow_print("  ❌ Couldn't escape!")
        else:
            slow_print("  ❓ Invalid.")

        # Enemy attacks
        if enemy.is_alive():
            dmg = enemy.attack(hero)
            if defending and dmg > 0:
                reduction = int(dmg * 0.4)
                hero.hp   = min(hero.max_hp, hero.hp + reduction)
                slow_print(f"  🛡️  Defense reduced damage by {reduction}!")

        # Resurrection
        if not hero.is_alive() and "resurrection_ready" in hero.statuses:
            del hero.statuses["resurrection_ready"]
            hero.hp = hero.max_hp // 2
            slow_print("  🌟 RESURRECTION! You rise from the dead with half HP!")
            pause(1)

        pause(0.5)

    if hero.is_alive():
        divider()
        slow_print(f"  🏆 Victory! {enemy.name} defeated!")
        hero.kills += 1
        loot = enemy.gold + random.randint(-3, 8)
        hero.gold += loot
        hero.gain_xp(enemy.xp)
        slow_print(f"  💰 Looted {loot} gold!")
        if random.random() < 0.15:
            hero.potions += 1
            slow_print("  🎁 Rare drop: Potion!")
        pause(1.5)
        return "win"
    else:
        divider()
        slow_print(f"  💀 {hero.name} has fallen...")
        pause(2)
        return "lose"


# ══════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════
def main():
    clear()
    divider("═")
    slow_print("  🐉  DRAGON QUEST — EXPANDED EDITION  🐉")
    slow_print("  Equipment · Skills · Bosses · Status Effects")
    divider("═")
    pause(0.5)

    name = input("\n  Hero name: ").strip() or "Hero"
    divider()
    print("\n  Choose your class:\n")
    print("  [1] Warrior  — Tanky, strong physical, berserk mode")
    print("  [2] Mage     — Fragile, devastating spells, AoE")
    print("  [3] Rogue    — Fast, poison & death mark combos")
    print("  [4] Paladin  — Self-heal, curses, resurrection")
    divider()

    cls = {"1":"Warrior","2":"Mage","3":"Rogue","4":"Paladin"}.get(
        input("  Choice (1-4): ").strip(), "Warrior")

    hero   = Hero(name, cls)
    bosses = make_bosses()

    clear(); divider()
    slow_print(f"  Welcome, {hero.name} the {cls}!")
    slow_print("  Conquer 15 floors. Defeat the Dragon Lord!")
    slow_print("  ⚠️  Bosses at floors 3, 6, 10 and 15!")
    divider(); pause(2)

    floor        = 1
    total_floors = 15

    while hero.is_alive() and floor <= total_floors:

        # ── BOSS FLOOR ──────────────────────────
        if floor in bosses:
            clear(); divider("═")
            slow_print(f"  ⚠️  FLOOR {floor} — BOSS BATTLE!")
            divider("═"); pause(0.8)
            boss = bosses[floor]
            boss.hp       = boss.max_hp  # reset if re-entered
            boss.statuses = {}
            result = battle(hero, boss)
            if result == "win":
                hero.floors_cleared += 1
                floor += 1
            elif result == "lose":
                break
            else:
                slow_print("  ⚠️  Can't escape a boss! Try again.")
                pause(1)
            continue

        # ── NORMAL FLOOR ────────────────────────
        clear(); divider()
        slow_print(f"  🏰 FLOOR {floor} / {total_floors}")
        divider()
        print("  [1] Explore      (fight + chance of event)")
        print("  [2] View stats")
        print("  [3] Visit Shop")
        print("  [4] Rest at Inn")
        print("  [5] Quit")
        divider()

        c = input("  What do you do? ").strip()

        if c == "1":
            floor_event(hero, floor)
            if not hero.is_alive():
                break
            enemy  = get_enemy(floor)
            result = battle(hero, enemy)
            if result == "win":
                hero.floors_cleared += 1
                floor += 1
            elif result == "lose":
                break
        elif c == "2":
            clear(); divider(); hero.show_stats(); divider()
            input("  Press Enter...")
        elif c == "3":
            visit_shop(hero)
        elif c == "4":
            visit_inn(hero)
        elif c == "5":
            slow_print("  👋 Farewell, hero!"); return
        else:
            slow_print("  ❓ Invalid choice.")

    # ── END SCREEN ──────────────────────────────
    clear(); divider("═")
    if floor > total_floors:
        slow_print("  🎉 YOU WIN! THE DRAGON LORD IS DEFEATED!")
        slow_print(f"  {hero.name} is crowned the greatest hero of all time! 👑")
    else:
        slow_print("  💀 GAME OVER")
        slow_print(f"  {hero.name} fell on Floor {floor}.")
    divider("═")
    print(f"\n  Class          : {hero.cls}")
    print(f"  Final Level    : {hero.level}")
    print(f"  Floors Cleared : {hero.floors_cleared}")
    print(f"  Enemies Slain  : {hero.kills}")
    print(f"  Gold Collected : {hero.gold}")
    print(f"  Weapon         : {hero.weapon['name']}")
    print(f"  Armor          : {hero.armor['name']}")
    print(f"  Accessory      : {hero.accessory['name']}")
    divider("═")
    slow_print("  Thanks for playing Dragon Quest Expanded! 🐉\n")

    again = input("  Play again? (y/n): ").strip().lower()
    if again == "y":
        main()


if __name__ == "__main__":
    main()