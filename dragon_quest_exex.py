import random
import time
import os

# ═══════════════════════════════════════════════════════════════════
#   🐉  DRAGON QUEST — MAXIMUM EDITION
#   40 Floors · 8 Bosses · 6 Classes · Companions · Talent Tree
#   30+ Enemies · Achievements · Gambling · Bank · Reputation
#   10 Skills/Class · Expanded Crafting · Side Dungeons · Lore
# ═══════════════════════════════════════════════════════════════════

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_print(text, delay=0.024):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def divider(char="═", n=54):
    print(char * n)

def pause(s=1.1):
    time.sleep(s)

def hp_bar(cur, mx, length=22):
    filled = int((max(0, cur) / max(1, mx)) * length)
    return "█" * filled + "░" * (length - filled)

def pct_bar(cur, mx, length=16):
    filled = int((max(0, cur) / max(1, mx)) * length)
    return "▓" * filled + "░" * (length - filled)

# ═══════════════════════════════════════════════════════════════════
#  STATUS EFFECTS
# ═══════════════════════════════════════════════════════════════════
STATUS = {
    "poison":      {"emoji":"☠️",  "tick":"dmg", "amount":(5,11)},
    "burn":        {"emoji":"🔥",  "tick":"dmg", "amount":(4,9)},
    "bleed":       {"emoji":"🩸",  "tick":"dmg", "amount":(3,7)},
    "acid":        {"emoji":"🟢",  "tick":"dmg", "amount":(6,14)},
    "stun":        {"emoji":"⚡",  "tick":"skip"},
    "frozen":      {"emoji":"❄️",  "tick":"skip"},
    "cursed":      {"emoji":"💜",  "tick":"none"},
    "blind":       {"emoji":"🌫️", "tick":"none"},
    "weakened":    {"emoji":"📉",  "tick":"none"},
    "marked":      {"emoji":"🎯",  "tick":"none"},
    "berserk":     {"emoji":"😡",  "tick":"none"},
    "empowered":   {"emoji":"💪",  "tick":"none"},
    "blessed":     {"emoji":"✨",  "tick":"heal", "amount":(5,10)},
    "regen":       {"emoji":"💚",  "tick":"heal", "amount":(8,16)},
    "shielded":    {"emoji":"🛡️", "tick":"none"},
    "death_mark":  {"emoji":"💀",  "tick":"none"},
    "resurrection_ready":{"emoji":"🌟","tick":"none"},
    "soul_link":   {"emoji":"🔗",  "tick":"none"},
    "enraged":     {"emoji":"🔴",  "tick":"none"},
    "vampiric":    {"emoji":"🧛",  "tick":"none"},
    "hasted":      {"emoji":"💨",  "tick":"none"},
    "petrified":   {"emoji":"🗿",  "tick":"skip"},
    "doom":        {"emoji":"⏳",  "tick":"countdown"},
    "barrier":     {"emoji":"🔷",  "tick":"none"},
}

# ═══════════════════════════════════════════════════════════════════
#  EQUIPMENT TIERS
# ═══════════════════════════════════════════════════════════════════
WEAPONS = [
    {"name":"Rusty Sword",       "atk":0,  "price":0,   "tier":0, "desc":"Starting blade"},
    {"name":"Iron Sword",        "atk":6,  "price":18,  "tier":1, "desc":"Reliable"},
    {"name":"Steel Sword",       "atk":11, "price":35,  "tier":1, "desc":"Sharp steel"},
    {"name":"Shadow Blade",      "atk":17, "price":60,  "tier":2, "desc":"Ignores 5 DEF"},
    {"name":"Flame Sword",       "atk":23, "price":90,  "tier":2, "desc":"Burns 20%"},
    {"name":"Thunder Blade",     "atk":28, "price":125, "tier":3, "desc":"Stuns 18%"},
    {"name":"Frost Edge",        "atk":32, "price":155, "tier":3, "desc":"Freezes 22%"},
    {"name":"Void Saber",        "atk":40, "price":200, "tier":4, "desc":"Bleeds 28%, ignores 8 DEF"},
    {"name":"Soul Reaper",       "atk":48, "price":265, "tier":4, "desc":"Steals 15% dmg as HP"},
    {"name":"Dragon Fang",       "atk":58, "price":340, "tier":5, "desc":"Burns+bleeds 30%"},
    {"name":"Celestial Blade",   "atk":72, "price":450, "tier":5, "desc":"Ultimate +25% all spells"},
    {"name":"Godslayer",         "atk":90, "price":600, "tier":6, "desc":"Mythic. All procs at once"},
]
ARMORS = [
    {"name":"Cloth Robe",        "def":0,  "price":0,   "tier":0, "desc":"Starting"},
    {"name":"Leather Armor",     "def":5,  "price":15,  "tier":1, "desc":"Basic"},
    {"name":"Studded Leather",   "def":9,  "price":30,  "tier":1, "desc":"Reinforced"},
    {"name":"Chain Mail",        "def":14, "price":55,  "tier":2, "desc":"Solid"},
    {"name":"Shadow Cloak",      "def":18, "price":80,  "tier":2, "desc":"+14% dodge"},
    {"name":"Knight Plate",      "def":25, "price":120, "tier":3, "desc":"Heavy protection"},
    {"name":"Void Armor",        "def":32, "price":170, "tier":4, "desc":"Reflects 10% dmg"},
    {"name":"Dragon Scale",      "def":42, "price":240, "tier":5, "desc":"Near-impenetrable"},
    {"name":"Celestial Robe",    "def":54, "price":330, "tier":5, "desc":"+20% max MP"},
    {"name":"Aegis Plate",       "def":68, "price":480, "tier":6, "desc":"Mythic. +25% all block"},
]
ACCESSORIES = [
    {"name":"None",              "bonus":{},                            "price":0,   "tier":0, "desc":"Nothing"},
    {"name":"Lucky Charm",       "bonus":{"crit":10},                   "price":22,  "tier":1, "desc":"+10% crit"},
    {"name":"Mana Ring",         "bonus":{"mp_regen":4},                "price":28,  "tier":1, "desc":"+4 MP/turn"},
    {"name":"Warrior's Band",    "bonus":{"atk":6},                     "price":35,  "tier":1, "desc":"+6 ATK"},
    {"name":"Guardian Amulet",   "bonus":{"block":15},                  "price":42,  "tier":2, "desc":"+15% block"},
    {"name":"Sage's Pendant",    "bonus":{"spell_power":22},            "price":55,  "tier":2, "desc":"+22% spell dmg"},
    {"name":"Berserker Ring",    "bonus":{"atk":12,"crit":10},          "price":80,  "tier":3, "desc":"+12 ATK +10% crit"},
    {"name":"Vampiric Fang",     "bonus":{"lifesteal":18},              "price":95,  "tier":3, "desc":"+18% lifesteal"},
    {"name":"Phoenix Feather",   "bonus":{"revive":True},               "price":110, "tier":3, "desc":"Auto-revive once"},
    {"name":"Dragon Eye",        "bonus":{"all":14},                    "price":160, "tier":4, "desc":"+14 all stats"},
    {"name":"Arcane Heart",      "bonus":{"spell_power":35,"mp_regen":6},"price":200,"tier":4, "desc":"+35% spell, +6 MP/turn"},
    {"name":"Titan Gauntlet",    "bonus":{"atk":20,"block":20},        "price":260, "tier":5, "desc":"+20 ATK +20% block"},
    {"name":"Godstone",          "bonus":{"all":22,"crit":15,"block":15},"price":400,"tier":6, "desc":"Mythic. Everything."},
]

# Crafting
CRAFT_RECIPES = {
    ("Iron Sword",    "Steel Sword"):     ("Shadow Blade",   "weapon"),
    ("Flame Sword",   "Thunder Blade"):   ("Void Saber",     "weapon"),
    ("Void Saber",    "Dragon Fang"):     ("Celestial Blade","weapon"),
    ("Chain Mail",    "Shadow Cloak"):    ("Void Armor",     "armor"),
    ("Void Armor",    "Dragon Scale"):    ("Celestial Robe", "armor"),
    ("Lucky Charm",   "Warrior's Band"):  ("Berserker Ring", "acc"),
    ("Sage's Pendant","Mana Ring"):       ("Arcane Heart",   "acc"),
    ("Berserker Ring","Dragon Eye"):      ("Titan Gauntlet", "acc"),
    ("Celestial Blade","Celestial Robe"): ("Godslayer",      "weapon"),
}

# ═══════════════════════════════════════════════════════════════════
#  TALENTS (Passive upgrades bought with Talent Points)
# ═══════════════════════════════════════════════════════════════════
TALENT_TREE = {
    "Iron Body":     {"desc":"+20 max HP permanently",      "cost":1, "effect":"max_hp",  "amount":20},
    "Sharp Mind":    {"desc":"+15 max MP permanently",      "cost":1, "effect":"max_mp",  "amount":15},
    "Battle Hardened":{"desc":"+4 DEF permanently",        "cost":1, "effect":"base_def","amount":4},
    "Killer Instinct":{"desc":"+4 ATK permanently",        "cost":1, "effect":"base_atk","amount":4},
    "Lucky Strike":  {"desc":"+8% crit chance globally",   "cost":2, "effect":"global_crit","amount":8},
    "Thick Skin":    {"desc":"Reduce all damage by 8%",    "cost":2, "effect":"dmg_reduce","amount":8},
    "Bloodthirst":   {"desc":"+10% lifesteal on attacks",  "cost":2, "effect":"lifesteal","amount":10},
    "Arcane Mastery":{"desc":"+15% spell power globally",  "cost":2, "effect":"global_sp","amount":15},
    "Giant Slayer":  {"desc":"+25% dmg to bosses/elites",  "cost":3, "effect":"boss_dmg", "amount":25},
    "Iron Will":     {"desc":"Survive lethal hit at 1 HP (once/floor)","cost":3,"effect":"iron_will","amount":1},
    "Mana Fountain": {"desc":"+8 MP every turn passively", "cost":3, "effect":"mp_regen_passive","amount":8},
    "Berserker Soul":{"desc":"+2% ATK per 10% HP missing", "cost":3, "effect":"rage_atk","amount":2},
    "Ancient Knowledge":{"desc":"+20% XP from all sources","cost":2,"effect":"xp_bonus","amount":20},
    "Gold Sense":    {"desc":"+25% gold from all sources", "cost":2, "effect":"gold_bonus","amount":25},
    "Toughness":     {"desc":"+30 max HP + +5 DEF",        "cost":3, "effect":"tough",   "amount":30},
    "Spell Surge":   {"desc":"10% chance to cast skill twice","cost":4,"effect":"spell_surge","amount":10},
}

# ═══════════════════════════════════════════════════════════════════
#  COMPANIONS
# ═══════════════════════════════════════════════════════════════════
COMPANIONS = [
    {"name":"Mira the Healer",  "emoji":"💉", "hire_cost":40,  "upkeep":5,
     "ability":"Heals 15-30 HP each turn", "type":"heal",   "power":22},
    {"name":"Rex the Warrior",  "emoji":"⚔️", "hire_cost":50,  "upkeep":6,
     "ability":"Deals 60% of your ATK each turn", "type":"atk", "power":60},
    {"name":"Luna the Mage",    "emoji":"🔮", "hire_cost":55,  "upkeep":7,
     "ability":"Casts random spell for 30-55 dmg", "type":"spell","power":42},
    {"name":"Shade the Rogue",  "emoji":"🗡️","hire_cost":45,  "upkeep":5,
     "ability":"50% chance to poison enemy each turn","type":"poison","power":4},
    {"name":"Golem Guardian",   "emoji":"🗿", "hire_cost":70,  "upkeep":8,
     "ability":"Absorbs 20% of damage you take","type":"tank","power":20},
    {"name":"Lyra the Bard",    "emoji":"🎵", "hire_cost":35,  "upkeep":4,
     "ability":"Grants +10% ATK and +5 MP each turn","type":"buff","power":10},
]

# ═══════════════════════════════════════════════════════════════════
#  CLASS SKILLS  (10 per class)
# ═══════════════════════════════════════════════════════════════════
ALL_SKILLS = {
    "Warrior": [
        {"name":"Shield Bash",    "mp":8,  "desc":"Dmg + 40% stun",           "ul":1},
        {"name":"Whirlwind",      "mp":14, "desc":"2-5 quick hits",            "ul":3},
        {"name":"Berserk Mode",   "mp":20, "desc":"+60% ATK 3 turns",          "ul":5},
        {"name":"War Cry",        "mp":16, "desc":"Weaken enemy -25% ATK",     "ul":7},
        {"name":"Earthquake",     "mp":28, "desc":"Massive ground slam",       "ul":9},
        {"name":"Titan Smash",    "mp":35, "desc":"2× ATK ignores all DEF",    "ul":12},
        {"name":"Unbreakable",    "mp":25, "desc":"Block 2 turns",             "ul":15},
        {"name":"Battle Cry",     "mp":22, "desc":"Empower self +30% 4 turns", "ul":18},
        {"name":"Ragnarok",       "mp":50, "desc":"Triple ATK self-bleed",     "ul":22},
        {"name":"World Breaker",  "mp":70, "desc":"Destroy enemy DEF + 4× hit","ul":28},
    ],
    "Mage": [
        {"name":"Fireball",       "mp":10, "desc":"Burns 25%",                 "ul":1},
        {"name":"Blizzard",       "mp":14, "desc":"Freezes 30%",               "ul":3},
        {"name":"Thunder",        "mp":18, "desc":"Stuns 35%",                 "ul":5},
        {"name":"Arcane Bolt",    "mp":12, "desc":"Pure magic ignores DEF",    "ul":7},
        {"name":"Meteor Strike",  "mp":30, "desc":"Devastating impact",        "ul":9},
        {"name":"Chain Lightning","mp":35, "desc":"Hits 3 times with stun",    "ul":12},
        {"name":"Blizzard Storm", "mp":42, "desc":"Freeze + massive dmg",      "ul":15},
        {"name":"Mana Surge",     "mp":0,  "desc":"Sacrifice HP for MP",       "ul":18},
        {"name":"Armageddon",     "mp":65, "desc":"Catastrophic spell",        "ul":22},
        {"name":"Big Bang",       "mp":90, "desc":"Ultimate destruction",      "ul":28},
    ],
    "Rogue": [
        {"name":"Shadowstep",     "mp":8,  "desc":"Bypass all DEF",            "ul":1},
        {"name":"Poison Blade",   "mp":12, "desc":"Poison 5 turns",            "ul":3},
        {"name":"Smoke Bomb",     "mp":10, "desc":"Bleed + escape",            "ul":5},
        {"name":"Mark Target",    "mp":8,  "desc":"+30% dmg taken 4 turns",    "ul":7},
        {"name":"Death Mark",     "mp":25, "desc":"Next attack ×3",            "ul":9},
        {"name":"Shadow Clone",   "mp":30, "desc":"Attack twice this turn",    "ul":12},
        {"name":"Vanish",         "mp":20, "desc":"Skip enemy turn",           "ul":15},
        {"name":"Acid Splash",    "mp":18, "desc":"Acid dmg + acid status",    "ul":18},
        {"name":"Assassination",  "mp":45, "desc":"60% of enemy max HP",       "ul":22},
        {"name":"Oblivion Strike","mp":60, "desc":"Ignore HP, deal flat 999",  "ul":28},
    ],
    "Paladin": [
        {"name":"Holy Strike",    "mp":10, "desc":"Dmg + self-heal",           "ul":1},
        {"name":"Divine Shield",  "mp":12, "desc":"Block next attack",         "ul":3},
        {"name":"Smite",          "mp":20, "desc":"Dmg + curse enemy",         "ul":5},
        {"name":"Consecrate",     "mp":15, "desc":"Regen + blessed 4 turns",   "ul":7},
        {"name":"Resurrection",   "mp":40, "desc":"Revive on death",           "ul":9},
        {"name":"Holy Nova",      "mp":35, "desc":"Dmg + heal + cleanse",      "ul":12},
        {"name":"Sacred Flame",   "mp":28, "desc":"Burns + blinds enemy",      "ul":15},
        {"name":"Aura of Light",  "mp":30, "desc":"Barrier absorbs 60 dmg",    "ul":18},
        {"name":"Divine Judgment","mp":55, "desc":"Massive holy + regen",      "ul":22},
        {"name":"Holy Apocalypse","mp":80, "desc":"Ultimate holy destruction",  "ul":28},
    ],
    "Necromancer": [
        {"name":"Drain Life",     "mp":12, "desc":"Steal HP from enemy",       "ul":1},
        {"name":"Bone Spear",     "mp":10, "desc":"Piercing bone projectile",  "ul":3},
        {"name":"Curse of Decay", "mp":14, "desc":"Poison + weaken enemy",     "ul":5},
        {"name":"Soul Rend",      "mp":20, "desc":"Tears soul, heavy dmg",     "ul":7},
        {"name":"Raise Dead",     "mp":25, "desc":"Undead ally attacks once",  "ul":9},
        {"name":"Death Coil",     "mp":18, "desc":"Dmg + self-heal 30%",       "ul":12},
        {"name":"Plague",         "mp":30, "desc":"Poison+acid+bleed all at once","ul":15},
        {"name":"Soul Harvest",   "mp":35, "desc":"Heal fully from kills",     "ul":18},
        {"name":"Lich Form",      "mp":50, "desc":"Become lich: +50% all 5t",  "ul":22},
        {"name":"Death Nova",     "mp":75, "desc":"Massive AoE necrotic",      "ul":28},
    ],
    "Berserker": [
        {"name":"Cleave",         "mp":8,  "desc":"Heavy hit, ignores 4 DEF",  "ul":1},
        {"name":"Battle Rage",    "mp":12, "desc":"+40% ATK 4 turns",          "ul":3},
        {"name":"Bloodlust",      "mp":15, "desc":"Heal on every hit",         "ul":5},
        {"name":"Rampage",        "mp":20, "desc":"3-6 random hits",           "ul":7},
        {"name":"Enrage",         "mp":18, "desc":"More ATK as HP drops",      "ul":9},
        {"name":"Skull Crack",    "mp":25, "desc":"Dmg + stun + blind",        "ul":12},
        {"name":"Endless Fury",   "mp":35, "desc":"5 hits, each empowered",    "ul":15},
        {"name":"Blood Frenzy",   "mp":30, "desc":"Berserk + vampiric 3 turns","ul":18},
        {"name":"Obliterate",     "mp":55, "desc":"Crush with full strength",  "ul":22},
        {"name":"Armageddon Fist","mp":80, "desc":"Punch with the force of gods","ul":28},
    ],
}

# ═══════════════════════════════════════════════════════════════════
#  ACHIEVEMENTS
# ═══════════════════════════════════════════════════════════════════
ACHIEVEMENTS = {
    "First Blood":     {"desc":"Win your first battle",           "done":False,"reward":("gold",10)},
    "Centurion":       {"desc":"Kill 100 enemies",                "done":False,"reward":("xp",200)},
    "Dungeon Diver":   {"desc":"Reach floor 20",                  "done":False,"reward":("gold",80)},
    "Boss Slayer":     {"desc":"Defeat 5 bosses",                 "done":False,"reward":("xp",300)},
    "Untouchable":     {"desc":"Win a battle without taking dmg", "done":False,"reward":("gold",50)},
    "Millionaire":     {"desc":"Accumulate 500 gold",             "done":False,"reward":("xp",150)},
    "Skill Master":    {"desc":"Use skills 50 times",             "done":False,"reward":("gold",60)},
    "Arena Legend":    {"desc":"Win the Arena 5 times",           "done":False,"reward":("xp",250)},
    "Crafter":         {"desc":"Craft 5 items",                   "done":False,"reward":("gold",70)},
    "Quest Champion":  {"desc":"Complete 8 quests",               "done":False,"reward":("xp",180)},
    "Lucky Gambler":   {"desc":"Win 10 gambling bets",            "done":False,"reward":("gold",100)},
    "Lore Master":     {"desc":"Read all lore entries",           "done":False,"reward":("xp",120)},
    "Companion Bond":  {"desc":"Use a companion for 15 battles",  "done":False,"reward":("gold",90)},
    "Dragon Slayer":   {"desc":"Defeat the Dragon Lord",          "done":False,"reward":("xp",1000)},
    "Talentless":      {"desc":"Spend 10 talent points",          "done":False,"reward":("gold",120)},
    "Side Runner":     {"desc":"Complete 3 side dungeons",        "done":False,"reward":("xp",200)},
}

# ═══════════════════════════════════════════════════════════════════
#  HERO CLASS
# ═══════════════════════════════════════════════════════════════════
class Hero:
    def __init__(self, name, cls):
        self.name  = name
        self.cls   = cls
        self.level = 1
        self.xp    = 0
        self.xp_next = 45
        self.gold  = 25
        self.bank  = 0
        self.potions = 3
        self.elixirs = 0
        self.antidotes = 1
        self.statuses  = {}
        self.kills      = 0
        self.boss_kills = 0
        self.floors_cleared = 0
        self.quests_done    = 0
        self.arena_wins     = 0
        self.crafts_made    = 0
        self.skill_uses     = 0
        self.gambles_won    = 0
        self.total_dmg      = 0
        self.total_gold_earned = 0
        self.lore_read      = 0
        self.companion_battles = 0
        self.side_dungeons  = 0
        self.talent_points  = 0
        self.talents        = {}
        self.revive_used    = False
        self.iron_will_used = False
        self.achievements   = dict(ACHIEVEMENTS)
        self.companion      = None
        self.companion_battles_total = 0
        self.lore_entries_read = set()

        self.weapon    = WEAPONS[0].copy()
        self.armor     = ARMORS[0].copy()
        self.accessory = ACCESSORIES[0].copy()

        base = {
            "Warrior":    {"hp":145,"atk":18,"def":12,"mp":30, "sp":1.0},
            "Mage":       {"hp":80, "atk":10,"def":4, "mp":90, "sp":1.6},
            "Rogue":      {"hp":110,"atk":22,"def":7, "mp":42, "sp":1.1},
            "Paladin":    {"hp":125,"atk":14,"def":14,"mp":50, "sp":1.3},
            "Necromancer":{"hp":95, "atk":12,"def":6, "mp":80, "sp":1.5},
            "Berserker":  {"hp":160,"atk":25,"def":8, "mp":25, "sp":0.9},
        }[cls]

        self.max_hp   = base["hp"]
        self.hp       = base["hp"]
        self.base_atk = base["atk"]
        self.base_def = base["def"]
        self.mp       = base["mp"]
        self.max_mp   = base["mp"]
        self.sp_power = base["sp"]
        self.skills   = [s.copy() for s in ALL_SKILLS[cls] if s["ul"] <= 1]

    # ─── derived stats ────────────────────────────────────────────
    @property
    def atk(self):
        a = (self.base_atk + self.weapon["atk"]
             + self.accessory["bonus"].get("atk",0)
             + self.accessory["bonus"].get("all",0)
             + self.talents.get("Killer Instinct",0)*4
             + self.talents.get("Berserker Soul",0)*self._rage_bonus())
        if "berserk"   in self.statuses: a = int(a*1.6)
        if "empowered" in self.statuses: a = int(a*1.3)
        if "weakened"  in self.statuses: a = int(a*0.75)
        if "enraged"   in self.statuses: a = int(a*1.4)
        return max(1, a)

    def _rage_bonus(self):
        missing_pct = max(0, 100 - int(self.hp/max(1,self.max_hp)*100))
        return (missing_pct // 10) * self.talents.get("Berserker Soul", 0)

    @property
    def defense(self):
        d = (self.base_def + self.armor["def"]
             + self.accessory["bonus"].get("all",0)
             + self.talents.get("Battle Hardened",0)*4)
        if "berserk" in self.statuses: d = int(d*0.70)
        if "frozen"  in self.statuses: d = int(d*0.55)
        return max(0, d)

    def is_alive(self): return self.hp > 0

    def talent_value(self, key, default=0):
        return self.talents.get(key, default)

    def unlock_skills(self):
        have = {s["name"] for s in self.skills}
        for s in ALL_SKILLS[self.cls]:
            if s["ul"] <= self.level and s["name"] not in have:
                self.skills.append(s.copy())
                slow_print(f"  🌟 SKILL UNLOCKED: {s['name']}! — {s['desc']}")

    def apply_status_tick(self):
        rm = []
        for st, turns in list(self.statuses.items()):
            info = STATUS.get(st,{})
            tick = info.get("tick","none")
            if tick == "dmg":
                lo,hi = info.get("amount",(3,8))
                d = random.randint(lo,hi)
                red = self.talents.get("Thick Skin",0)*8//100
                d = max(1,d-red)
                self.hp = max(0,self.hp-d)
                slow_print(f"  {info['emoji']} {st}: -{d} HP!")
            elif tick == "heal":
                lo,hi = info.get("amount",(5,12))
                h = random.randint(lo,hi)
                self.hp = min(self.max_hp,self.hp+h)
                slow_print(f"  {info['emoji']} {st}: +{h} HP!")
            elif tick == "countdown":
                if turns <= 1:
                    slow_print(f"  ⏳ DOOM strikes! Instant death!")
                    self.hp = 0
            if st not in ("death_mark","resurrection_ready","shielded","vampiric","barrier"):
                self.statuses[st] = turns-1
                if self.statuses[st] <= 0: rm.append(st)
        for st in rm:
            del self.statuses[st]
            slow_print(f"  ✅ {st.capitalize()} wore off.")

        # passive mp regen from talent
        passive_mp = self.talents.get("Mana Fountain",0)*8
        if passive_mp:
            self.mp = min(self.max_mp, self.mp+passive_mp)

    def add_status(self, st, turns):
        self.statuses[st] = turns
        emoji = STATUS.get(st,{}).get("emoji","❓")
        slow_print(f"  {emoji} {self.name} is {st}! ({turns} turns)")

    def show_stats(self):
        st_str = " ".join(STATUS.get(s,{}).get("emoji","?") for s in self.statuses) or "—"
        bar    = hp_bar(self.hp, self.max_hp)
        mp_b   = pct_bar(self.mp, self.max_mp)
        print(f"  🧙 {self.name} [{self.cls}] Lv.{self.level}  {st_str}")
        print(f"  ❤️  [{bar}] {self.hp}/{self.max_hp}")
        print(f"  💎 [{mp_b}] {self.mp}/{self.max_mp}")
        print(f"  ⚔️  ATK:{self.atk}  🛡️ DEF:{self.defense}  ✨ Kills:{self.kills}")
        print(f"  🗡️  {self.weapon['name']}  🥋 {self.armor['name']}  💍 {self.accessory['name']}")
        print(f"  💰 {self.gold}g  🏦 {self.bank}g  🧪×{self.potions}  💊×{self.elixirs}  💉×{self.antidotes}")
        if self.companion:
            c = self.companion
            print(f"  🤝 Companion: {c['emoji']} {c['name']}")
        if self.skills:
            sk = ", ".join(s["name"] for s in self.skills[:5])
            if len(self.skills)>5: sk+=" ..."
            print(f"  🌟 Skills: {sk}")
        if self.talents:
            tl = ", ".join(self.talents.keys())
            print(f"  🧠 Talents: {tl}")

    def check_achievements(self):
        ach = self.achievements
        def check(key, cond):
            if not ach[key]["done"] and cond:
                ach[key]["done"] = True
                r = ach[key]["reward"]
                slow_print(f"  🏆 ACHIEVEMENT: {key}! — {ach[key]['desc']}")
                if r[0]=="gold": self.gold+=r[1]; slow_print(f"     +{r[1]} gold!")
                elif r[0]=="xp": self.gain_xp(r[1])
                divider(); pause(0.8)

        check("First Blood",    self.kills>=1)
        check("Centurion",      self.kills>=100)
        check("Dungeon Diver",  self.floors_cleared>=20)
        check("Boss Slayer",    self.boss_kills>=5)
        check("Millionaire",    self.total_gold_earned>=500)
        check("Skill Master",   self.skill_uses>=50)
        check("Arena Legend",   self.arena_wins>=5)
        check("Crafter",        self.crafts_made>=5)
        check("Quest Champion", self.quests_done>=8)
        check("Lucky Gambler",  self.gambles_won>=10)
        check("Lore Master",    len(self.lore_entries_read)>=6)
        check("Companion Bond", self.companion_battles_total>=15)
        check("Dragon Slayer",  self.floors_cleared>=40)
        check("Talentless",     sum(self.talents.values())>=10)
        check("Side Runner",    self.side_dungeons>=3)

    def normal_attack(self, enemy):
        if "blind" in self.statuses and random.random()<0.38:
            slow_print(f"  🌫️  Blind — you miss!"); return 0
        if self.armor["name"]=="Shadow Cloak" and random.random()<0.14:
            slow_print(f"  💨 Dodge!"); return 0
        block_chance = (self.accessory["bonus"].get("block",0)
                        + self.talents.get("Titan Gauntlet",{}) if isinstance(self.talents.get("Titan Gauntlet"),int) else 0)
        block_val = self.accessory["bonus"].get("block",0)
        if self.accessory["name"]=="Aegis Plate": block_val+=25
        if block_val and random.random()<block_val/100:
            slow_print(f"  🛡️  Blocked!"); return 0

        crit_base = 0.15 + self.accessory["bonus"].get("crit",0)/100 + self.talents.get("Lucky Strike",0)*8/100
        crit_base += self.accessory["bonus"].get("all",0)/200
        crit = random.random() < crit_base

        # DEF ignore
        ignore = 0
        wn = self.weapon["name"]
        if "Shadow" in wn: ignore=5
        if "Void" in wn:   ignore=8
        if "Celestial" in wn: ignore=10
        if wn=="Godslayer": ignore=15

        dmg = max(1, self.atk - max(0,enemy.defense-ignore) + random.randint(-4,8))

        # talent modifiers
        if "Thick Skin" not in self.talents:
            pass
        dr = self.talents.get("Thick Skin",0)*8/100
        if "marked" in enemy.statuses: dmg=int(dmg*1.30)
        if (self.talents.get("Giant Slayer",0) and (enemy.boss or enemy.elite)):
            dmg=int(dmg*1.25)
        if crit: dmg=int(dmg*2.1); slow_print(f"  💥 CRITICAL! {dmg} damage!")
        else:    slow_print(f"  ⚔️  {self.name} attacks for {dmg} damage!")

        # weapon procs
        if wn=="Flame Sword"    and random.random()<0.20: enemy.add_status("burn",3)
        if wn=="Thunder Blade"  and random.random()<0.18: enemy.add_status("stun",1)
        if wn=="Frost Edge"     and random.random()<0.22: enemy.add_status("frozen",2)
        if wn=="Void Saber"     and random.random()<0.28: enemy.add_status("bleed",3)
        if wn=="Soul Reaper":
            steal=int(dmg*0.15); self.hp=min(self.max_hp,self.hp+steal)
            slow_print(f"  🧛 Soul Reaper steals {steal} HP!")
        if wn=="Dragon Fang":
            if random.random()<0.30: enemy.add_status("burn",3)
            if random.random()<0.30: enemy.add_status("bleed",3)
        if wn=="Godslayer":
            for st in ["burn","bleed","poison","stun"]:
                if random.random()<0.25: enemy.add_status(st,2)

        # lifesteal
        ls = self.accessory["bonus"].get("lifesteal",0) + self.talents.get("Bloodthirst",0)*10
        if ls:
            h = int(dmg*ls/100); self.hp=min(self.max_hp,self.hp+h)
            if h: slow_print(f"  🧛 Lifesteal +{h} HP!")

        # Vampiric status
        if "vampiric" in self.statuses:
            h2=int(dmg*0.25); self.hp=min(self.max_hp,self.hp+h2)
            slow_print(f"  🧛 Vampiric +{h2} HP!")

        # Void Armor reflect
        if self.armor["name"]=="Void Armor" and random.random()<0.10:
            ref=int(dmg*0.10); enemy.hp-=ref; slow_print(f"  🔄 Reflected {ref}!")

        enemy.hp -= dmg
        self.total_dmg += dmg

        # Spell Surge (procs on skill, handled there)
        return dmg

    def use_skill(self, skill, enemy):
        name = skill["name"]
        mp   = skill["mp"]

        if name=="Mana Surge":
            cost=22
            if self.hp<=cost: slow_print("  ❌ Not enough HP!"); return False
            gain=min(self.max_mp-self.mp,35); self.hp-=cost; self.mp=min(self.max_mp,self.mp+gain)
            slow_print(f"  ⚡ Mana Surge! -{cost} HP, +{gain} MP!"); return True

        if self.mp<mp: slow_print(f"  ❌ Need {mp} MP (have {self.mp})."); return False
        self.mp -= mp
        self.skill_uses += 1

        sp = self.sp_power * (1+self.accessory["bonus"].get("spell_power",0)/100)
        sp *= (1+self.talents.get("Arcane Mastery",0)*15/100)
        if self.weapon["name"]=="Celestial Blade": sp*=1.25
        if self.weapon["name"]=="Godslayer": sp*=1.40

        def deal(d):
            if "marked" in enemy.statuses: d=int(d*1.30)
            if self.talents.get("Giant Slayer") and (enemy.boss or enemy.elite): d=int(d*1.25)
            enemy.hp-=d; self.total_dmg+=d

            # Spell Surge double-cast check
            if self.talents.get("Spell Surge") and random.random()<0.10:
                slow_print(f"  ⚡ SPELL SURGE! Casts again!")
                enemy.hp-=d; self.total_dmg+=d; return d*2
            return d

        # lifesteal on skill
        def maybe_steal(d):
            ls = self.accessory["bonus"].get("lifesteal",0) + self.talents.get("Bloodthirst",0)*10
            if ls:
                h=int(d*ls/100); self.hp=min(self.max_hp,self.hp+h)
                if h: slow_print(f"  🧛 +{h} HP lifesteal!")

        # ─ WARRIOR ────────────────────────────────────────────────
        if name=="Shield Bash":
            d=deal(int(self.atk*1.3+random.randint(10,20))); slow_print(f"  🛡️  Shield Bash! {d} dmg!")
            if random.random()<0.40: enemy.add_status("stun",1)
        elif name=="Whirlwind":
            hits=random.randint(2,5); total=sum(max(1,int(self.atk*0.65+random.randint(4,10))) for _ in range(hits))
            deal(total); slow_print(f"  🌀 Whirlwind! {hits} hits, {total} total!")
        elif name=="Berserk Mode":
            self.statuses["berserk"]=3; slow_print("  😡 BERSERK! +60% ATK for 3 turns!")
        elif name=="War Cry":
            enemy.add_status("weakened",3); slow_print("  📢 WAR CRY! Enemy weakened!")
        elif name=="Earthquake":
            d=deal(int((self.atk*2.8+random.randint(25,40))*sp)); slow_print(f"  🌍 EARTHQUAKE! {d} dmg!")
        elif name=="Titan Smash":
            sd=enemy.defense; enemy.defense=0
            d=deal(int(self.atk*2.2+random.randint(22,38))); enemy.defense=sd
            slow_print(f"  🔨 TITAN SMASH! {d} dmg, ignores DEF!")
        elif name=="Unbreakable":
            self.statuses["shielded"]=2; slow_print("  🛡️  UNBREAKABLE! 2 turns!")
        elif name=="Battle Cry":
            self.add_status("empowered",4); slow_print("  💪 Battle Cry! +30% ATK 4 turns!")
        elif name=="Ragnarok":
            d=deal(int(self.atk*3.2+random.randint(30,55))); self.add_status("bleed",3)
            slow_print(f"  ⚡ RAGNAROK! {d} dmg! (self bleed)")
        elif name=="World Breaker":
            sd=enemy.defense; enemy.defense=0
            d=deal(int(self.atk*4.5+random.randint(40,70))); enemy.defense=sd
            slow_print(f"  🌎 WORLD BREAKER! {d} catastrophic dmg!")

        # ─ MAGE ────────────────────────────────────────────────────
        elif name=="Fireball":
            d=deal(int((48+random.randint(-8,15))*sp)); slow_print(f"  🔥 Fireball! {d} dmg!")
            if random.random()<0.25: enemy.add_status("burn",3)
        elif name=="Blizzard":
            d=deal(int((44+random.randint(-6,13))*sp)); slow_print(f"  ❄️  Blizzard! {d} dmg!")
            if random.random()<0.30: enemy.add_status("frozen",2)
        elif name=="Thunder":
            d=deal(int((52+random.randint(-8,16))*sp)); slow_print(f"  ⚡ Thunder! {d} dmg!")
            if random.random()<0.35: enemy.add_status("stun",1)
        elif name=="Arcane Bolt":
            d=int(self.base_atk*2.5+35*sp+random.randint(12,22)); deal(d)
            slow_print(f"  🔮 Arcane Bolt! {d} pure magic!")
        elif name=="Meteor Strike":
            d=deal(int((105+random.randint(-12,24))*sp)); slow_print(f"  ☄️  METEOR! {d} dmg!")
        elif name=="Chain Lightning":
            hits=3; total=0
            for _ in range(hits):
                d2=int((40+random.randint(-5,10))*sp); deal(d2); total+=d2
            slow_print(f"  ⚡ Chain Lightning! {hits} strikes, {total} total!")
            if random.random()<0.40: enemy.add_status("stun",1)
        elif name=="Blizzard Storm":
            d=deal(int((145+random.randint(-15,28))*sp)); enemy.add_status("frozen",3)
            slow_print(f"  🌨️  Blizzard Storm! {d} dmg + freeze!")
        elif name=="Armageddon":
            d=deal(int((210+random.randint(-20,40))*sp)); slow_print(f"  💥 ARMAGEDDON! {d} dmg!")
        elif name=="Big Bang":
            d=deal(int((320+random.randint(-25,55))*sp)); slow_print(f"  🌌 BIG BANG! {d} ULTIMATE dmg!")

        # ─ ROGUE ───────────────────────────────────────────────────
        elif name=="Shadowstep":
            d=int(self.atk*2.2+random.randint(16,28)); deal(d)
            slow_print(f"  🌑 Shadowstep! {d} dmg, bypasses DEF!")
        elif name=="Poison Blade":
            d=max(1,self.atk-enemy.defense+random.randint(7,14)); deal(d)
            slow_print(f"  🗡️  Poison Blade! {d} + 5 turns poison!"); enemy.add_status("poison",5)
        elif name=="Smoke Bomb":
            enemy.add_status("bleed",3); slow_print("  💨 Smoke Bomb! Bleed + escape!"); return "escape"
        elif name=="Mark Target":
            enemy.add_status("marked",4); slow_print("  🎯 Target marked! +30% dmg taken!")
        elif name=="Death Mark":
            self.statuses["death_mark"]=1; slow_print("  💀 DEATH MARK! Next attack ×3!")
        elif name=="Shadow Clone":
            d1=max(1,self.atk-enemy.defense+random.randint(-2,6))
            d2=max(1,self.atk-enemy.defense+random.randint(-2,6))
            deal(d1+d2); slow_print(f"  👥 Clone! {d1}+{d2}={d1+d2} total!")
        elif name=="Vanish":
            self.statuses["shielded"]=1; slow_print("  🌫️  Vanished! Enemy skips a turn!")
        elif name=="Acid Splash":
            d=deal(int((55+random.randint(-8,14))*sp)); enemy.add_status("acid",4)
            slow_print(f"  🟢 Acid Splash! {d} dmg + acid 4 turns!")
        elif name=="Assassination":
            d=int(enemy.max_hp*0.60); deal(d); slow_print(f"  🗡️  ASSASSINATION! {d} dmg!")
        elif name=="Oblivion Strike":
            d=min(999,enemy.hp-1) if enemy.hp>1 else 1; deal(d)
            slow_print(f"  ⚫ OBLIVION STRIKE! {d} dmg!")

        # ─ PALADIN ─────────────────────────────────────────────────
        elif name=="Holy Strike":
            d=deal(int((self.atk*1.55+random.randint(12,22))*sp))
            h=random.randint(12,24); self.hp=min(self.max_hp,self.hp+h)
            slow_print(f"  ✝️  Holy Strike! {d} dmg, +{h} HP!")
        elif name=="Divine Shield":
            self.statuses["shielded"]=1; slow_print("  🛡️  Divine Shield!")
        elif name=="Smite":
            d=deal(int((58+random.randint(-10,18))*sp)); enemy.add_status("cursed",3)
            slow_print(f"  ⚡ Smite! {d} dmg + cursed!")
        elif name=="Consecrate":
            self.add_status("regen",4); self.add_status("blessed",4)
            slow_print("  🌿 Consecrate! Regen+Blessed 4 turns!")
        elif name=="Resurrection":
            self.statuses["resurrection_ready"]=99; slow_print("  🌟 Resurrection armed!")
        elif name=="Holy Nova":
            d=deal(int((88+random.randint(-10,22))*sp)); h=random.randint(18,32)
            self.hp=min(self.max_hp,self.hp+h)
            self.statuses={k:v for k,v in self.statuses.items()
                           if k not in("poison","burn","bleed","cursed","frozen","stun","blind","acid")}
            slow_print(f"  💫 Holy Nova! {d} dmg +{h} HP, debuffs cleansed!")
        elif name=="Sacred Flame":
            d=deal(int((70+random.randint(-8,18))*sp)); enemy.add_status("burn",4); enemy.add_status("blind",3)
            slow_print(f"  🔥 Sacred Flame! {d} dmg + burn + blind!")
        elif name=="Aura of Light":
            self.statuses["barrier"]=60; slow_print("  🔷 Aura of Light! Barrier absorbs 60 dmg!")
        elif name=="Divine Judgment":
            d=deal(int((165+random.randint(-15,32))*sp)); h=random.randint(22,38)
            self.hp=min(self.max_hp,self.hp+h); self.add_status("regen",5)
            slow_print(f"  ⚡ DIVINE JUDGMENT! {d} dmg +{h} HP!")
        elif name=="Holy Apocalypse":
            d=deal(int((280+random.randint(-20,50))*sp)); h=int(d*0.30)
            self.hp=min(self.max_hp,self.hp+h); self.statuses.clear()
            slow_print(f"  🌟 HOLY APOCALYPSE! {d} dmg! Healed {h}! All debuffs cleared!")

        # ─ NECROMANCER ─────────────────────────────────────────────
        elif name=="Drain Life":
            d=deal(int((50+random.randint(-8,14))*sp)); self.hp=min(self.max_hp,self.hp+d//2)
            slow_print(f"  🧛 Drain Life! {d} dmg, +{d//2} HP!")
        elif name=="Bone Spear":
            d=deal(int((55+random.randint(-6,16))*sp)); slow_print(f"  🦴 Bone Spear! {d} piercing dmg!")
        elif name=="Curse of Decay":
            enemy.add_status("poison",5); enemy.add_status("weakened",3)
            slow_print("  💀 Curse of Decay! Poisoned+weakened!")
        elif name=="Soul Rend":
            d=deal(int((80+random.randint(-10,20))*sp)); slow_print(f"  💀 Soul Rend! {d} dmg!")
        elif name=="Raise Dead":
            undead_dmg=int(self.atk*1.8+random.randint(15,30)); deal(undead_dmg)
            slow_print(f"  🧟 Undead ally attacks for {undead_dmg} dmg!")
        elif name=="Death Coil":
            d=deal(int((70+random.randint(-8,18))*sp)); h=int(d*0.35)
            self.hp=min(self.max_hp,self.hp+h); slow_print(f"  🌀 Death Coil! {d} dmg, +{h} HP!")
        elif name=="Plague":
            for st in ["poison","acid","bleed"]: enemy.add_status(st,4)
            slow_print("  🟢 Plague! Poison+Acid+Bleed for 4 turns!")
        elif name=="Soul Harvest":
            self.hp=self.max_hp; self.mp=min(self.max_mp,self.mp+20)
            slow_print("  💀 Soul Harvest! Fully healed!")
        elif name=="Lich Form":
            for st in ["berserk","regen","empowered"]: self.statuses[st]=5
            slow_print("  💀 LICH FORM! Empowered 5 turns!")
        elif name=="Death Nova":
            d=deal(int((250+random.randint(-20,45))*sp)); slow_print(f"  ☠️  DEATH NOVA! {d} necrotic dmg!")

        # ─ BERSERKER ───────────────────────────────────────────────
        elif name=="Cleave":
            ignore2=4; d=max(1,self.atk-max(0,enemy.defense-ignore2)+random.randint(5,18))
            deal(d); slow_print(f"  🪓 Cleave! {d} dmg!")
        elif name=="Battle Rage":
            self.add_status("empowered",4); slow_print("  😤 Battle Rage! +40% ATK 4 turns!")
        elif name=="Bloodlust":
            self.add_status("vampiric",4); slow_print("  🧛 Bloodlust! Vampiric 4 turns!")
        elif name=="Rampage":
            hits=random.randint(3,6); total=sum(max(1,int(self.atk*0.7+random.randint(5,12))) for _ in range(hits))
            deal(total); slow_print(f"  🔥 Rampage! {hits} hits, {total} total!")
        elif name=="Enrage":
            self.add_status("enraged",4); slow_print("  🔴 ENRAGED! Damage scales with HP loss!")
        elif name=="Skull Crack":
            d=deal(int(self.atk*1.8+random.randint(15,25)))
            enemy.add_status("stun",1); enemy.add_status("blind",2)
            slow_print(f"  💥 Skull Crack! {d} dmg + stun + blind!")
        elif name=="Endless Fury":
            hits=5; total=sum(int(self.atk*0.9+random.randint(8,16)) for _ in range(hits))
            deal(total); slow_print(f"  ⚡ Endless Fury! 5 empowered hits = {total} total!")
        elif name=="Blood Frenzy":
            self.statuses["berserk"]=3; self.statuses["vampiric"]=3
            slow_print("  🩸 Blood Frenzy! Berserk+Vampiric 3 turns!")
        elif name=="Obliterate":
            d=deal(int(self.atk*3.8+random.randint(35,60))); slow_print(f"  💢 OBLITERATE! {d} dmg!")
        elif name=="Armageddon Fist":
            d=deal(int(self.atk*6.0+random.randint(60,100))); slow_print(f"  👊 ARMAGEDDON FIST! {d} GODLIKE dmg!")

        maybe_steal(self.total_dmg)  # rough steal, compensated above
        return True

    def use_potion(self):
        if self.potions<=0: slow_print("  ❌ No potions!"); return
        h=random.randint(32,55); self.hp=min(self.max_hp,self.hp+h)
        self.potions-=1; slow_print(f"  🧪 Potion! +{h} HP ({self.potions} left)")

    def use_elixir(self):
        if self.elixirs<=0: slow_print("  ❌ No elixirs!"); return
        self.hp=self.max_hp; self.mp=self.max_mp
        self.elixirs-=1; slow_print(f"  💊 Elixir! Fully restored!")

    def use_antidote(self):
        if self.antidotes<=0: slow_print("  ❌ No antidotes!"); return
        cleared=[s for s in list(self.statuses) if s in("poison","burn","bleed","acid","cursed","blind","weakened")]
        for s in cleared: del self.statuses[s]
        self.antidotes-=1
        slow_print(f"  💉 Antidote! Cleared: {', '.join(cleared) if cleared else 'nothing'}.")

    def gain_xp(self, amount):
        bonus = int(amount * self.talents.get("Ancient Knowledge",0)*20/100)
        amount += bonus
        self.xp+=amount; slow_print(f"  ✨ +{amount} XP!")
        while self.xp>=self.xp_next: self.level_up()

    def level_up(self):
        self.level+=1; self.xp-=self.xp_next; self.xp_next=int(self.xp_next*1.40)
        hp=random.randint(14,24); a=random.randint(2,5); d=random.randint(1,3); m=random.randint(8,14)
        self.max_hp+=hp; self.hp=self.max_hp
        self.base_atk+=a; self.base_def+=d; self.max_mp+=m; self.mp=self.max_mp
        self.talent_points+=1
        divider()
        slow_print(f"  🎉 LEVEL UP! Now Level {self.level}!")
        slow_print(f"     +{hp} HP  +{a} ATK  +{d} DEF  +{m} MP  +1 Talent Point")
        self.unlock_skills(); divider()

    def get_title(self):
        if self.floors_cleared>=40: return "🌟 Dragon Lord Slayer"
        if self.kills>=100: return "💀 Centurion"
        if self.boss_kills>=5: return "👑 Boss Destroyer"
        if self.arena_wins>=5: return "⚔️  Arena Legend"
        if self.crafts_made>=5: return "🔨 Master Crafter"
        if self.quests_done>=8: return "📋 Quest Champion"
        if self.level>=25: return "🦁 Veteran Hero"
        if self.floors_cleared>=20: return "🏰 Dungeon Diver"
        return "🗡️  Adventurer"


# ═══════════════════════════════════════════════════════════════════
#  ENEMY
# ═══════════════════════════════════════════════════════════════════
class Enemy:
    def __init__(self, name, hp, atk, defense, xp, gold, emoji,
                 skills=None, weakness=None, boss=False, elite=False):
        self.name=name; self.hp=hp; self.max_hp=hp; self.atk=atk
        self.defense=defense; self.xp=xp; self.gold=gold; self.emoji=emoji
        self.skills=skills or []; self.weakness=weakness
        self.boss=boss; self.elite=elite; self.statuses={}

    def is_alive(self): return self.hp>0

    def add_status(self, st, turns):
        self.statuses[st]=turns
        slow_print(f"  {STATUS.get(st,{}).get('emoji','❓')} {self.name} is {st}!")

    def apply_status_tick(self):
        rm=[]
        for st,turns in list(self.statuses.items()):
            info=STATUS.get(st,{}); tick=info.get("tick","none")
            if tick=="dmg":
                lo,hi=info.get("amount",(4,10)); d=random.randint(lo,hi)
                self.hp=max(0,self.hp-d)
                slow_print(f"  {info['emoji']} {self.name} takes {d} from {st}!")
            self.statuses[st]=turns-1
            if self.statuses[st]<=0: rm.append(st)
        for st in rm: del self.statuses[st]

    def attack(self, hero):
        if any(s in self.statuses for s in ("stun","frozen","petrified")):
            slow_print(f"  {self.name} can't move!"); return 0
        if "shielded" in hero.statuses:
            slow_print(f"  🛡️  Shield blocks!"); del hero.statuses["shielded"]; return 0
        if "barrier" in hero.statuses:
            barrier_hp=hero.statuses["barrier"]
            slow_print(f"  🔷 Barrier absorbs the hit!")
            hero.statuses["barrier"]=0; del hero.statuses["barrier"]; return 0
        if random.random()<0.08:
            slow_print(f"  💨 {self.name} missed!"); return 0
        if (self.boss or self.elite) and self.skills and random.random()<0.40:
            return self._special(hero)
        dmg=max(1,self.atk-hero.defense+random.randint(-4,7))
        if "cursed" in self.statuses: dmg=max(1,dmg//2)
        dr=hero.talents.get("Thick Skin",0)*8/100
        dmg=max(1,int(dmg*(1-dr)))
        slow_print(f"  {self.emoji} {self.name} attacks for {dmg} dmg!")
        hero.hp-=dmg

        # Iron Will talent
        if hero.hp<=0 and hero.talents.get("Iron Will") and not hero.iron_will_used:
            hero.hp=1; hero.iron_will_used=True
            slow_print("  💎 IRON WILL! Survived at 1 HP!")

        return dmg

    def _special(self,hero):
        skill=random.choice(self.skills)
        slow_print(f"  {self.emoji} {self.name}: {skill['name']}!")
        pause(0.4)
        dmg=skill.get("dmg",0)
        if dmg:
            dr=hero.talents.get("Thick Skin",0)*8/100
            actual=max(1,int((dmg-hero.defense//2+random.randint(-5,10))*(1-dr)))
            hero.hp-=actual; slow_print(f"  💥 {actual} dmg!")
        if "status" in skill:
            hero.add_status(skill["status"],skill.get("turns",2))
        return dmg

    def hp_bar_str(self):
        bar=hp_bar(self.hp,self.max_hp,24)
        tag=" ⭐ELITE" if self.elite else (" 💀BOSS" if self.boss else "")
        st_str=" ".join(STATUS.get(s,{}).get("emoji","?") for s in self.statuses)
        print(f"  {self.emoji}{tag} {self.name}")
        print(f"  [{bar}] {max(0,self.hp)}/{self.max_hp}  {st_str}")
        if self.weakness: print(f"  🔍 Weakness: {self.weakness}")


# ═══════════════════════════════════════════════════════════════════
#  ENEMY POOLS
# ═══════════════════════════════════════════════════════════════════
def make_normal_enemies():
    return [
        Enemy("Slime",          38,  6,  1, 10,  3, "🟢"),
        Enemy("Goblin",         52,  9,  2, 16,  5, "👺"),
        Enemy("Skeleton",       62, 13,  3, 22,  8, "💀",weakness="fire"),
        Enemy("Orc Warrior",    82, 16,  6, 30, 11, "🐗"),
        Enemy("Witch",          68, 20,  2, 35, 13, "🧙‍♀️"),
        Enemy("Vampire",        88, 22,  5, 42, 16, "🧛"),
        Enemy("Golem",         115, 18, 14, 48, 18, "🗿",weakness="thunder"),
        Enemy("Dark Knight",    98, 25,  8, 55, 20, "🖤"),
        Enemy("Werewolf",       92, 28,  7, 52, 19, "🐺"),
        Enemy("Shadow Mage",    78, 30,  3, 60, 22, "🌑"),
        Enemy("Lich",          108, 27,  6, 65, 25, "☠️",weakness="holy"),
        Enemy("Demon",         125, 32, 10, 72, 28, "😈"),
        Enemy("Chimera",       138, 34, 12, 80, 31, "🦁"),
        Enemy("Death Knight",  148, 36, 14, 88, 34, "🖤🗡️"),
        Enemy("Wyvern",        135, 38,  9, 82, 32, "🐉"),
        Enemy("Necromancer",   115, 34,  5, 90, 36, "🧟"),
        Enemy("Abyssal Fiend", 165, 40, 12, 98, 40, "👿"),
        Enemy("Infernal Drake",178, 42, 15,104, 43, "🔥🐲"),
        Enemy("Void Wraith",   145, 45,  8,108, 42, "🌀"),
        Enemy("Ancient Golem", 205, 35, 22,115, 46, "🗿⭐",weakness="thunder"),
        Enemy("Soul Devourer", 155, 48, 10,120, 48, "👁️"),
        Enemy("Hellhound",     135, 44,  8,112, 44, "🐕‍🦺"),
        Enemy("Phantom Archer",125, 50,  4,118, 46, "🏹"),
        Enemy("Chaos Knight",  180, 46, 18,125, 50, "⚔️"),
        Enemy("Elder Dragon",  220, 52, 16,135, 55, "🐲",weakness="ice"),
        Enemy("Doom Harbinger",200, 55, 14,140, 58, "⏳"),
        Enemy("Titan Spawn",   250, 50, 20,148, 62, "🦾"),
        Enemy("Void Leviathan",280, 58, 16,158, 68, "🦑"),
        Enemy("Shadow Titan",  265, 60, 22,162, 70, "🌑💪"),
        Enemy("Nightmare",     240, 62, 12,170, 72, "😱"),
    ]

def make_elite(floor):
    pool=make_normal_enemies()
    base=random.choice(pool[min(floor-1,len(pool)-1):min(floor+4,len(pool))])
    return Enemy(
        "Elite "+base.name, int(base.hp*2.0), int(base.atk*1.5), int(base.defense*1.4),
        int(base.xp*2.5), int(base.gold*2.2), base.emoji, elite=True,
        skills=[
            {"name":"Power Strike","dmg":int(base.atk*2.0)},
            {"name":"Vicious Blow","dmg":int(base.atk*2.5),"status":"bleed","turns":4},
            {"name":"Enrage","dmg":0,"status":"enraged","turns":3},
        ]
    )

def make_bosses():
    return {
        5:  Enemy("Iron Colossus",    280, 26, 10, 100, 50, "🤖", boss=True, skills=[
                {"name":"Steel Punch","dmg":32},{"name":"Tremor","dmg":22,"status":"stun","turns":1},
                {"name":"Iron Slam","dmg":40}]),
        10: Enemy("Shadow Drake",     420, 32, 14, 145, 70, "🐍", boss=True, skills=[
                {"name":"Poison Breath","dmg":25,"status":"poison","turns":5},
                {"name":"Tail Whip","dmg":38},{"name":"Shadow Bite","dmg":50}]),
        15: Enemy("Vampire Lord",     560, 40, 17, 195,100, "🧛‍♂️", boss=True, skills=[
                {"name":"Blood Drain","dmg":45},{"name":"Curse","dmg":20,"status":"cursed","turns":4},
                {"name":"Bat Storm","dmg":35,"status":"bleed","turns":4},{"name":"Nightmare","dmg":55}]),
        20: Enemy("Abyssal Titan",    740, 50, 21, 260,135, "👿", boss=True, skills=[
                {"name":"Void Crush","dmg":62},{"name":"Soul Drain","dmg":40,"status":"weakened","turns":3},
                {"name":"Dark Nova","dmg":56,"status":"cursed","turns":3},{"name":"Abyss Slam","dmg":75}]),
        25: Enemy("Death God",        920, 58, 25, 340,175, "💀👑", boss=True, skills=[
                {"name":"Death Touch","dmg":70,"status":"bleed","turns":5},
                {"name":"Soul Shatter","dmg":82},{"name":"Eternal Curse","dmg":45,"status":"cursed","turns":5},
                {"name":"Reaper's Blow","dmg":95}]),
        30: Enemy("Ancient Leviathan",1100,65,28, 420,220, "🦑", boss=True, skills=[
                {"name":"Tidal Crush","dmg":78},{"name":"Ink Cloud","dmg":50,"status":"blind","turns":4},
                {"name":"Void Tentacle","dmg":90,"status":"stun","turns":2},{"name":"Maelstrom","dmg":105}]),
        36: Enemy("Chaos Titan",     1350,75,32, 510,275, "🦾", boss=True, skills=[
                {"name":"Chaos Slam","dmg":90},{"name":"Entropy","dmg":70,"status":"weakened","turns":4},
                {"name":"Doom Pulse","dmg":0,"status":"doom","turns":3},{"name":"World Shatter","dmg":120}]),
        40: Enemy("Dragon Lord",     1800,88,38, 650,350, "🐲", boss=True, skills=[
                {"name":"Dragon Breath","dmg":85,"status":"burn","turns":6},
                {"name":"Tail Crush","dmg":75},{"name":"Fear Roar","dmg":30,"status":"cursed","turns":4},
                {"name":"Inferno Nova","dmg":100,"status":"blind","turns":3},
                {"name":"Ancient Fury","dmg":130},{"name":"World Flame","dmg":150}]),
    }

def get_enemy(floor):
    pool=make_normal_enemies()
    thresholds=[3,7,11,15,19,23,27,31,35]
    idx=0
    for i,t in enumerate(thresholds):
        if floor>t: idx=i+1
    start=min(idx*3,len(pool)-5)
    end=min(start+6,len(pool))
    return random.choice(pool[start:end])


# ═══════════════════════════════════════════════════════════════════
#  SIDE DUNGEONS
# ═══════════════════════════════════════════════════════════════════
SIDE_DUNGEONS = [
    {"name":"Crystal Caves",   "floors":3, "enemy_mult":1.1, "gold":60,  "xp":80,  "desc":"Ice-themed cavern"},
    {"name":"Haunted Crypt",   "floors":4, "enemy_mult":1.2, "gold":80,  "xp":100, "desc":"Undead stronghold"},
    {"name":"Lava Fortress",   "floors":4, "enemy_mult":1.3, "gold":95,  "xp":120, "desc":"Fire demons within"},
    {"name":"Void Sanctum",    "floors":5, "enemy_mult":1.5, "gold":130, "xp":160, "desc":"Dangerous void realm"},
    {"name":"Dragon's Lair",   "floors":5, "enemy_mult":1.6, "gold":150, "xp":180, "desc":"Packed with dragons"},
    {"name":"God's Tomb",      "floors":6, "enemy_mult":1.8, "gold":200, "xp":250, "desc":"Mythic difficulty"},
]

def run_side_dungeon(hero, qb, floor):
    clear(); divider()
    slow_print("  🗺️  SIDE DUNGEONS — Extra challenge, extra reward!")
    divider()
    avail=[d for d in SIDE_DUNGEONS if SIDE_DUNGEONS.index(d)*6<=floor]
    if not avail: slow_print("  No side dungeons unlocked yet."); pause(1); return
    for i,d in enumerate(avail,1):
        print(f"  [{i}] {d['name']:<18} {d['floors']} floors  {d['gold']}g + {d['xp']} XP  — {d['desc']}")
    print("  [0] Leave")
    divider()
    c=input("  Choose: ").strip()
    if c=="0": return
    try:
        dng=avail[int(c)-1]
    except: return

    slow_print(f"\n  Entering {dng['name']}...")
    pause(1)
    hp_before=hero.hp
    for f in range(1,dng["floors"]+1):
        slow_print(f"\n  {dng['name']} — Room {f}/{dng['floors']}")
        enemy=get_enemy(floor)
        enemy.hp=int(enemy.hp*dng["enemy_mult"])
        enemy.atk=int(enemy.atk*dng["enemy_mult"])
        result=battle(hero,enemy,qb)
        if result=="lose":
            slow_print("  💀 Defeated in the side dungeon. Returning..."); pause(1.5); return

    # Completed!
    divider()
    slow_print(f"  🏆 {dng['name']} CLEARED!")
    gold_bonus=dng["gold"]+random.randint(-10,20)
    hero.gold+=gold_bonus; hero.gain_xp(dng["xp"])
    hero.elixirs+=1; hero.side_dungeons+=1
    slow_print(f"  💰 +{gold_bonus} gold, +{dng['xp']} XP, +1 Elixir!")
    if random.random()<0.30:
        hero.antidotes+=2; slow_print("  💉 Bonus: +2 Antidotes!")
    divider(); pause(1.5)


# ═══════════════════════════════════════════════════════════════════
#  LORE LIBRARY
# ═══════════════════════════════════════════════════════════════════
LORE = [
    ("The Dragon Lord",     "It is said the Dragon Lord was once a mortal king who made a pact with chaos. His fire cannot be extinguished by water alone — only iron will and courage can douse those flames.", "regen",3),
    ("The Shadow Realm",    "Creatures from the Shadow Realm feed on fear. Show no hesitation and they weaken. The Shadow Blade was forged from their own darkness — turned against them.", "empowered",3),
    ("The Ancient Golems",  "Golems were built by the Titan mages of old. Their stone cores vibrate at a frequency that amplifies thunder magic. Strike them with lightning to exploit this.", "atk_bonus",3),
    ("Vampiric Curse",      "Vampires grow stronger each century. The Vampire Lord commands legions. His curse is weakened by holy energy — and his blood, if consumed, grants short-term power.", "vampiric",4),
    ("The Void",            "Beyond the 30th floor, reality frays. The Void whispers promises to those who listen. Ignore them. Those who accept power from the Void become its slaves.", "barrier",50),
    ("Legend of the Forge", "The Celestial Blade was forged from the bones of a fallen god. The smith who made it went blind afterwards — yet claimed it was worth it.", "xp_bonus",0),
    ("Dragon Slayers",      "Only three heroes have ever reached the Dragon Lord and returned. All three carried companions with them. No solo hero has ever succeeded.", "gold_bonus",0),
    ("The Necromancer's Path","Necromancers do not fear death — they have already walked its halls. The Lich Form allows one to briefly touch immortality, but the mind suffers for it.", "mp_bonus",20),
]

def visit_library(hero):
    clear(); divider()
    slow_print("  📚 THE ANCIENT LIBRARY — Knowledge is power!")
    divider()
    for i,(title,text,effect,val) in enumerate(LORE,1):
        read="✅" if i-1 in hero.lore_entries_read else "📖"
        print(f"  [{i}] {read} {title}")
    print("  [0] Leave")
    divider()
    c=input("  Read entry (1-8): ").strip()
    if c=="0": return
    try:
        idx=int(c)-1
        if 0<=idx<len(LORE):
            title,text,effect,val=LORE[idx]
            clear(); divider()
            slow_print(f"  📖 {title}")
            divider()
            slow_print(f"  {text}")
            divider()
            if idx not in hero.lore_entries_read:
                hero.lore_entries_read.add(idx)
                if effect=="regen": hero.add_status("regen",val); slow_print(f"  ✨ Inspiration! Regen {val} turns!")
                elif effect=="empowered": hero.add_status("empowered",val); slow_print(f"  💪 Empowered {val} turns!")
                elif effect=="vampiric": hero.add_status("vampiric",val); slow_print(f"  🧛 Vampiric {val} turns!")
                elif effect=="barrier": hero.statuses["barrier"]=val; slow_print(f"  🔷 Barrier activated!")
                elif effect=="mp_bonus":
                    hero.max_mp+=val; hero.mp=min(hero.max_mp,hero.mp+val)
                    slow_print(f"  💎 +{val} max MP!")
            else:
                slow_print("  (Already read — no bonus)")
            input("\n  Press Enter...")
    except: pass


# ═══════════════════════════════════════════════════════════════════
#  TALENT TREE
# ═══════════════════════════════════════════════════════════════════
def visit_talent_tree(hero):
    while True:
        clear(); divider()
        slow_print("  🧠 TALENT TREE")
        divider()
        print(f"  Talent Points available: {hero.talent_points}")
        print()
        for i,(name,info) in enumerate(TALENT_TREE.items(),1):
            owned=" ✅" if name in hero.talents else ""
            print(f"  [{i:>2}] {name:<20} {info['cost']} pt  — {info['desc']}{owned}")
        print("  [0] Leave")
        divider()
        c=input("  Buy talent (1-{}) or 0: ".format(len(TALENT_TREE))).strip()
        if c=="0": break
        try:
            idx=int(c)-1
            name,info=list(TALENT_TREE.items())[idx]
            if name in hero.talents:
                slow_print("  ⚠️  Already owned."); pause(0.8); continue
            if hero.talent_points<info["cost"]:
                slow_print("  ❌ Not enough talent points."); pause(0.8); continue
            hero.talent_points-=info["cost"]
            hero.talents[name]=1
            eff=info["effect"]
            if eff=="max_hp":     hero.max_hp+=info["amount"]; hero.hp=hero.max_hp
            elif eff=="max_mp":   hero.max_mp+=info["amount"]; hero.mp=hero.max_mp
            elif eff=="base_def": hero.base_def+=info["amount"]
            elif eff=="base_atk": hero.base_atk+=info["amount"]
            elif eff=="tough":    hero.max_hp+=info["amount"]; hero.base_def+=5; hero.hp=hero.max_hp
            slow_print(f"  ✅ Talent '{name}' purchased!"); pause(1)
        except (IndexError,ValueError): slow_print("  ❓ Invalid."); pause(0.5)


# ═══════════════════════════════════════════════════════════════════
#  COMPANION SYSTEM
# ═══════════════════════════════════════════════════════════════════
def visit_tavern(hero):
    clear(); divider()
    slow_print("  🍺 THE TAVERN — Hire a companion!")
    divider()
    if hero.companion:
        slow_print(f"  Current: {hero.companion['emoji']} {hero.companion['name']}")
        print("  [D] Dismiss companion   [0] Leave")
        divider()
        c=input("  > ").strip().lower()
        if c=="d":
            slow_print(f"  👋 {hero.companion['name']} departs."); hero.companion=None
        return

    for i,c in enumerate(COMPANIONS,1):
        print(f"  [{i}] {c['emoji']} {c['name']:<20} Hire:{c['hire_cost']}g  Upkeep:{c['upkeep']}g/floor")
        print(f"       {c['ability']}")
    print("  [0] Leave"); divider()
    print(f"  💰 Gold: {hero.gold}"); divider()
    ch=input("  Hire companion: ").strip()
    try:
        comp=COMPANIONS[int(ch)-1]
        if hero.gold>=comp["hire_cost"]:
            hero.gold-=comp["hire_cost"]; hero.companion=comp
            slow_print(f"  ✅ {comp['name']} joins your party!")
        else: slow_print("  ❌ Not enough gold.")
    except: pass
    pause(1)

def companion_action(hero, enemy):
    if not hero.companion: return
    c=hero.companion
    t=c["type"]
    p=c["power"]
    if t=="heal":
        h=random.randint(p-8,p+8); hero.hp=min(hero.max_hp,hero.hp+h)
        slow_print(f"  {c['emoji']} {c['name']} heals you for {h} HP!")
    elif t=="atk":
        d=max(1,int(hero.atk*p/100)+random.randint(-5,8)); enemy.hp-=d
        slow_print(f"  {c['emoji']} {c['name']} strikes for {d} dmg!")
    elif t=="spell":
        d=random.randint(p-12,p+12); enemy.hp-=d
        slow_print(f"  {c['emoji']} {c['name']} casts for {d} dmg!")
    elif t=="poison":
        if random.random()<0.50: enemy.add_status("poison",3)
        slow_print(f"  {c['emoji']} {c['name']} attempts to poison!")
    elif t=="tank":
        # absorb handled via check in battle
        slow_print(f"  {c['emoji']} {c['name']} holds the line! (-{p}% dmg this turn)")
    elif t=="buff":
        hero.base_atk+=1; hero.mp=min(hero.max_mp,hero.mp+5)
        slow_print(f"  {c['emoji']} {c['name']} inspires you! +1 ATK, +5 MP!")
    hero.companion_battles_total+=1


# ═══════════════════════════════════════════════════════════════════
#  GAMBLING DEN
# ═══════════════════════════════════════════════════════════════════
def visit_gambling(hero):
    clear(); divider()
    slow_print("  🎲 THE GAMBLING DEN — Bet wisely!")
    divider()
    print("  [1] Coin Flip    (bet gold, 50/50, win 2×)")
    print("  [2] High Roll    (bet gold, roll 4-6 to win 2.5×)")
    print("  [3] Lucky Number (bet gold, pick 1-6, win 5×)")
    print("  [4] Double Down  (bet gold, 40% win 3×)")
    print("  [0] Leave")
    divider(); print(f"  💰 Gold: {hero.gold}"); divider()

    choice=input("  Game: ").strip()
    if choice=="0": return
    if choice not in ["1","2","3","4"]: return

    bet_str=input("  Bet amount: ").strip()
    try: bet=min(int(bet_str),hero.gold)
    except: slow_print("  Invalid bet."); pause(1); return
    if bet<=0: return

    hero.gold-=bet
    won=False; winnings=0

    if choice=="1":
        flip=random.choice(["H","T"]); guess=input("  H or T? ").strip().upper()
        slow_print(f"  Flip: {flip}!")
        if guess==flip: won=True; winnings=bet*2
    elif choice=="2":
        roll=random.randint(1,6); slow_print(f"  Roll: {roll}!")
        if roll>=4: won=True; winnings=int(bet*2.5)
    elif choice=="3":
        try: num=int(input("  Pick 1-6: ").strip())
        except: num=1
        roll=random.randint(1,6); slow_print(f"  Roll: {roll}!")
        if roll==num: won=True; winnings=bet*5
    elif choice=="4":
        slow_print("  Doubling down...")
        if random.random()<0.40: won=True; winnings=bet*3

    if won:
        hero.gold+=winnings; hero.total_gold_earned+=winnings-bet
        slow_print(f"  🎉 YOU WIN! +{winnings} gold!")
        hero.gambles_won+=1
    else:
        slow_print(f"  💸 You lose {bet} gold. Better luck next time!")
    pause(1.2)


# ═══════════════════════════════════════════════════════════════════
#  BANK
# ═══════════════════════════════════════════════════════════════════
def visit_bank(hero):
    clear(); divider()
    slow_print("  🏦 THE ROYAL BANK")
    divider()
    print(f"  Wallet: {hero.gold}g   Savings: {hero.bank}g")
    print()
    print("  [1] Deposit gold")
    print("  [2] Withdraw gold")
    print("  [3] Collect interest (5% of savings)")
    print("  [0] Leave")
    divider()
    c=input("  > ").strip()
    if c=="1":
        try:
            amt=min(int(input("  Deposit: ").strip()),hero.gold)
            if amt>0: hero.gold-=amt; hero.bank+=amt; slow_print(f"  ✅ Deposited {amt}g!")
        except: pass
    elif c=="2":
        try:
            amt=min(int(input("  Withdraw: ").strip()),hero.bank)
            if amt>0: hero.bank-=amt; hero.gold+=amt; slow_print(f"  ✅ Withdrew {amt}g!")
        except: pass
    elif c=="3":
        interest=int(hero.bank*0.05)
        if interest>0:
            hero.gold+=interest; slow_print(f"  💰 Interest: +{interest}g!")
        else: slow_print("  No interest yet (need more savings).")
    pause(1)


# ═══════════════════════════════════════════════════════════════════
#  QUESTS
# ═══════════════════════════════════════════════════════════════════
QUEST_POOL=[
    {"name":"First Blood",     "desc":"Win a battle",           "type":"kills",  "goal":1,  "gold":12,"xp":20},
    {"name":"Monster Slayer",  "desc":"Defeat 5 enemies",       "type":"kills",  "goal":5,  "gold":30,"xp":45},
    {"name":"Warlord",         "desc":"Defeat 15 enemies",      "type":"kills",  "goal":15, "gold":65,"xp":90},
    {"name":"Centurion Quest", "desc":"Defeat 50 enemies",      "type":"kills",  "goal":50, "gold":150,"xp":200},
    {"name":"Reach Floor 5",   "desc":"Clear floor 5",          "type":"floors", "goal":5,  "gold":35,"xp":50},
    {"name":"Reach Floor 15",  "desc":"Clear floor 15",         "type":"floors", "goal":15, "gold":80,"xp":110},
    {"name":"Halfway!",        "desc":"Reach floor 20",         "type":"floors", "goal":20, "gold":100,"xp":140},
    {"name":"Going Deep",      "desc":"Reach floor 30",         "type":"floors", "goal":30, "gold":140,"xp":190},
    {"name":"Spellcaster",     "desc":"Use skills 20 times",    "type":"skills", "goal":20, "gold":45,"xp":60},
    {"name":"Skill Addict",    "desc":"Use skills 60 times",    "type":"skills", "goal":60, "gold":100,"xp":130},
    {"name":"Rich Adventurer", "desc":"Earn 200 gold total",    "type":"gold",   "goal":200,"gold":55,"xp":70},
    {"name":"Gold Hoarder",    "desc":"Earn 500 gold total",    "type":"gold",   "goal":500,"gold":120,"xp":150},
    {"name":"Survivor",        "desc":"Stay above 50 HP",       "type":"survive","goal":50, "gold":25,"xp":35},
    {"name":"Lucky Potion",    "desc":"Use 5 potions",          "type":"potions","goal":5,  "gold":20,"xp":28},
    {"name":"Side Explorer",   "desc":"Complete a side dungeon","type":"side",   "goal":1,  "gold":70,"xp":100},
    {"name":"Arena Warrior",   "desc":"Win the arena",          "type":"arena",  "goal":1,  "gold":55,"xp":80},
]

class QuestBoard:
    def __init__(self):
        self.active=[]
        self.completed_names=set()

    def offer_quests(self,hero):
        clear(); divider(); slow_print("  📋 QUEST BOARD"); divider()
        available=[q for q in QUEST_POOL
                   if q["name"] not in self.completed_names
                   and q["name"] not in [a["name"] for a in self.active]
                   and len(self.active)<3]
        if not available: slow_print("  No new quests."); pause(1); return
        offer=random.sample(available,min(3,len(available)))
        for i,q in enumerate(offer,1):
            print(f"  [{i}] {q['name']:<22} {q['desc']}")
            print(f"       Reward: {q['gold']}g + {q['xp']} XP")
        print(f"\n  Active quests: {len(self.active)}/3")
        print("  [0] Leave"); divider()
        c=input("  Accept (1-3) or 0: ").strip()
        if c in["1","2","3"]:
            try:
                q=offer[int(c)-1]; self.active.append(q)
                slow_print(f"  ✅ Accepted: {q['name']}!")
            except: pass
        pause(0.8)

    def check_quests(self,hero):
        done=[]
        for q in self.active:
            complete=False
            t=q["type"]
            if t=="kills"   and hero.kills>=q["goal"]: complete=True
            if t=="floors"  and hero.floors_cleared>=q["goal"]: complete=True
            if t=="skills"  and hero.skill_uses>=q["goal"]: complete=True
            if t=="gold"    and hero.total_gold_earned>=q["goal"]: complete=True
            if t=="survive" and hero.hp>=q["goal"]: complete=True
            if t=="potions" and hero.potions>=q["goal"]: complete=True  # used count not tracked, approx
            if t=="side"    and hero.side_dungeons>=q["goal"]: complete=True
            if t=="arena"   and hero.arena_wins>=q["goal"]: complete=True
            if complete: done.append(q)
        for q in done:
            self.active.remove(q); self.completed_names.add(q["name"])
            hero.gold+=q["gold"]; hero.gain_xp(q["xp"]); hero.quests_done+=1
            slow_print(f"  🏆 QUEST: {q['name']} complete! +{q['gold']}g +{q['xp']} XP!")
            divider(); pause(0.8)


# ═══════════════════════════════════════════════════════════════════
#  ARENA
# ═══════════════════════════════════════════════════════════════════
def visit_arena(hero,floor,qb):
    clear(); divider(); slow_print("  ⚔️  THE ARENA — 4 waves, no healing!"); divider()
    print("  [1] Enter   [2] Leave"); divider()
    if input("  > ").strip()!="1": return

    for wave in range(1,5):
        clear(); slow_print(f"  ⚔️  ARENA WAVE {wave}/4")
        e=get_enemy(floor) if wave<4 else make_elite(floor)
        e.hp=int(e.hp*0.85)
        result=battle(hero,e,qb,arena=True)
        if result=="lose":
            slow_print("  💀 Eliminated!"); pause(1.5); return
        if wave<4:
            h=random.randint(12,20); hero.hp=min(hero.max_hp,hero.hp+h)
            slow_print(f"  🩹 Brief recovery: +{h} HP"); pause(0.8)

    divider(); slow_print("  🏆 ARENA CHAMPION! All 4 waves!")
    prize=100+floor*6; xp_prize=130+floor*9
    hero.gold+=prize; hero.gain_xp(xp_prize); hero.elixirs+=1; hero.arena_wins+=1
    slow_print(f"  💰 {prize}g + {xp_prize} XP + Elixir!"); pause(2)


# ═══════════════════════════════════════════════════════════════════
#  SHOP
# ═══════════════════════════════════════════════════════════════════
def visit_shop(hero):
    while True:
        clear(); divider(); slow_print("  🏪 BLACKSMITH & ITEM SHOP"); divider()
        print("  ── CONSUMABLES ──")
        print("  [1] Potion        8g   +32-55 HP")
        print("  [2] Elixir       30g   Full HP+MP")
        print("  [3] Antidote      7g   Clear debuffs")
        print("  [4] Power Dust   16g   +4 ATK perm")
        print("  [5] Iron Plate   16g   +4 DEF perm")
        print("  [6] Mana Shard   16g   +15 MP perm")
        print()
        print("  ── WEAPONS ──")
        for i,w in enumerate(WEAPONS[1:],7):
            eq=" ◄" if hero.weapon["name"]==w["name"] else ""
            print(f"  [{i:>2}] {w['name']:<18} {w['price']}g  +{w['atk']} ATK  {w['desc']}{eq}")
        print()
        print("  ── ARMOR ──")
        for i,a in enumerate(ARMORS[1:],18):
            eq=" ◄" if hero.armor["name"]==a["name"] else ""
            print(f"  [{i:>2}] {a['name']:<18} {a['price']}g  +{a['def']} DEF  {a['desc']}{eq}")
        print()
        print("  ── ACCESSORIES ──")
        for i,ac in enumerate(ACCESSORIES[1:],27):
            eq=" ◄" if hero.accessory["name"]==ac["name"] else ""
            print(f"  [{i:>2}] {ac['name']:<18} {ac['price']}g  {ac['desc']}{eq}")
        print("\n  [0] Leave")
        divider(); print(f"  💰 Gold: {hero.gold}"); divider()
        c=input("  Choose: ").strip()
        if c=="0": break
        try:
            idx=int(c)
            if idx==1:
                if hero.gold>=8: hero.gold-=8;hero.potions+=1;slow_print("  🧪 Potion!")
                else: slow_print("  ❌")
            elif idx==2:
                if hero.gold>=30: hero.gold-=30;hero.elixirs+=1;slow_print("  💊 Elixir!")
                else: slow_print("  ❌")
            elif idx==3:
                if hero.gold>=7: hero.gold-=7;hero.antidotes+=1;slow_print("  💉 Antidote!")
                else: slow_print("  ❌")
            elif idx==4:
                if hero.gold>=16: hero.gold-=16;hero.base_atk+=4;slow_print("  ⚔️  +4 ATK!")
                else: slow_print("  ❌")
            elif idx==5:
                if hero.gold>=16: hero.gold-=16;hero.base_def+=4;slow_print("  🛡️  +4 DEF!")
                else: slow_print("  ❌")
            elif idx==6:
                if hero.gold>=16: hero.gold-=16;hero.max_mp+=15;hero.mp=min(hero.max_mp,hero.mp+15);slow_print("  💎 +15 MP!")
                else: slow_print("  ❌")
            elif 7<=idx<=17:
                w=WEAPONS[idx-6]
                if hero.gold>=w["price"]:
                    if hero.weapon["atk"]>=w["atk"]: slow_print("  ⚠️  Already better.")
                    else: hero.gold-=w["price"];hero.weapon=w.copy();slow_print(f"  ⚔️  {w['name']}!")
                else: slow_print("  ❌")
            elif 18<=idx<=26:
                a=ARMORS[idx-17]
                if hero.gold>=a["price"]:
                    if hero.armor["def"]>=a["def"]: slow_print("  ⚠️  Already better.")
                    else: hero.gold-=a["price"];hero.armor=a.copy();slow_print(f"  🥋 {a['name']}!")
                else: slow_print("  ❌")
            elif 27<=idx<=38:
                ac=ACCESSORIES[idx-26]
                if hero.gold>=ac["price"]:
                    hero.gold-=ac["price"];hero.accessory=ac.copy();slow_print(f"  💍 {ac['name']}!")
                else: slow_print("  ❌")
            else: slow_print("  ❓")
        except ValueError: slow_print("  ❓")
        pause(0.8)


# ═══════════════════════════════════════════════════════════════════
#  CRAFTING FORGE
# ═══════════════════════════════════════════════════════════════════
def visit_forge(hero):
    clear(); divider(); slow_print("  🔨 THE FORGE"); divider()
    print("  Known recipes (you need both items equipped/owned):")
    for (i1,i2),(result,kind) in CRAFT_RECIPES.items():
        print(f"  ⚗️  {i1} + {i2} → {result}")
    divider()
    print(f"  Weapon: {hero.weapon['name']}  Armor: {hero.armor['name']}  Acc: {hero.accessory['name']}")
    divider(); print("  [1] Attempt craft   [2] Leave")
    if input("  > ").strip()!="1": return

    held=[hero.weapon["name"],hero.armor["name"],hero.accessory["name"]]
    crafted=False
    for (i1,i2),(result,kind) in CRAFT_RECIPES.items():
        if i1 in held and i2 in held:
            slow_print(f"  ✅ Recipe: {i1} + {i2} → {result}!")
            if kind=="weapon":
                for w in WEAPONS:
                    if w["name"]==result: hero.weapon=w.copy(); break
            elif kind=="armor":
                for a in ARMORS:
                    if a["name"]==result: hero.armor=a.copy(); break
            elif kind=="acc":
                for ac in ACCESSORIES:
                    if ac["name"]==result: hero.accessory=ac.copy(); break
            hero.crafts_made+=1; crafted=True
            slow_print(f"  🔥 Crafted {result}!"); break
    if not crafted: slow_print("  ❌ No matching recipe.")
    pause(1.5)


# ═══════════════════════════════════════════════════════════════════
#  INN
# ═══════════════════════════════════════════════════════════════════
def visit_inn(hero):
    cost=12+hero.level*2
    clear(); divider(); slow_print("  🏨 TRAVELER'S INN"); divider()
    print(f"  [1] Full Rest      {cost}g — HP+MP+clear debuffs")
    print(f"  [2] Quick Nap      {cost//2}g — Restore 45% HP")
    print(f"  [3] Meditation     {cost//2}g — Restore 50% MP")
    print("  [0] Leave"); divider(); print(f"  💰 Gold: {hero.gold}"); divider()
    c=input("  > ").strip()
    if c=="1":
        if hero.gold>=cost:
            hero.gold-=cost; hero.hp=hero.max_hp; hero.mp=hero.max_mp
            hero.statuses.clear(); slow_print("  😴 Fully rested!")
        else: slow_print("  ❌")
    elif c=="2":
        h2=cost//2
        if hero.gold>=h2:
            hero.gold-=h2; h=int(hero.max_hp*0.45)
            hero.hp=min(hero.max_hp,hero.hp+h); slow_print(f"  😪 +{h} HP")
        else: slow_print("  ❌")
    elif c=="3":
        h2=cost//2
        if hero.gold>=h2:
            hero.gold-=h2; m=int(hero.max_mp*0.50)
            hero.mp=min(hero.max_mp,hero.mp+m); slow_print(f"  🧘 +{m} MP")
        else: slow_print("  ❌")
    pause(1.2)


# ═══════════════════════════════════════════════════════════════════
#  FLOOR EVENTS
# ═══════════════════════════════════════════════════════════════════
def floor_event(hero,floor):
    r=random.random()
    if r<0.15:
        # Treasure chest
        divider(); slow_print("  📦 TREASURE CHEST!")
        r2=random.random()
        if r2<0.18: g=random.randint(20,55+floor*2);hero.gold+=g;slow_print(f"  💰 {g}g!")
        elif r2<0.34: hero.potions+=random.randint(1,2);slow_print("  🧪 Potions!")
        elif r2<0.46: hero.elixirs+=1;slow_print("  💊 Elixir!")
        elif r2<0.56: g=random.randint(5,9+floor//3);hero.base_atk+=g;slow_print(f"  ⚔️  +{g} ATK!")
        elif r2<0.65: g=random.randint(4,7+floor//4);hero.base_def+=g;slow_print(f"  🛡️  +{g} DEF!")
        elif r2<0.73: g=random.randint(14,24);hero.max_mp+=g;hero.mp=min(hero.max_mp,hero.mp+g);slow_print(f"  💎 +{g} MP!")
        elif r2<0.80: g=random.randint(16,32);hero.max_hp+=g;hero.hp=min(hero.max_hp,hero.hp+g);slow_print(f"  ❤️  +{g} max HP!")
        elif r2<0.88: xp=random.randint(25,55);hero.gain_xp(xp)
        elif r2<0.95: slow_print("  💎 Full restore!");hero.hp=hero.max_hp;hero.mp=hero.max_mp
        else: slow_print("  💀 MIMIC!");dmg=random.randint(20,40);hero.hp=max(1,hero.hp-dmg);slow_print(f"  -{dmg} HP!")
        divider();pause(1.2)
    elif r<0.25:
        clear();divider();slow_print("  🛒 Wandering Merchant!")
        print("  [1] Potion (7g)  [2] Elixir (24g)  [3] ATK Dust (18g)  [4] Antidote (6g)  [5] Ignore")
        c=input("  > ").strip()
        if c=="1" and hero.gold>=7:  hero.gold-=7;hero.potions+=1;slow_print("  🧪!")
        elif c=="2" and hero.gold>=24: hero.gold-=24;hero.elixirs+=1;slow_print("  💊!")
        elif c=="3" and hero.gold>=18: hero.gold-=18;hero.base_atk+=4;slow_print("  ⚔️  +4 ATK!")
        elif c=="4" and hero.gold>=6:  hero.gold-=6;hero.antidotes+=1;slow_print("  💉!")
        pause(1.2)
    elif r<0.36:
        clear();divider();slow_print("  🏛️  Healing Shrine!")
        h=random.randint(22,45);m=random.randint(12,24)
        hero.hp=min(hero.max_hp,hero.hp+h);hero.mp=min(hero.max_mp,hero.mp+m)
        slow_print(f"  ✨ +{h} HP, +{m} MP!");divider();pause(1.2)
    elif r<0.44:
        clear();divider();slow_print("  ⚗️  Strange Potion...")
        roll=random.random()
        if roll<0.40: hero.add_status("empowered",5);slow_print("  💪 +30% ATK 5t!")
        elif roll<0.60: hero.add_status("regen",6);slow_print("  💚 Regen 6t!")
        elif roll<0.75: hero.add_status("hasted",3);slow_print("  💨 Hasted 3t!")
        elif roll<0.88: hero.add_status("blessed",5);slow_print("  ✨ Blessed 5t!")
        else: hero.add_status("poison",3);slow_print("  ☠️  Poison 3t!")
        divider();pause(1.2)
    elif r<0.50:
        clear();divider();slow_print("  ⚠️  Trap!")
        dmg=random.randint(14,32);hero.hp=max(1,hero.hp-dmg)
        slow_print(f"  💥 -{dmg} HP!");divider();pause(1.2)
    elif r<0.56:
        clear();divider();slow_print("  📖 Ancient Inscription...")
        xp=random.randint(28,60);hero.gain_xp(xp);divider();pause(1.2)
    elif r<0.61:
        clear();divider();slow_print("  💰 Hidden stash!")
        g=random.randint(22,50);hero.gold+=g;hero.total_gold_earned+=g
        slow_print(f"  💰 +{g}g!");divider();pause(1.2)
    elif r<0.65:
        clear();divider();slow_print("  🗝️  Old chest — locked. Forced open!")
        if random.random()<0.5:
            hero.elixirs+=1;slow_print("  💊 Elixir inside!")
        else:
            slow_print("  💀 Trapped! Poison!"); hero.add_status("poison",3)
        divider();pause(1.2)


# ═══════════════════════════════════════════════════════════════════
#  BATTLE ENGINE
# ═══════════════════════════════════════════════════════════════════
def battle(hero, enemy, qb=None, arena=False):
    clear(); divider()
    if enemy.boss:
        slow_print(f"  ⚠️  BOSS: {enemy.emoji} {enemy.name}!")
        slow_print("  This is a legendary fight — survive or perish!")
    elif enemy.elite:
        slow_print(f"  ⭐ ELITE: {enemy.emoji} {enemy.name}!")
    else:
        slow_print(f"  ⚔️  {enemy.emoji} {enemy.name} appears!")
    divider(); pause(0.9)

    hero.iron_will_used=False
    turn=0

    while hero.is_alive() and enemy.is_alive():
        turn+=1
        hero.apply_status_tick(); enemy.apply_status_tick()
        if not hero.is_alive(): break

        # Companion upkeep per floor handled in main; companion acts here
        if hero.companion: companion_action(hero,enemy)

        # Accessory mp regen
        if hero.accessory["bonus"].get("mp_regen"):
            hero.mp=min(hero.max_mp,hero.mp+hero.accessory["bonus"]["mp_regen"])

        if qb: qb.check_quests(hero)

        clear()
        print(f"\n  ─── Turn {turn} ───")
        enemy.hp_bar_str(); print()
        hero.show_stats(); divider()
        print("  [1] Attack         [2] Use Skill")
        print("  [3] Potion         [4] Elixir")
        print("  [5] Antidote       [6] Defend (-40% dmg)")
        print("  [7] Inspect enemy")
        if not arena and not enemy.boss:
            print("  [8] Run Away")
        divider()

        action=input("  Action: ").strip()
        defending=False

        if action=="1":
            if "death_mark" in hero.statuses:
                base=hero.normal_attack(enemy)
                bonus=base*2; enemy.hp-=bonus
                slow_print(f"  💀 DEATH MARK! +{bonus} bonus dmg!")
                del hero.statuses["death_mark"]
            else:
                hero.normal_attack(enemy)

        elif action=="2":
            if not hero.skills: slow_print("  ❌ No skills!"); continue
            print()
            for i,s in enumerate(hero.skills,1):
                print(f"  [{i}] {s['name']:<18} {s['mp']} MP  {s['desc']}")
            print("  [0] Cancel")
            sc=input("  Skill: ").strip()
            if sc=="0": continue
            try:
                sk=hero.skills[int(sc)-1]
                result=hero.use_skill(sk,enemy)
                if result=="escape":
                    slow_print("  💨 Escaped!"); pause(1); return "escaped"
                if not result: continue
            except: slow_print("  ❓"); continue

        elif action=="3": hero.use_potion()
        elif action=="4": hero.use_elixir()
        elif action=="5": hero.use_antidote()
        elif action=="6":
            defending=True; slow_print("  🛡️  Defending...")
        elif action=="7":
            clear(); divider()
            print(f"  🔍 {enemy.name}")
            print(f"  HP:{enemy.hp}/{enemy.max_hp}  ATK:{enemy.atk}  DEF:{enemy.defense}")
            print(f"  Boss:{enemy.boss}  Elite:{enemy.elite}  Weakness:{enemy.weakness}")
            if enemy.statuses: print(f"  Status: {', '.join(enemy.statuses)}")
            if enemy.skills: print(f"  Skills: {', '.join(s['name'] for s in enemy.skills)}")
            divider(); input("  Press Enter..."); continue
        elif action=="8" and not arena and not enemy.boss:
            if random.random()<0.38: slow_print("  🏃 Escaped!"); pause(1); return "escaped"
            else: slow_print("  ❌ Couldn't escape!")
        else:
            slow_print("  ❓ Invalid.")

        # Enemy attacks
        if enemy.is_alive():
            dmg=enemy.attack(hero)
            if defending and dmg>0:
                red=int(dmg*0.40); hero.hp=min(hero.max_hp,hero.hp+red)
                slow_print(f"  🛡️  Defense reduced dmg by {red}!")
            # Companion tank absorb
            if hero.companion and hero.companion["type"]=="tank" and dmg>0:
                absorb=int(dmg*hero.companion["power"]/100)
                hero.hp=min(hero.max_hp,hero.hp+absorb)
                slow_print(f"  🗿 {hero.companion['name']} absorbs {absorb} dmg!")

        # Death checks
        if not hero.is_alive():
            if "resurrection_ready" in hero.statuses:
                del hero.statuses["resurrection_ready"]
                hero.hp=hero.max_hp//2
                slow_print("  🌟 RESURRECTION! You rise!"); pause(1)
            elif hero.accessory["bonus"].get("revive") and not hero.revive_used:
                hero.revive_used=True; hero.hp=hero.max_hp//2
                slow_print("  🪶 Phoenix Feather! Revived!"); pause(1)

        pause(0.42)

    if hero.is_alive():
        divider(); slow_print(f"  🏆 Victory! {enemy.name} defeated!")
        hero.kills+=1
        if enemy.boss: hero.boss_kills+=1
        loot=enemy.gold+random.randint(-5,12)
        bonus_pct=hero.talents.get("Gold Sense",0)*25/100
        loot=int(loot*(1+bonus_pct))
        hero.gold+=loot; hero.total_gold_earned+=loot
        hero.gain_xp(enemy.xp)
        slow_print(f"  💰 Looted {loot}g!")
        if random.random()<0.12: hero.potions+=1;slow_print("  🎁 Drop: Potion!")
        if (enemy.boss or enemy.elite) and random.random()<0.30: hero.elixirs+=1;slow_print("  🎁 Drop: Elixir!")
        if enemy.boss and random.random()<0.20: hero.antidotes+=2;slow_print("  🎁 Drop: Antidotes!")
        hero.check_achievements()
        pause(1.5); return "win"
    else:
        divider(); slow_print(f"  💀 {hero.name} has fallen..."); pause(2); return "lose"


# ═══════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════
def main():
    clear(); divider("═")
    slow_print("  🐉  DRAGON QUEST — MAXIMUM EDITION  🐉")
    slow_print("  40 Floors · 8 Bosses · 6 Classes · 10 Skills Each")
    slow_print("  Companions · Talents · Arena · Side Dungeons · Lore")
    slow_print("  Bank · Gambling · Crafting · Achievements · Quests")
    divider("═"); pause(0.5)

    name=input("\n  Hero name: ").strip() or "Hero"
    divider()
    print("\n  Choose your class:\n")
    print("  [1] Warrior     — Tanky, berserk combos, World Breaker")
    print("  [2] Mage        — Fragile, massive spells, Big Bang")
    print("  [3] Rogue       — Poison, assassination, Oblivion Strike")
    print("  [4] Paladin     — Self-heal, holy power, Holy Apocalypse")
    print("  [5] Necromancer — Drain life, Plague, Lich Form, Death Nova")
    print("  [6] Berserker   — Raw power, vampiric, Armageddon Fist")
    divider()
    cls={"1":"Warrior","2":"Mage","3":"Rogue","4":"Paladin","5":"Necromancer","6":"Berserker"}.get(
        input("  Choice (1-6): ").strip(),"Warrior")

    hero   = Hero(name,cls)
    bosses = make_bosses()
    qb     = QuestBoard()

    clear(); divider()
    slow_print(f"  Welcome, {hero.name} the {cls}!")
    slow_print("  Conquer 40 floors. Slay the Dragon Lord!")
    slow_print("  ⚠️  Bosses at floors 5,10,15,20,25,30,36,40")
    slow_print("  ⭐ Elite enemies can appear anywhere!")
    slow_print("  🌟 Earn Talent Points on level-up")
    divider(); pause(2)

    floor=1; total=40
    floor_ref = [floor]  # mutable reference for cheat codes

    # Companion upkeep per floor
    upkeep_floor=0

    while hero.is_alive() and floor_ref[0]<=total:
        floor = floor_ref[0]
        qb.check_quests(hero)
        hero.check_achievements()

        # Companion upkeep
        if hero.companion and floor>upkeep_floor:
            uke=hero.companion["upkeep"]
            if hero.gold>=uke: hero.gold-=uke
            else:
                slow_print(f"  ⚠️  Can't afford {hero.companion['name']}'s upkeep! They leave.")
                hero.companion=None
            upkeep_floor=floor

        # ── BOSS FLOOR ──────────────────────────────────────────
        if floor in bosses:
            clear(); divider("═")
            slow_print(f"  ⚠️  FLOOR {floor} — BOSS BATTLE!")
            divider("═"); pause(0.8)
            boss=bosses[floor]; boss.hp=boss.max_hp; boss.statuses={}
            result=battle(hero,boss,qb)
            if result=="win": hero.floors_cleared+=1; floor_ref[0]+=1
            elif result=="lose": break
            else: slow_print("  ⚠️  Can't flee boss!"); pause(1)
            continue

        # ── NORMAL FLOOR ────────────────────────────────────────
        clear(); divider()
        slow_print(f"  🏰 FLOOR {floor}/{total}  Kills:{hero.kills}  Quests:{hero.quests_done}  Talents:{hero.talent_points}pt")
        divider()
        print("  [1]  Explore        (fight + random event)")
        print("  [2]  Elite Battle   (⭐ harder, better loot)")
        print("  [3]  View Stats")
        print("  [4]  Shop")
        print("  [5]  Inn")
        print("  [6]  Arena          (4 waves)")
        print("  [7]  Quest Board")
        print("  [8]  Forge          (crafting)")
        print("  [9]  Side Dungeon   (bonus area)")
        print("  [10] Talent Tree")
        print("  [11] Tavern         (companions)")
        print("  [12] Library        (lore + buffs)")
        print("  [13] Bank")
        print("  [14] Gambling Den")
        print("  [15] Achievements")
        print("  [16] 🔑 Cheat Codes")
        print("  [0]  Quit")
        divider()

        c=input("  > ").strip()

        if c=="1":
            floor_event(hero,floor)
            if not hero.is_alive(): break
            enemy=get_enemy(floor)
            result=battle(hero,enemy,qb)
            if result=="win": hero.floors_cleared+=1; floor_ref[0]+=1
            elif result=="lose": break

        elif c=="2":
            slow_print("  ⭐ Searching for elite...")
            pause(0.5)
            elite=make_elite(floor)
            result=battle(hero,elite,qb)
            if result=="win": hero.floors_cleared+=1; floor_ref[0]+=1
            elif result=="lose": break

        elif c=="3":
            clear(); divider(); hero.show_stats(); divider()
            input("  Press Enter...")

        elif c=="4":  visit_shop(hero)
        elif c=="5":  visit_inn(hero)
        elif c=="6":  visit_arena(hero,floor,qb)
        elif c=="7":  qb.offer_quests(hero); qb.check_quests(hero)
        elif c=="8":  visit_forge(hero)
        elif c=="9":  run_side_dungeon(hero,qb,floor)
        elif c=="10": visit_talent_tree(hero)
        elif c=="11": visit_tavern(hero)
        elif c=="12": visit_library(hero)
        elif c=="13": visit_bank(hero)
        elif c=="14": visit_gambling(hero)
        elif c=="15":
            clear(); divider(); slow_print("  🏆 ACHIEVEMENTS"); divider()
            for name2,info in hero.achievements.items():
                status="✅" if info["done"] else "⬜"
                print(f"  {status} {name2:<22} {info['desc']}")
            divider(); input("  Press Enter...")
        elif c=="16":
            cheat_menu(hero, floor_ref)
        elif c=="0":
            slow_print("  👋 Farewell, hero!"); return
        else:
            slow_print("  ❓ Invalid.")

    floor = floor_ref[0]

    # ── END SCREEN ─────────────────────────────────────────────────
    clear(); divider("═")
    if floor>total:
        slow_print("  🎉🎉  ULTIMATE VICTORY! THE DRAGON LORD IS SLAIN!  🎉🎉")
        slow_print(f"  {hero.name} — Legend of legends. Champion eternal. 👑")
    else:
        slow_print("  💀 GAME OVER")
        slow_print(f"  {hero.name} fell on Floor {floor}.")
    divider("═")
    title=hero.get_title()
    ach_done=sum(1 for a in hero.achievements.values() if a["done"])
    print(f"\n  🏅 Title          : {title}")
    print(f"  Class            : {hero.cls}")
    print(f"  Final Level      : {hero.level}")
    print(f"  Floors Cleared   : {hero.floors_cleared}/{total}")
    print(f"  Enemies Slain    : {hero.kills}  (Bosses: {hero.boss_kills})")
    print(f"  Total Damage     : {hero.total_dmg}")
    print(f"  Quests Completed : {hero.quests_done}")
    print(f"  Arena Wins       : {hero.arena_wins}")
    print(f"  Side Dungeons    : {hero.side_dungeons}")
    print(f"  Crafts Made      : {hero.crafts_made}")
    print(f"  Gold Collected   : {hero.total_gold_earned}")
    print(f"  Achievements     : {ach_done}/{len(hero.achievements)}")
    print(f"  Talents Learned  : {', '.join(hero.talents) or 'None'}")
    print(f"  Weapon           : {hero.weapon['name']}")
    print(f"  Armor            : {hero.armor['name']}")
    print(f"  Accessory        : {hero.accessory['name']}")
    divider("═")
    slow_print("  Thanks for playing Dragon Quest Maximum Edition! 🐲\n")

    if input("  Play again? (y/n): ").strip().lower()=="y":
        main()

# ═══════════════════════════════════════════════════════════════════
#  CHEAT CODES
# ═══════════════════════════════════════════════════════════════════
CHEAT_CODES = {
    "GOLDRAIN":    "Give 999 gold",
    "GODMODE":     "Max HP, MP, ATK, DEF permanently",
    "LEVELUP":     "Instantly gain 5 levels",
    "FULLSTOCK":   "Get 10 potions, 5 elixirs, 5 antidotes",
    "SKIPFLOOR":   "Skip ahead 5 floors instantly",
    "BESTGEAR":    "Equip best weapon, armor and accessory",
    "ALLSKILLS":   "Unlock all skills for your class",
    "ALLTALENTS":  "Unlock every talent for free",
    "KILLALL":     "Add 50 kills to your count",
    "INEEDMP":     "Fully restore MP",
    "BLESSED":     "Apply all positive statuses for 10 turns",
    "DRAGONSLAIN": "Instantly win the game (skip to floor 41)",
    "RICHKID":     "Deposit 9999g into the bank",
    "COMPANION":   "Get the best companion for free",
    "NODEBUFFS":   "Clear all negative statuses",
    "WHOAMI":      "Reveal secret hero info",
}

USED_CODES = set()

def cheat_menu(hero, floor_ref):
    clear(); divider("═")
    slow_print("  🔑  CHEAT CODES")
    slow_print("  Enter a code if you know one...")
    divider("═")
    print()
    code = input("  Code (or BACK): ").strip().upper()

    if code == "BACK":
        return floor_ref[0]

    if code not in CHEAT_CODES:
        slow_print("  ❌ Unknown cheat code."); pause(1)
        return floor_ref[0]

    if code in USED_CODES:
        slow_print("  ⚠️  Already used that code!"); pause(1)
        return floor_ref[0]

    USED_CODES.add(code)
    divider()

    if code == "GOLDRAIN":
        hero.gold += 999
        hero.total_gold_earned += 999
        slow_print("  💰💰 GOLDRAIN! +999 gold! It's raining gold!")

    elif code == "GODMODE":
        hero.max_hp  += 500; hero.hp = hero.max_hp
        hero.max_mp  += 300; hero.mp = hero.max_mp
        hero.base_atk += 50
        hero.base_def += 40
        slow_print("  👑 GODMODE! +500 HP, +300 MP, +50 ATK, +40 DEF!")

    elif code == "LEVELUP":
        slow_print("  🎉 Levelling up 5 times...")
        for _ in range(5):
            hero.xp = hero.xp_next
            hero.level_up()

    elif code == "FULLSTOCK":
        hero.potions   += 10
        hero.elixirs   += 5
        hero.antidotes += 5
        slow_print("  🧪 FULLSTOCK! +10 Potions, +5 Elixirs, +5 Antidotes!")

    elif code == "SKIPFLOOR":
        skip = min(5, 40 - floor_ref[0])
        floor_ref[0] += skip
        hero.floors_cleared += skip
        slow_print(f"  🏰 SKIPFLOOR! Jumped to floor {floor_ref[0]}!")

    elif code == "BESTGEAR":
        hero.weapon    = WEAPONS[-1].copy()
        hero.armor     = ARMORS[-1].copy()
        hero.accessory = ACCESSORIES[-1].copy()
        slow_print(f"  ⚔️  BESTGEAR! Equipped {WEAPONS[-1]['name']}, {ARMORS[-1]['name']}, {ACCESSORIES[-1]['name']}!")

    elif code == "ALLSKILLS":
        hero.skills = [s.copy() for s in ALL_SKILLS[hero.cls]]
        slow_print(f"  🌟 ALLSKILLS! All {len(hero.skills)} skills unlocked!")

    elif code == "ALLTALENTS":
        for tname, tinfo in TALENT_TREE.items():
            if tname not in hero.talents:
                hero.talents[tname] = 1
                eff = tinfo["effect"]
                if eff == "max_hp":     hero.max_hp += tinfo["amount"]; hero.hp = hero.max_hp
                elif eff == "max_mp":   hero.max_mp += tinfo["amount"]; hero.mp = hero.max_mp
                elif eff == "base_def": hero.base_def += tinfo["amount"]
                elif eff == "base_atk": hero.base_atk += tinfo["amount"]
                elif eff == "tough":    hero.max_hp += tinfo["amount"]; hero.base_def += 5; hero.hp = hero.max_hp
        slow_print("  🧠 ALLTALENTS! Every talent unlocked for free!")

    elif code == "KILLALL":
        hero.kills += 50
        slow_print("  💀 KILLALL! +50 kills added to your count!")

    elif code == "INEEDMP":
        hero.mp = hero.max_mp
        slow_print("  💎 INEEDMP! MP fully restored!")

    elif code == "BLESSED":
        for st in ("regen", "empowered", "blessed", "hasted", "vampiric"):
            hero.statuses[st] = 10
        hero.statuses["shielded"] = 3
        slow_print("  ✨ BLESSED! All positive statuses applied for 10 turns!")

    elif code == "DRAGONSLAIN":
        slow_print("  🐲 DRAGONSLAIN! The Dragon Lord mysteriously explodes...")
        slow_print("  You win... but did you really earn it? 😏")
        floor_ref[0] = 41
        return floor_ref[0]

    elif code == "RICHKID":
        hero.bank += 9999
        slow_print("  🏦 RICHKID! 9999 gold deposited into your bank!")

    elif code == "COMPANION":
        best = COMPANIONS[-1]  # Golem Guardian or last in list
        hero.companion = best
        slow_print(f"  🤝 COMPANION! {best['emoji']} {best['name']} joins for free!")

    elif code == "NODEBUFFS":
        bad = ("poison","burn","bleed","acid","stun","frozen","cursed",
               "blind","weakened","marked","petrified","doom")
        cleared = [s for s in list(hero.statuses) if s in bad]
        for s in cleared: del hero.statuses[s]
        slow_print(f"  💉 NODEBUFFS! Cleared: {', '.join(cleared) if cleared else 'nothing active'}.")

    elif code == "WHOAMI":
        slow_print(f"  🔍 Name    : {hero.name}")
        slow_print(f"  🔍 Class   : {hero.cls}")
        slow_print(f"  🔍 Level   : {hero.level}")
        slow_print(f"  🔍 Kills   : {hero.kills}")
        slow_print(f"  🔍 Title   : {hero.get_title()}")
        slow_print(f"  🔍 Secret  : You are destined to face the Dragon Lord. Or not. Your choice.")

    divider()
    slow_print("  ✅ Cheat applied!")
    pause(1.5)
    return floor_ref[0]


if __name__=="__main__":
    main()