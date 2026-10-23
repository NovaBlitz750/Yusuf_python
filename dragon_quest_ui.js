import { useState, useEffect, useRef, useCallback } from "react";

const rnd = (lo, hi) => Math.floor(Math.random() * (hi - lo + 1)) + lo;
const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));

// ── DATA ────────────────────────────────────────────────────────────
const WEAPONS = [
  { name: "Rusty Sword", atk: 0, price: 0, tier: 0, desc: "Starting blade" },
  { name: "Iron Sword", atk: 6, price: 18, tier: 1, desc: "Reliable" },
  { name: "Steel Sword", atk: 11, price: 35, tier: 1, desc: "Sharp steel" },
  { name: "Shadow Blade", atk: 17, price: 60, tier: 2, desc: "Ignores 5 DEF" },
  { name: "Flame Sword", atk: 23, price: 90, tier: 2, desc: "Burns 20%" },
  { name: "Thunder Blade", atk: 28, price: 125, tier: 3, desc: "Stuns 18%" },
  { name: "Frost Edge", atk: 32, price: 155, tier: 3, desc: "Freezes 22%" },
  { name: "Void Saber", atk: 40, price: 200, tier: 4, desc: "Bleeds 28%" },
  { name: "Soul Reaper", atk: 48, price: 265, tier: 4, desc: "Steals 15% dmg as HP" },
  { name: "Dragon Fang", atk: 58, price: 340, tier: 5, desc: "Burns+bleeds 30%" },
  { name: "Celestial Blade", atk: 72, price: 450, tier: 5, desc: "+25% spell dmg" },
  { name: "Godslayer", atk: 90, price: 600, tier: 6, desc: "Mythic" },
];
const ARMORS = [
  { name: "Cloth Robe", def: 0, price: 0, tier: 0, desc: "Starting" },
  { name: "Leather Armor", def: 5, price: 15, tier: 1, desc: "Basic" },
  { name: "Studded Leather", def: 9, price: 30, tier: 1, desc: "Reinforced" },
  { name: "Chain Mail", def: 14, price: 55, tier: 2, desc: "Solid" },
  { name: "Shadow Cloak", def: 18, price: 80, tier: 2, desc: "+14% dodge" },
  { name: "Knight Plate", def: 25, price: 120, tier: 3, desc: "Heavy" },
  { name: "Void Armor", def: 32, price: 170, tier: 4, desc: "Reflects 10% dmg" },
  { name: "Dragon Scale", def: 42, price: 240, tier: 5, desc: "Near-impenetrable" },
  { name: "Celestial Robe", def: 54, price: 330, tier: 5, desc: "+20% max MP" },
  { name: "Aegis Plate", def: 68, price: 480, tier: 6, desc: "Mythic" },
];
const ACCESSORIES = [
  { name: "None", bonus: {}, price: 0, tier: 0, desc: "Nothing" },
  { name: "Lucky Charm", bonus: { crit: 10 }, price: 22, tier: 1, desc: "+10% crit" },
  { name: "Mana Ring", bonus: { mp_regen: 4 }, price: 28, tier: 1, desc: "+4 MP/turn" },
  { name: "Warrior's Band", bonus: { atk: 6 }, price: 35, tier: 1, desc: "+6 ATK" },
  { name: "Guardian Amulet", bonus: { block: 15 }, price: 42, tier: 2, desc: "+15% block" },
  { name: "Sage's Pendant", bonus: { spell_power: 22 }, price: 55, tier: 2, desc: "+22% spell dmg" },
  { name: "Berserker Ring", bonus: { atk: 12, crit: 10 }, price: 80, tier: 3, desc: "+12 ATK +10% crit" },
  { name: "Vampiric Fang", bonus: { lifesteal: 18 }, price: 95, tier: 3, desc: "+18% lifesteal" },
  { name: "Phoenix Feather", bonus: { revive: true }, price: 110, tier: 3, desc: "Auto-revive once" },
  { name: "Dragon Eye", bonus: { all: 14 }, price: 160, tier: 4, desc: "+14 all stats" },
  { name: "Arcane Heart", bonus: { spell_power: 35, mp_regen: 6 }, price: 200, tier: 4, desc: "+35% spell, +6 MP/turn" },
  { name: "Titan Gauntlet", bonus: { atk: 20, block: 20 }, price: 260, tier: 5, desc: "+20 ATK +20% block" },
  { name: "Godstone", bonus: { all: 22, crit: 15, block: 15 }, price: 400, tier: 6, desc: "Mythic" },
];

const ALL_SKILLS = {
  Warrior: [
    { name: "Shield Bash", mp: 8, desc: "Dmg + 40% stun", ul: 1 },
    { name: "Whirlwind", mp: 14, desc: "2-5 quick hits", ul: 3 },
    { name: "Berserk Mode", mp: 20, desc: "+60% ATK 3 turns", ul: 5 },
    { name: "War Cry", mp: 16, desc: "Weaken enemy -25% ATK", ul: 7 },
    { name: "Earthquake", mp: 28, desc: "Massive ground slam", ul: 9 },
    { name: "Titan Smash", mp: 35, desc: "2x ATK ignores DEF", ul: 12 },
    { name: "Unbreakable", mp: 25, desc: "Block 2 turns", ul: 15 },
    { name: "Battle Cry", mp: 22, desc: "Empower self +30% 4t", ul: 18 },
    { name: "Ragnarok", mp: 50, desc: "Triple ATK self-bleed", ul: 22 },
    { name: "World Breaker", mp: 70, desc: "Destroy DEF + 4x hit", ul: 28 },
  ],
  Mage: [
    { name: "Fireball", mp: 10, desc: "Burns 25%", ul: 1 },
    { name: "Blizzard", mp: 14, desc: "Freezes 30%", ul: 3 },
    { name: "Thunder", mp: 18, desc: "Stuns 35%", ul: 5 },
    { name: "Arcane Bolt", mp: 12, desc: "Pure magic ignores DEF", ul: 7 },
    { name: "Meteor Strike", mp: 30, desc: "Devastating impact", ul: 9 },
    { name: "Chain Lightning", mp: 35, desc: "Hits 3 times with stun", ul: 12 },
    { name: "Blizzard Storm", mp: 42, desc: "Freeze + massive dmg", ul: 15 },
    { name: "Mana Surge", mp: 0, desc: "Sacrifice HP for MP", ul: 18 },
    { name: "Armageddon", mp: 65, desc: "Catastrophic spell", ul: 22 },
    { name: "Big Bang", mp: 90, desc: "Ultimate destruction", ul: 28 },
  ],
  Rogue: [
    { name: "Shadowstep", mp: 8, desc: "Bypass all DEF", ul: 1 },
    { name: "Poison Blade", mp: 12, desc: "Poison 5 turns", ul: 3 },
    { name: "Smoke Bomb", mp: 10, desc: "Bleed + escape", ul: 5 },
    { name: "Mark Target", mp: 8, desc: "+30% dmg taken 4t", ul: 7 },
    { name: "Death Mark", mp: 25, desc: "Next attack x3", ul: 9 },
    { name: "Shadow Clone", mp: 30, desc: "Attack twice", ul: 12 },
    { name: "Vanish", mp: 20, desc: "Skip enemy turn", ul: 15 },
    { name: "Acid Splash", mp: 18, desc: "Acid dmg + status", ul: 18 },
    { name: "Assassination", mp: 45, desc: "60% of enemy max HP", ul: 22 },
    { name: "Oblivion Strike", mp: 60, desc: "Flat 999 dmg", ul: 28 },
  ],
  Paladin: [
    { name: "Holy Strike", mp: 10, desc: "Dmg + self-heal", ul: 1 },
    { name: "Divine Shield", mp: 12, desc: "Block next attack", ul: 3 },
    { name: "Smite", mp: 20, desc: "Dmg + curse enemy", ul: 5 },
    { name: "Consecrate", mp: 15, desc: "Regen + blessed 4t", ul: 7 },
    { name: "Resurrection", mp: 40, desc: "Revive on death", ul: 9 },
    { name: "Holy Nova", mp: 35, desc: "Dmg + heal + cleanse", ul: 12 },
    { name: "Sacred Flame", mp: 28, desc: "Burns + blinds enemy", ul: 15 },
    { name: "Aura of Light", mp: 30, desc: "Barrier absorbs 60 dmg", ul: 18 },
    { name: "Divine Judgment", mp: 55, desc: "Massive holy + regen", ul: 22 },
    { name: "Holy Apocalypse", mp: 80, desc: "Ultimate holy", ul: 28 },
  ],
  Necromancer: [
    { name: "Drain Life", mp: 12, desc: "Steal HP from enemy", ul: 1 },
    { name: "Bone Spear", mp: 10, desc: "Piercing bone", ul: 3 },
    { name: "Curse of Decay", mp: 14, desc: "Poison + weaken", ul: 5 },
    { name: "Soul Rend", mp: 20, desc: "Tears soul, heavy dmg", ul: 7 },
    { name: "Raise Dead", mp: 25, desc: "Undead ally attacks", ul: 9 },
    { name: "Death Coil", mp: 18, desc: "Dmg + self-heal 30%", ul: 12 },
    { name: "Plague", mp: 30, desc: "Poison+acid+bleed", ul: 15 },
    { name: "Soul Harvest", mp: 35, desc: "Heal fully", ul: 18 },
    { name: "Lich Form", mp: 50, desc: "Become lich +50% all", ul: 22 },
    { name: "Death Nova", mp: 75, desc: "Massive necrotic AoE", ul: 28 },
  ],
  Berserker: [
    { name: "Cleave", mp: 8, desc: "Heavy hit, ignores DEF", ul: 1 },
    { name: "Battle Rage", mp: 12, desc: "+40% ATK 4 turns", ul: 3 },
    { name: "Bloodlust", mp: 15, desc: "Heal on every hit", ul: 5 },
    { name: "Rampage", mp: 20, desc: "3-6 random hits", ul: 7 },
    { name: "Enrage", mp: 18, desc: "More ATK as HP drops", ul: 9 },
    { name: "Skull Crack", mp: 25, desc: "Dmg + stun + blind", ul: 12 },
    { name: "Endless Fury", mp: 35, desc: "5 empowered hits", ul: 15 },
    { name: "Blood Frenzy", mp: 30, desc: "Berserk + vampiric 3t", ul: 18 },
    { name: "Obliterate", mp: 55, desc: "Crush with full strength", ul: 22 },
    { name: "Armageddon Fist", mp: 80, desc: "Force of gods", ul: 28 },
  ],
};

const COMPANIONS = [
  { name: "Mira the Healer", emoji: "💉", hire_cost: 40, upkeep: 5, ability: "Heals 15-30 HP each turn", type: "heal", power: 22 },
  { name: "Rex the Warrior", emoji: "⚔️", hire_cost: 50, upkeep: 6, ability: "Deals 60% of your ATK each turn", type: "atk", power: 60 },
  { name: "Luna the Mage", emoji: "🔮", hire_cost: 55, upkeep: 7, ability: "Casts random spell for 30-55 dmg", type: "spell", power: 42 },
  { name: "Shade the Rogue", emoji: "🗡️", hire_cost: 45, upkeep: 5, ability: "50% chance to poison each turn", type: "poison", power: 4 },
  { name: "Golem Guardian", emoji: "🗿", hire_cost: 70, upkeep: 8, ability: "Absorbs 20% of damage", type: "tank", power: 20 },
  { name: "Lyra the Bard", emoji: "🎵", hire_cost: 35, upkeep: 4, ability: "+10% ATK and +5 MP each turn", type: "buff", power: 10 },
];

const TALENT_TREE = [
  { name: "Iron Body", desc: "+20 max HP permanently", cost: 1, effect: "max_hp", amount: 20 },
  { name: "Sharp Mind", desc: "+15 max MP permanently", cost: 1, effect: "max_mp", amount: 15 },
  { name: "Battle Hardened", desc: "+4 DEF permanently", cost: 1, effect: "base_def", amount: 4 },
  { name: "Killer Instinct", desc: "+4 ATK permanently", cost: 1, effect: "base_atk", amount: 4 },
  { name: "Lucky Strike", desc: "+8% crit chance globally", cost: 2, effect: "global_crit", amount: 8 },
  { name: "Thick Skin", desc: "Reduce all damage by 8%", cost: 2, effect: "dmg_reduce", amount: 8 },
  { name: "Bloodthirst", desc: "+10% lifesteal on attacks", cost: 2, effect: "lifesteal", amount: 10 },
  { name: "Arcane Mastery", desc: "+15% spell power globally", cost: 2, effect: "global_sp", amount: 15 },
  { name: "Giant Slayer", desc: "+25% dmg to bosses/elites", cost: 3, effect: "boss_dmg", amount: 25 },
  { name: "Iron Will", desc: "Survive lethal hit at 1 HP once/floor", cost: 3, effect: "iron_will", amount: 1 },
  { name: "Mana Fountain", desc: "+8 MP every turn passively", cost: 3, effect: "mp_regen_passive", amount: 8 },
  { name: "Ancient Knowledge", desc: "+20% XP from all sources", cost: 2, effect: "xp_bonus", amount: 20 },
  { name: "Gold Sense", desc: "+25% gold from all sources", cost: 2, effect: "gold_bonus", amount: 25 },
  { name: "Toughness", desc: "+30 max HP + +5 DEF", cost: 3, effect: "tough", amount: 30 },
  { name: "Spell Surge", desc: "10% chance to cast skill twice", cost: 4, effect: "spell_surge", amount: 10 },
];

const ENEMIES_BY_TIER = [
  [
    { name: "Slime", hp: 38, atk: 6, def: 1, xp: 10, gold: 3, emoji: "🟢" },
    { name: "Goblin", hp: 52, atk: 9, def: 2, xp: 16, gold: 5, emoji: "👺" },
    { name: "Skeleton", hp: 62, atk: 13, def: 3, xp: 22, gold: 8, emoji: "💀", weakness: "fire" },
  ],
  [
    { name: "Orc Warrior", hp: 82, atk: 16, def: 6, xp: 30, gold: 11, emoji: "🐗" },
    { name: "Witch", hp: 68, atk: 20, def: 2, xp: 35, gold: 13, emoji: "🧙" },
    { name: "Vampire", hp: 88, atk: 22, def: 5, xp: 42, gold: 16, emoji: "🧛" },
  ],
  [
    { name: "Golem", hp: 115, atk: 18, def: 14, xp: 48, gold: 18, emoji: "🗿", weakness: "thunder" },
    { name: "Dark Knight", hp: 98, atk: 25, def: 8, xp: 55, gold: 20, emoji: "🖤" },
    { name: "Werewolf", hp: 92, atk: 28, def: 7, xp: 52, gold: 19, emoji: "🐺" },
  ],
  [
    { name: "Shadow Mage", hp: 78, atk: 30, def: 3, xp: 60, gold: 22, emoji: "🌑" },
    { name: "Lich", hp: 108, atk: 27, def: 6, xp: 65, gold: 25, emoji: "☠️", weakness: "holy" },
    { name: "Demon", hp: 125, atk: 32, def: 10, xp: 72, gold: 28, emoji: "😈" },
  ],
  [
    { name: "Chimera", hp: 138, atk: 34, def: 12, xp: 80, gold: 31, emoji: "🦁" },
    { name: "Death Knight", hp: 148, atk: 36, def: 14, xp: 88, gold: 34, emoji: "🖤" },
    { name: "Wyvern", hp: 135, atk: 38, def: 9, xp: 82, gold: 32, emoji: "🐉" },
  ],
  [
    { name: "Abyssal Fiend", hp: 165, atk: 40, def: 12, xp: 98, gold: 40, emoji: "👿" },
    { name: "Infernal Drake", hp: 178, atk: 42, def: 15, xp: 104, gold: 43, emoji: "🔥" },
    { name: "Void Wraith", hp: 145, atk: 45, def: 8, xp: 108, gold: 42, emoji: "🌀" },
  ],
  [
    { name: "Ancient Golem", hp: 205, atk: 35, def: 22, xp: 115, gold: 46, emoji: "🗿", weakness: "thunder" },
    { name: "Soul Devourer", hp: 155, atk: 48, def: 10, xp: 120, gold: 48, emoji: "👁️" },
    { name: "Chaos Knight", hp: 180, atk: 46, def: 18, xp: 125, gold: 50, emoji: "⚔️" },
  ],
  [
    { name: "Elder Dragon", hp: 220, atk: 52, def: 16, xp: 135, gold: 55, emoji: "🐲", weakness: "ice" },
    { name: "Void Leviathan", hp: 280, atk: 58, def: 16, xp: 158, gold: 68, emoji: "🦑" },
    { name: "Shadow Titan", hp: 265, atk: 60, def: 22, xp: 162, gold: 70, emoji: "🌑" },
  ],
];

const BOSSES = {
  5: { name: "Iron Colossus", hp: 280, atk: 26, def: 10, xp: 100, gold: 50, emoji: "🤖", skills: [
    { name: "Steel Punch", dmg: 32 }, { name: "Tremor", dmg: 22, status: "stun" }, { name: "Iron Slam", dmg: 40 }
  ]},
  10: { name: "Shadow Drake", hp: 420, atk: 32, def: 14, xp: 145, gold: 70, emoji: "🐍", skills: [
    { name: "Poison Breath", dmg: 25, status: "poison" }, { name: "Tail Whip", dmg: 38 }, { name: "Shadow Bite", dmg: 50 }
  ]},
  15: { name: "Vampire Lord", hp: 560, atk: 40, def: 17, xp: 195, gold: 100, emoji: "🧛", skills: [
    { name: "Blood Drain", dmg: 45 }, { name: "Curse", dmg: 20, status: "cursed" }, { name: "Bat Storm", dmg: 35 }
  ]},
  20: { name: "Abyssal Titan", hp: 740, atk: 50, def: 21, xp: 260, gold: 135, emoji: "👿", skills: [
    { name: "Void Crush", dmg: 62 }, { name: "Dark Nova", dmg: 56, status: "cursed" }, { name: "Abyss Slam", dmg: 75 }
  ]},
  25: { name: "Death God", hp: 920, atk: 58, def: 25, xp: 340, gold: 175, emoji: "💀", skills: [
    { name: "Death Touch", dmg: 70, status: "bleed" }, { name: "Soul Shatter", dmg: 82 }, { name: "Reaper's Blow", dmg: 95 }
  ]},
  30: { name: "Ancient Leviathan", hp: 1100, atk: 65, def: 28, xp: 420, gold: 220, emoji: "🦑", skills: [
    { name: "Tidal Crush", dmg: 78 }, { name: "Void Tentacle", dmg: 90, status: "stun" }, { name: "Maelstrom", dmg: 105 }
  ]},
  36: { name: "Chaos Titan", hp: 1350, atk: 75, def: 32, xp: 510, gold: 275, emoji: "🦾", skills: [
    { name: "Chaos Slam", dmg: 90 }, { name: "World Shatter", dmg: 120 }, { name: "Entropy", dmg: 70, status: "weakened" }
  ]},
  40: { name: "Dragon Lord", hp: 1800, atk: 88, def: 38, xp: 650, gold: 350, emoji: "🐲", skills: [
    { name: "Dragon Breath", dmg: 85, status: "burn" }, { name: "Ancient Fury", dmg: 130 }, { name: "World Flame", dmg: 150 }
  ]},
};

const STATUS_ICONS = {
  poison: "☠️", burn: "🔥", bleed: "🩸", acid: "🟢", stun: "⚡",
  frozen: "❄️", cursed: "💜", blind: "🌫️", weakened: "📉", marked: "🎯",
  berserk: "😡", empowered: "💪", blessed: "✨", regen: "💚",
  shielded: "🛡️", vampiric: "🧛", enraged: "🔴", barrier: "🔷",
};

const DOT_STATUSES = new Set(["poison", "burn", "bleed", "acid"]);
const SKIP_STATUSES = new Set(["stun", "frozen", "petrified"]);
const HEAL_STATUSES = new Set(["regen", "blessed"]);

const BASE_STATS = {
  Warrior: { hp: 145, atk: 18, def: 12, mp: 30, sp: 1.0 },
  Mage: { hp: 80, atk: 10, def: 4, mp: 90, sp: 1.6 },
  Rogue: { hp: 110, atk: 22, def: 7, mp: 42, sp: 1.1 },
  Paladin: { hp: 125, atk: 14, def: 14, mp: 50, sp: 1.3 },
  Necromancer: { hp: 95, atk: 12, def: 6, mp: 80, sp: 1.5 },
  Berserker: { hp: 160, atk: 25, def: 8, mp: 25, sp: 0.9 },
};

// ── INITIAL HERO ────────────────────────────────────────────────────
function makeHero(name, cls) {
  const base = BASE_STATS[cls];
  return {
    name, cls,
    level: 1, xp: 0, xpNext: 45,
    gold: 25, bank: 0,
    potions: 3, elixirs: 0, antidotes: 1,
    maxHp: base.hp, hp: base.hp,
    baseAtk: base.atk, baseDef: base.def,
    mp: base.mp, maxMp: base.mp,
    spPower: base.sp,
    statuses: {},
    kills: 0, bossKills: 0, floorsCleared: 0,
    questsDone: 0, arenaWins: 0, craftsMade: 0,
    skillUses: 0, gamblesWon: 0, totalDmg: 0,
    totalGoldEarned: 0, sideDungeons: 0,
    talentPoints: 0, talents: {},
    reviveUsed: false, ironWillUsed: false,
    weapon: { ...WEAPONS[0] },
    armor: { ...ARMORS[0] },
    accessory: { ...ACCESSORIES[0] },
    companion: null,
    companionBattles: 0,
    skills: ALL_SKILLS[cls].filter(s => s.ul <= 1).map(s => ({ ...s })),
  };
}

function heroAtk(h) {
  let a = h.baseAtk + h.weapon.atk
    + (h.accessory.bonus.atk || 0)
    + (h.accessory.bonus.all || 0)
    + (h.talents["Killer Instinct"] ? 4 : 0);
  if (h.statuses.berserk) a = Math.floor(a * 1.6);
  if (h.statuses.empowered) a = Math.floor(a * 1.3);
  if (h.statuses.weakened) a = Math.floor(a * 0.75);
  if (h.statuses.enraged) a = Math.floor(a * 1.4);
  return Math.max(1, a);
}

function heroDef(h) {
  let d = h.baseDef + h.armor.def
    + (h.accessory.bonus.all || 0)
    + (h.talents["Battle Hardened"] ? 4 : 0);
  if (h.statuses.berserk) d = Math.floor(d * 0.7);
  if (h.statuses.frozen) d = Math.floor(d * 0.55);
  return Math.max(0, d);
}

function getEnemyForFloor(floor) {
  const tier = Math.min(Math.floor((floor - 1) / 5), ENEMIES_BY_TIER.length - 1);
  const pool = ENEMIES_BY_TIER[tier];
  return { ...pool[rnd(0, pool.length - 1)] };
}

function makeElite(floor) {
  const base = getEnemyForFloor(floor);
  return {
    ...base,
    name: "Elite " + base.name,
    hp: Math.floor(base.hp * 2.0),
    maxHp: Math.floor(base.hp * 2.0),
    atk: Math.floor(base.atk * 1.5),
    def: Math.floor(base.def * 1.4),
    xp: Math.floor(base.xp * 2.5),
    gold: Math.floor(base.gold * 2.2),
    elite: true,
    statuses: {},
    skills: [
      { name: "Power Strike", dmg: Math.floor(base.atk * 2.0) },
      { name: "Vicious Blow", dmg: Math.floor(base.atk * 2.5), status: "bleed" },
    ],
  };
}

function makeBossEnemy(floor) {
  const b = BOSSES[floor];
  return { ...b, maxHp: b.hp, statuses: {}, boss: true };
}

// ── SKILL DAMAGE ────────────────────────────────────────────────────
function calcSkillDmg(skill, hero, enemy) {
  const sp = hero.spPower * (1 + (hero.accessory.bonus.spell_power || 0) / 100)
    * (1 + (hero.talents["Arcane Mastery"] ? 15 : 0) / 100);
  const atk = heroAtk(hero);
  const def = heroDef(hero);
  const eDef = enemy.def || 0;
  const giantBonus = (hero.talents["Giant Slayer"] && (enemy.boss || enemy.elite)) ? 1.25 : 1;
  const markedBonus = enemy.statuses?.marked ? 1.3 : 1;

  let dmg = 0;
  let heal = 0;
  let addHeroStatus = [];
  let addEnemyStatus = [];
  let log = "";

  switch (skill.name) {
    case "Shield Bash": dmg = Math.floor((atk * 1.3 + rnd(10, 20))); log = `Shield Bash! ${dmg} dmg`; if (Math.random() < 0.4) addEnemyStatus.push(["stun", 1]); break;
    case "Whirlwind": { const hits = rnd(2, 5); dmg = 0; for (let i = 0; i < hits; i++) dmg += Math.max(1, Math.floor(atk * 0.65 + rnd(4, 10))); log = `Whirlwind! ${hits} hits, ${dmg} total`; break; }
    case "Berserk Mode": addHeroStatus.push(["berserk", 3]); log = "BERSERK! +60% ATK for 3 turns!"; break;
    case "War Cry": addEnemyStatus.push(["weakened", 3]); log = "War Cry! Enemy weakened!"; break;
    case "Earthquake": dmg = Math.floor((atk * 2.8 + rnd(25, 40)) * sp); log = `EARTHQUAKE! ${dmg} dmg`; break;
    case "Titan Smash": dmg = Math.floor(atk * 2.2 + rnd(22, 38)); log = `Titan Smash! ${dmg} dmg (ignores DEF)`; break;
    case "Unbreakable": addHeroStatus.push(["shielded", 2]); log = "UNBREAKABLE! Shielded 2 turns!"; break;
    case "Battle Cry": addHeroStatus.push(["empowered", 4]); log = "Battle Cry! +30% ATK 4 turns!"; break;
    case "Ragnarok": dmg = Math.floor(atk * 3.2 + rnd(30, 55)); addHeroStatus.push(["bleed", 3]); log = `RAGNAROK! ${dmg} dmg! (self-bleed)`; break;
    case "World Breaker": dmg = Math.floor(atk * 4.5 + rnd(40, 70)); log = `WORLD BREAKER! ${dmg} CATASTROPHIC dmg!`; break;
    case "Fireball": dmg = Math.floor((48 + rnd(-8, 15)) * sp); log = `Fireball! ${dmg} dmg`; if (Math.random() < 0.25) addEnemyStatus.push(["burn", 3]); break;
    case "Blizzard": dmg = Math.floor((44 + rnd(-6, 13)) * sp); log = `Blizzard! ${dmg} dmg`; if (Math.random() < 0.3) addEnemyStatus.push(["frozen", 2]); break;
    case "Thunder": dmg = Math.floor((52 + rnd(-8, 16)) * sp); log = `Thunder! ${dmg} dmg`; if (Math.random() < 0.35) addEnemyStatus.push(["stun", 1]); break;
    case "Arcane Bolt": dmg = Math.floor(hero.baseAtk * 2.5 + 35 * sp + rnd(12, 22)); log = `Arcane Bolt! ${dmg} pure magic`; break;
    case "Meteor Strike": dmg = Math.floor((105 + rnd(-12, 24)) * sp); log = `METEOR STRIKE! ${dmg} dmg`; break;
    case "Chain Lightning": { let tot = 0; for (let i = 0; i < 3; i++) tot += Math.floor((40 + rnd(-5, 10)) * sp); dmg = tot; log = `Chain Lightning! 3 strikes, ${tot} total`; if (Math.random() < 0.4) addEnemyStatus.push(["stun", 1]); break; }
    case "Blizzard Storm": dmg = Math.floor((145 + rnd(-15, 28)) * sp); addEnemyStatus.push(["frozen", 3]); log = `Blizzard Storm! ${dmg} dmg + freeze`; break;
    case "Armageddon": dmg = Math.floor((210 + rnd(-20, 40)) * sp); log = `ARMAGEDDON! ${dmg} dmg`; break;
    case "Big Bang": dmg = Math.floor((320 + rnd(-25, 55)) * sp); log = `BIG BANG! ${dmg} ULTIMATE dmg`; break;
    case "Shadowstep": dmg = Math.floor(atk * 2.2 + rnd(16, 28)); log = `Shadowstep! ${dmg} dmg (bypasses DEF)`; break;
    case "Poison Blade": dmg = Math.max(1, atk - eDef + rnd(7, 14)); addEnemyStatus.push(["poison", 5]); log = `Poison Blade! ${dmg} dmg + 5t poison`; break;
    case "Smoke Bomb": addEnemyStatus.push(["bleed", 3]); log = "Smoke Bomb! Bleed applied!"; break;
    case "Mark Target": addEnemyStatus.push(["marked", 4]); log = "Mark Target! +30% dmg taken!"; break;
    case "Death Mark": addHeroStatus.push(["death_mark", 1]); log = "DEATH MARK! Next attack x3!"; break;
    case "Shadow Clone": { const d1 = Math.max(1, atk - eDef + rnd(-2, 6)); const d2 = Math.max(1, atk - eDef + rnd(-2, 6)); dmg = d1 + d2; log = `Shadow Clone! ${d1}+${d2}=${dmg} total`; break; }
    case "Vanish": addHeroStatus.push(["shielded", 1]); log = "Vanished! Enemy skips a turn!"; break;
    case "Acid Splash": dmg = Math.floor((55 + rnd(-8, 14)) * sp); addEnemyStatus.push(["acid", 4]); log = `Acid Splash! ${dmg} dmg + acid`; break;
    case "Assassination": dmg = Math.floor(enemy.hp * 0.6); log = `ASSASSINATION! ${dmg} dmg!`; break;
    case "Oblivion Strike": dmg = Math.min(999, enemy.hp - 1); log = `OBLIVION STRIKE! ${dmg} dmg!`; break;
    case "Holy Strike": dmg = Math.floor((atk * 1.55 + rnd(12, 22)) * sp); heal = rnd(12, 24); log = `Holy Strike! ${dmg} dmg, +${heal} HP`; break;
    case "Divine Shield": addHeroStatus.push(["shielded", 1]); log = "Divine Shield!"; break;
    case "Smite": dmg = Math.floor((58 + rnd(-10, 18)) * sp); addEnemyStatus.push(["cursed", 3]); log = `Smite! ${dmg} dmg + cursed`; break;
    case "Consecrate": addHeroStatus.push(["regen", 4]); addHeroStatus.push(["blessed", 4]); log = "Consecrate! Regen+Blessed 4t!"; break;
    case "Resurrection": addHeroStatus.push(["resurrection_ready", 99]); log = "RESURRECTION armed!"; break;
    case "Holy Nova": dmg = Math.floor((88 + rnd(-10, 22)) * sp); heal = rnd(18, 32); log = `Holy Nova! ${dmg} dmg +${heal} HP, debuffs cleansed`; break;
    case "Sacred Flame": dmg = Math.floor((70 + rnd(-8, 18)) * sp); addEnemyStatus.push(["burn", 4]); addEnemyStatus.push(["blind", 3]); log = `Sacred Flame! ${dmg} dmg + burn + blind`; break;
    case "Aura of Light": addHeroStatus.push(["barrier", 60]); log = "Aura of Light! Barrier absorbs 60 dmg!"; break;
    case "Divine Judgment": dmg = Math.floor((165 + rnd(-15, 32)) * sp); heal = rnd(22, 38); addHeroStatus.push(["regen", 5]); log = `DIVINE JUDGMENT! ${dmg} dmg +${heal} HP`; break;
    case "Holy Apocalypse": dmg = Math.floor((280 + rnd(-20, 50)) * sp); heal = Math.floor(dmg * 0.3); log = `HOLY APOCALYPSE! ${dmg} dmg! Healed ${heal}! All debuffs cleared!`; break;
    case "Drain Life": dmg = Math.floor((50 + rnd(-8, 14)) * sp); heal = Math.floor(dmg / 2); log = `Drain Life! ${dmg} dmg, +${heal} HP`; break;
    case "Bone Spear": dmg = Math.floor((55 + rnd(-6, 16)) * sp); log = `Bone Spear! ${dmg} piercing`; break;
    case "Curse of Decay": addEnemyStatus.push(["poison", 5]); addEnemyStatus.push(["weakened", 3]); log = "Curse of Decay! Poisoned+weakened!"; break;
    case "Soul Rend": dmg = Math.floor((80 + rnd(-10, 20)) * sp); log = `Soul Rend! ${dmg} dmg`; break;
    case "Raise Dead": dmg = Math.floor(atk * 1.8 + rnd(15, 30)); log = `Undead ally attacks for ${dmg} dmg!`; break;
    case "Death Coil": dmg = Math.floor((70 + rnd(-8, 18)) * sp); heal = Math.floor(dmg * 0.35); log = `Death Coil! ${dmg} dmg, +${heal} HP`; break;
    case "Plague": addEnemyStatus.push(["poison", 4]); addEnemyStatus.push(["acid", 4]); addEnemyStatus.push(["bleed", 4]); log = "PLAGUE! Poison+Acid+Bleed 4 turns!"; break;
    case "Soul Harvest": heal = 9999; log = "Soul Harvest! Fully healed!"; break;
    case "Lich Form": addHeroStatus.push(["berserk", 5]); addHeroStatus.push(["regen", 5]); addHeroStatus.push(["empowered", 5]); log = "LICH FORM! Empowered 5 turns!"; break;
    case "Death Nova": dmg = Math.floor((250 + rnd(-20, 45)) * sp); log = `DEATH NOVA! ${dmg} necrotic dmg`; break;
    case "Cleave": dmg = Math.max(1, atk - Math.max(0, eDef - 4) + rnd(5, 18)); log = `Cleave! ${dmg} dmg`; break;
    case "Battle Rage": addHeroStatus.push(["empowered", 4]); log = "Battle Rage! +40% ATK 4t!"; break;
    case "Bloodlust": addHeroStatus.push(["vampiric", 4]); log = "Bloodlust! Vampiric 4 turns!"; break;
    case "Rampage": { const hits = rnd(3, 6); dmg = 0; for (let i = 0; i < hits; i++) dmg += Math.max(1, Math.floor(atk * 0.7 + rnd(5, 12))); log = `Rampage! ${hits} hits, ${dmg} total`; break; }
    case "Enrage": addHeroStatus.push(["enraged", 4]); log = "ENRAGED!"; break;
    case "Skull Crack": dmg = Math.floor(atk * 1.8 + rnd(15, 25)); addEnemyStatus.push(["stun", 1]); addEnemyStatus.push(["blind", 2]); log = `Skull Crack! ${dmg} dmg + stun + blind`; break;
    case "Endless Fury": { dmg = 0; for (let i = 0; i < 5; i++) dmg += Math.floor(atk * 0.9 + rnd(8, 16)); log = `Endless Fury! 5 hits = ${dmg} total`; break; }
    case "Blood Frenzy": addHeroStatus.push(["berserk", 3]); addHeroStatus.push(["vampiric", 3]); log = "Blood Frenzy! Berserk+Vampiric 3t!"; break;
    case "Obliterate": dmg = Math.floor(atk * 3.8 + rnd(35, 60)); log = `OBLITERATE! ${dmg} dmg`; break;
    case "Armageddon Fist": dmg = Math.floor(atk * 6.0 + rnd(60, 100)); log = `ARMAGEDDON FIST! ${dmg} GODLIKE dmg!`; break;
    case "Mana Surge": return { dmg: 0, heal: 0, heroMp: 35, heroHpCost: 22, addHeroStatus: [], addEnemyStatus: [], log: "Mana Surge! -22 HP, +35 MP!" };
    default: dmg = Math.floor(atk * 1.2); log = `${skill.name}! ${dmg} dmg`;
  }

  dmg = Math.floor(dmg * markedBonus * giantBonus);
  return { dmg, heal, addHeroStatus, addEnemyStatus, log };
}

// ── COMPONENTS ───────────────────────────────────────────────────────
function HpBar({ cur, max, color = "#e53e3e", height = 8 }) {
  const pct = Math.max(0, Math.min(1, (cur || 0) / Math.max(1, max || 1)));
  const col = pct > 0.5 ? "#38a169" : pct > 0.25 ? "#d69e2e" : "#e53e3e";
  return (
    <div style={{ background: "var(--color-background-secondary)", borderRadius: 4, overflow: "hidden", height }}>
      <div style={{ width: `${pct * 100}%`, height: "100%", background: col, transition: "width 0.3s ease", borderRadius: 4 }} />
    </div>
  );
}

function MpBar({ cur, max }) {
  const pct = Math.max(0, Math.min(1, (cur || 0) / Math.max(1, max || 1)));
  return (
    <div style={{ background: "var(--color-background-secondary)", borderRadius: 4, overflow: "hidden", height: 6 }}>
      <div style={{ width: `${pct * 100}%`, height: "100%", background: "#6b46c1", transition: "width 0.3s ease", borderRadius: 4 }} />
    </div>
  );
}

function StatusBadges({ statuses }) {
  const entries = Object.keys(statuses || {}).filter(s => statuses[s] > 0);
  if (!entries.length) return null;
  return (
    <div style={{ display: "flex", flexWrap: "wrap", gap: 4, marginTop: 4 }}>
      {entries.map(s => (
        <span key={s} style={{ fontSize: 11, padding: "1px 6px", borderRadius: 10, background: "var(--color-background-secondary)", border: "0.5px solid var(--color-border-secondary)", color: "var(--color-text-secondary)" }}>
          {STATUS_ICONS[s] || "?"} {s} {typeof statuses[s] === "number" && statuses[s] < 99 ? `(${statuses[s]})` : ""}
        </span>
      ))}
    </div>
  );
}

function CombatLog({ log }) {
  const ref = useRef(null);
  useEffect(() => { if (ref.current) ref.current.scrollTop = ref.current.scrollHeight; }, [log]);
  return (
    <div ref={ref} style={{ background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)", padding: "10px 12px", height: 180, overflowY: "auto", fontSize: 13, lineHeight: 1.7, color: "var(--color-text-secondary)", border: "0.5px solid var(--color-border-tertiary)" }}>
      {log.length === 0 ? <span style={{ color: "var(--color-text-tertiary)" }}>Battle log...</span> : log.map((line, i) => (
        <div key={i} style={{ color: line.startsWith("  ✅") || line.startsWith("  🏆") ? "var(--color-text-success)" : line.startsWith("  💀") || line.startsWith("  ❌") ? "var(--color-text-danger)" : "var(--color-text-secondary)" }}>{line}</div>
      ))}
    </div>
  );
}

// ── SCREENS ──────────────────────────────────────────────────────────

function CharSelect({ onStart }) {
  const [name, setName] = useState("");
  const [cls, setCls] = useState(null);
  const classes = ["Warrior", "Mage", "Rogue", "Paladin", "Necromancer", "Berserker"];
  const descs = {
    Warrior: "Tank & berserk combos", Mage: "Fragile, massive spells",
    Rogue: "Poison & assassination", Paladin: "Self-heal & holy power",
    Necromancer: "Drain & undead", Berserker: "Raw power & vampiric",
  };
  const icons = { Warrior: "⚔️", Mage: "🔮", Rogue: "🗡️", Paladin: "✝️", Necromancer: "💀", Berserker: "🔴" };

  return (
    <div style={{ maxWidth: 560, margin: "0 auto", padding: "2rem 1rem" }}>
      <div style={{ textAlign: "center", marginBottom: "2rem" }}>
        <div style={{ fontSize: 48, marginBottom: 8 }}>🐉</div>
        <h1 style={{ fontSize: 26, fontWeight: 500, margin: 0 }}>Dragon Quest</h1>
        <p style={{ color: "var(--color-text-secondary)", fontSize: 14, marginTop: 4 }}>Maximum Edition · 40 Floors · 8 Bosses</p>
      </div>

      <div style={{ marginBottom: "1.5rem" }}>
        <label style={{ display: "block", fontSize: 13, color: "var(--color-text-secondary)", marginBottom: 6 }}>Hero name</label>
        <input value={name} onChange={e => setName(e.target.value)} placeholder="Enter your name..." style={{ width: "100%", boxSizing: "border-box" }} maxLength={20} />
      </div>

      <div style={{ marginBottom: "1.5rem" }}>
        <label style={{ display: "block", fontSize: 13, color: "var(--color-text-secondary)", marginBottom: 8 }}>Choose your class</label>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 8 }}>
          {classes.map(c => (
            <button key={c} onClick={() => setCls(c)} style={{ padding: "12px 8px", border: `2px solid ${cls === c ? "var(--color-border-info)" : "var(--color-border-tertiary)"}`, background: cls === c ? "var(--color-background-info)" : "var(--color-background-primary)", borderRadius: "var(--border-radius-md)", cursor: "pointer", textAlign: "center", transition: "all 0.15s" }}>
              <div style={{ fontSize: 22, marginBottom: 4 }}>{icons[c]}</div>
              <div style={{ fontSize: 13, fontWeight: 500, color: "var(--color-text-primary)" }}>{c}</div>
              <div style={{ fontSize: 11, color: "var(--color-text-secondary)", marginTop: 2 }}>{descs[c]}</div>
            </button>
          ))}
        </div>
      </div>

      <button onClick={() => cls && onStart(name.trim() || "Hero", cls)} disabled={!cls} style={{ width: "100%", padding: "12px", fontSize: 15, fontWeight: 500, cursor: cls ? "pointer" : "not-allowed", opacity: cls ? 1 : 0.5 }}>
        Begin Adventure ↗
      </button>
    </div>
  );
}

// ── MAIN GAME ────────────────────────────────────────────────────────
function Game({ heroInit }) {
  const [hero, setHero] = useState(heroInit);
  const [floor, setFloor] = useState(1);
  const [scene, setScene] = useState("town"); // town | battle | shop | inn | talent | companion | gamble | bank | victory | defeat
  const [enemy, setEnemy] = useState(null);
  const [combatLog, setCombatLog] = useState([]);
  const [turn, setTurn] = useState(1);
  const [skillMenu, setSkillMenu] = useState(false);
  const [battlePhase, setBattlePhase] = useState("player"); // player | enemy | end
  const [showStats, setShowStats] = useState(false);
  const [notification, setNotification] = useState(null);
  const [gambetAmt, setGambetAmt] = useState(10);

  const notify = (msg, type = "info") => {
    setNotification({ msg, type });
    setTimeout(() => setNotification(null), 2200);
  };

  const updateHero = useCallback((fn) => setHero(h => fn({ ...h })), []);

  // ── XP / Level ──
  const gainXp = useCallback((hero, amount) => {
    const bonus = hero.talents["Ancient Knowledge"] ? Math.floor(amount * 0.2) : 0;
    amount += bonus;
    let h = { ...hero, xp: hero.xp + amount };
    while (h.xp >= h.xpNext) {
      h.xp -= h.xpNext;
      h.xpNext = Math.floor(h.xpNext * 1.4);
      h.level += 1;
      const hpGain = rnd(14, 24), atkGain = rnd(2, 5), defGain = rnd(1, 3), mpGain = rnd(8, 14);
      h.maxHp += hpGain; h.hp = h.maxHp;
      h.baseAtk += atkGain; h.baseDef += defGain;
      h.maxMp += mpGain; h.mp = h.maxMp;
      h.talentPoints += 1;
      const newSkills = ALL_SKILLS[h.cls].filter(s => s.ul <= h.level && !h.skills.find(sk => sk.name === s.name));
      h.skills = [...h.skills, ...newSkills];
      notify(`Level up! Now level ${h.level}!`, "success");
    }
    return h;
  }, []);

  // ── Start battle ──
  const startBattle = useCallback((type = "normal") => {
    let e;
    if (type === "boss") e = makeBossEnemy(floor);
    else if (type === "elite") e = makeElite(floor);
    else {
      e = getEnemyForFloor(floor);
      e.maxHp = e.hp;
      e.statuses = {};
    }
    setEnemy(e);
    setCombatLog([`  ${e.emoji} ${e.name} appears!`]);
    setTurn(1);
    setSkillMenu(false);
    setBattlePhase("player");
    setScene("battle");
  }, [floor]);

  // ── Advance floor ──
  const advanceFloor = useCallback(() => {
    const next = floor + 1;
    if (next > 40) { setScene("victory"); return; }
    setFloor(next);
    updateHero(h => {
      // companion upkeep
      if (h.companion) {
        if (h.gold >= h.companion.upkeep) return { ...h, gold: h.gold - h.companion.upkeep, floorsCleared: h.floorsCleared + 1 };
        else { notify("You can't afford companion upkeep!", "danger"); return { ...h, companion: null, floorsCleared: h.floorsCleared + 1 }; }
      }
      return { ...h, floorsCleared: h.floorsCleared + 1 };
    });
    if ([5, 10, 15, 20, 25, 30, 36, 40].includes(next)) {
      setTimeout(() => startBattle("boss"), 100);
    } else {
      setScene("town");
    }
  }, [floor, startBattle, updateHero]);

  // ── Player attack ──
  const doAttack = useCallback(() => {
    if (battlePhase !== "player" || !enemy) return;
    const h = hero;
    const atk = heroAtk(h);
    const def = enemy.def || 0;
    const critChance = 0.15 + (h.accessory.bonus.crit || 0) / 100 + (h.talents["Lucky Strike"] ? 8 / 100 : 0);
    const crit = Math.random() < critChance;
    let dmg = Math.max(1, atk - def + rnd(-4, 8));
    if (h.statuses.death_mark) { dmg *= 3; }
    if (h.talents["Giant Slayer"] && (enemy.boss || enemy.elite)) dmg = Math.floor(dmg * 1.25);
    if (enemy.statuses?.marked) dmg = Math.floor(dmg * 1.3);
    if (crit) dmg = Math.floor(dmg * 2.1);
    const dr = h.talents["Thick Skin"] ? 0.08 : 0;
    const logLine = crit ? `  💥 CRITICAL! ${dmg} damage!` : `  ⚔️  You attack for ${dmg} dmg!`;

    const newStatuses = { ...h.statuses };
    delete newStatuses.death_mark;

    let newEnemy = { ...enemy, hp: Math.max(0, enemy.hp - dmg), statuses: { ...(enemy.statuses || {}) } };

    // weapon procs
    const wn = h.weapon.name;
    if (wn === "Flame Sword" && Math.random() < 0.2) newEnemy.statuses.burn = 3;
    if (wn === "Thunder Blade" && Math.random() < 0.18) newEnemy.statuses.stun = 1;
    if (wn === "Frost Edge" && Math.random() < 0.22) newEnemy.statuses.frozen = 2;
    if (wn === "Void Saber" && Math.random() < 0.28) newEnemy.statuses.bleed = 3;
    if (wn === "Dragon Fang" && Math.random() < 0.3) newEnemy.statuses.burn = 3;
    if (wn === "Dragon Fang" && Math.random() < 0.3) newEnemy.statuses.bleed = 3;

    let newHp = h.hp;
    if (wn === "Soul Reaper") { const steal = Math.floor(dmg * 0.15); newHp = Math.min(h.maxHp, h.hp + steal); }
    const ls = (h.accessory.bonus.lifesteal || 0) + (h.talents["Bloodthirst"] ? 10 : 0);
    if (ls) { const steal2 = Math.floor(dmg * ls / 100); newHp = Math.min(h.maxHp, newHp + steal2); }

    setEnemy(newEnemy);
    updateHero(prev => ({ ...prev, hp: newHp, statuses: newStatuses, totalDmg: prev.totalDmg + dmg }));
    setCombatLog(l => [...l, logLine]);
    setBattlePhase("enemy");

    if (newEnemy.hp <= 0) { handleVictory(newEnemy); return; }

    setTimeout(() => doEnemyTurn(newEnemy), 700);
  }, [battlePhase, enemy, hero]);

  // ── Use skill ──
  const doSkill = useCallback((skill) => {
    if (battlePhase !== "player" || !enemy) return;
    const h = hero;
    if (h.mp < skill.mp) { notify(`Need ${skill.mp} MP!`, "danger"); return; }

    const result = calcSkillDmg(skill, h, enemy);
    let newH = { ...h, mp: h.mp - skill.mp, skillUses: h.skillUses + 1 };
    let newEnemy = { ...enemy };
    const logs = [`  ✨ ${skill.name}! ${result.log}`];

    if (result.dmg > 0) {
      newEnemy = { ...newEnemy, hp: Math.max(0, newEnemy.hp - result.dmg) };
      newH.totalDmg += result.dmg;
    }
    if (result.heroHpCost) { newH.hp = Math.max(1, newH.hp - result.heroHpCost); }
    if (result.heroMp) { newH.mp = Math.min(newH.maxMp, newH.mp + result.heroMp); }
    if (result.heal) { newH.hp = Math.min(newH.maxHp, newH.hp + result.heal); }
    if (result.addHeroStatus) {
      for (const [st, turns] of result.addHeroStatus) {
        if (st === "barrier") newH.statuses = { ...newH.statuses, barrier: turns };
        else newH.statuses = { ...newH.statuses, [st]: turns };
      }
    }
    if (result.addEnemyStatus) {
      for (const [st, turns] of result.addEnemyStatus) {
        newEnemy.statuses = { ...(newEnemy.statuses || {}), [st]: turns };
        logs.push(`  ${STATUS_ICONS[st] || "?"} ${newEnemy.name} is ${st}!`);
      }
    }
    if (skill.name === "Holy Nova" || skill.name === "Holy Apocalypse") {
      const bad = ["poison", "burn", "bleed", "acid", "cursed", "frozen", "stun", "blind"];
      const ns = { ...newH.statuses };
      bad.forEach(b => delete ns[b]);
      newH.statuses = ns;
    }

    setSkillMenu(false);
    setEnemy(newEnemy);
    setHero(newH);
    setCombatLog(l => [...l, ...logs]);
    setBattlePhase("enemy");

    if (newEnemy.hp <= 0) { handleVictory(newEnemy); return; }
    setTimeout(() => doEnemyTurn(newEnemy), 700);
  }, [battlePhase, enemy, hero]);

  // ── Enemy turn ──
  const doEnemyTurn = useCallback((currentEnemy) => {
    if (!currentEnemy || currentEnemy.hp <= 0) return;

    setHero(prevH => {
      const h = { ...prevH };

      // hero status tick
      const hStatuses = { ...h.statuses };
      let statusDmg = 0;
      let statusHeal = 0;
      const toRemove = [];
      for (const [st, turns] of Object.entries(hStatuses)) {
        if (DOT_STATUSES.has(st)) { const d = rnd(3, 10); statusDmg += d; }
        if (HEAL_STATUSES.has(st)) { const heal = rnd(5, 14); statusHeal += heal; }
        if (st !== "resurrection_ready" && st !== "shielded" && st !== "vampiric" && st !== "barrier") {
          hStatuses[st] = turns - 1;
          if (hStatuses[st] <= 0) toRemove.push(st);
        }
      }
      toRemove.forEach(st => delete hStatuses[st]);
      if (statusDmg > 0) setCombatLog(l => [...l, `  ☠️ Status effects: -${statusDmg} HP`]);
      if (statusHeal > 0) setCombatLog(l => [...l, `  💚 Status healing: +${statusHeal} HP`]);

      // enemy status tick
      const eStatuses = { ...(currentEnemy.statuses || {}) };
      let enemyStatusDmg = 0;
      const eToRemove = [];
      for (const [st, turns] of Object.entries(eStatuses)) {
        if (DOT_STATUSES.has(st)) { const d = rnd(4, 12); enemyStatusDmg += d; }
        eStatuses[st] = turns - 1;
        if (eStatuses[st] <= 0) eToRemove.push(st);
      }
      eToRemove.forEach(st => delete eStatuses[st]);

      setEnemy(prev => {
        if (!prev) return prev;
        const newHp = Math.max(0, prev.hp - enemyStatusDmg);
        if (enemyStatusDmg > 0) setCombatLog(l => [...l, `  ☠️ ${prev.name} takes ${enemyStatusDmg} from statuses`]);
        const updated = { ...prev, hp: newHp, statuses: eStatuses };
        if (newHp <= 0) {
          setTimeout(() => handleVictory(updated), 100);
        }
        return updated;
      });

      // mp regen
      const mpRegen = (h.accessory.bonus.mp_regen || 0) + (h.talents["Mana Fountain"] ? 8 : 0);
      h.mp = Math.min(h.maxMp, h.mp + mpRegen);

      // companion action
      if (h.companion) {
        const c = h.companion;
        if (c.type === "heal") { const ch = rnd(c.power - 8, c.power + 8); h.hp = Math.min(h.maxHp, h.hp + ch); setCombatLog(l => [...l, `  ${c.emoji} ${c.name} heals ${ch} HP`]); }
      }

      // can enemy attack?
      if (Object.keys(eStatuses).some(s => SKIP_STATUSES.has(s))) {
        setCombatLog(l => [...l, `  ⚡ ${currentEnemy.name} can't move!`]);
        return { ...h, hp: Math.max(0, h.hp + statusHeal - statusDmg), statuses: hStatuses };
      }
      if (hStatuses.shielded) {
        delete hStatuses.shielded;
        setCombatLog(l => [...l, "  🛡️ Shield blocks the attack!"]);
        return { ...h, hp: Math.max(0, h.hp + statusHeal - statusDmg), statuses: hStatuses };
      }

      // enemy attacks
      if (Math.random() < 0.08) {
        setCombatLog(l => [...l, `  💨 ${currentEnemy.name} missed!`]);
        return { ...h, hp: Math.max(0, h.hp + statusHeal - statusDmg), statuses: hStatuses };
      }

      let eDmg = currentEnemy.atk - heroDef(h) + rnd(-4, 7);
      if (eStatuses.cursed) eDmg = Math.floor(eDmg * 0.5);
      if (h.talents["Thick Skin"]) eDmg = Math.floor(eDmg * 0.92);
      eDmg = Math.max(1, eDmg);

      // boss skill
      if ((currentEnemy.boss || currentEnemy.elite) && currentEnemy.skills?.length && Math.random() < 0.4) {
        const sk = currentEnemy.skills[rnd(0, currentEnemy.skills.length - 1)];
        const skDmg = Math.max(1, (sk.dmg || 0) - heroDef(h) + rnd(-5, 10));
        eDmg = skDmg;
        setCombatLog(l => [...l, `  ${currentEnemy.emoji} ${currentEnemy.name} uses ${sk.name}! ${skDmg} dmg!`]);
        if (sk.status) { hStatuses[sk.status] = sk.turns || 2; }
      } else {
        setCombatLog(l => [...l, `  ${currentEnemy.emoji} ${currentEnemy.name} attacks for ${eDmg} dmg`]);
      }

      let newHp = Math.max(0, h.hp + statusHeal - statusDmg - eDmg);

      // iron will
      if (newHp <= 0 && h.talents["Iron Will"] && !h.ironWillUsed) {
        newHp = 1;
        hStatuses.ironWillUsed = true;
        setCombatLog(l => [...l, "  💎 IRON WILL! Survived at 1 HP!"]);
      }

      // phoenix feather
      if (newHp <= 0 && h.accessory.bonus.revive && !h.reviveUsed) {
        newHp = Math.floor(h.maxHp / 2);
        setCombatLog(l => [...l, "  🪶 Phoenix Feather! Revived!"]);
        return { ...h, hp: newHp, statuses: hStatuses, reviveUsed: true };
      }

      if (newHp <= 0) {
        setCombatLog(l => [...l, `  💀 ${h.name} has fallen...`]);
        setTimeout(() => setScene("defeat"), 1000);
      }

      setTurn(t => t + 1);
      setBattlePhase("player");
      return { ...h, hp: newHp, statuses: hStatuses };
    });
  }, []);

  const handleVictory = useCallback((defeatedEnemy) => {
    setBattlePhase("end");
    setHero(prev => {
      let loot = defeatedEnemy.gold + rnd(-5, 12);
      if (prev.talents["Gold Sense"]) loot = Math.floor(loot * 1.25);
      const newH = gainXp({ ...prev, kills: prev.kills + 1, bossKills: prev.bossKills + (defeatedEnemy.boss ? 1 : 0), gold: prev.gold + loot, totalGoldEarned: prev.totalGoldEarned + loot }, defeatedEnemy.xp);
      if (Math.random() < 0.12) newH.potions += 1;
      if ((defeatedEnemy.boss || defeatedEnemy.elite) && Math.random() < 0.3) newH.elixirs += 1;
      setCombatLog(l => [...l, `  🏆 Victory! +${loot} gold, +${defeatedEnemy.xp} XP`]);
      return newH;
    });
  }, [gainXp]);

  const doPotion = useCallback(() => {
    if (hero.potions <= 0) { notify("No potions!", "danger"); return; }
    const h = rnd(32, 55);
    updateHero(prev => ({ ...prev, hp: Math.min(prev.maxHp, prev.hp + h), potions: prev.potions - 1 }));
    setCombatLog(l => [...l, `  🧪 Potion! +${h} HP`]);
  }, [hero.potions, updateHero]);

  const doElixir = useCallback(() => {
    if (hero.elixirs <= 0) { notify("No elixirs!", "danger"); return; }
    updateHero(prev => ({ ...prev, hp: prev.maxHp, mp: prev.maxMp, elixirs: prev.elixirs - 1 }));
    setCombatLog(l => [...l, "  💊 Elixir! Fully restored!"]);
  }, [hero.elixirs, updateHero]);

  const doDefend = useCallback(() => {
    setBattlePhase("enemy");
    setCombatLog(l => [...l, "  🛡️ Defending... (40% reduced dmg)"]);
    // simplified defend: just small heal to represent reduced damage
    updateHero(prev => ({ ...prev, hp: Math.min(prev.maxHp, prev.hp + 8) }));
    setTimeout(() => doEnemyTurn(enemy), 500);
  }, [enemy, doEnemyTurn, updateHero]);

  const doFlee = useCallback(() => {
    if (Math.random() < 0.38) { notify("Escaped!", "success"); setScene("town"); }
    else { notify("Couldn't escape!", "danger"); doEnemyTurn(enemy); }
  }, [enemy, doEnemyTurn]);

  // ── SHOP ──
  const buyItem = useCallback((type, item) => {
    if (hero.gold < item.price) { notify("Not enough gold!", "danger"); return; }
    updateHero(prev => {
      if (type === "weapon") {
        if (prev.weapon.atk >= item.atk) { notify("Already have better weapon!", "danger"); return prev; }
        return { ...prev, gold: prev.gold - item.price, weapon: { ...item } };
      }
      if (type === "armor") {
        if (prev.armor.def >= item.def) { notify("Already have better armor!", "danger"); return prev; }
        return { ...prev, gold: prev.gold - item.price, armor: { ...item } };
      }
      if (type === "accessory") return { ...prev, gold: prev.gold - item.price, accessory: { ...item } };
      if (type === "potion") return { ...prev, gold: prev.gold - item.price, potions: prev.potions + 1 };
      if (type === "elixir") return { ...prev, gold: prev.gold - item.price, elixirs: prev.elixirs + 1 };
      if (type === "antidote") return { ...prev, gold: prev.gold - item.price, antidotes: prev.antidotes + 1 };
      if (type === "atk_dust") return { ...prev, gold: prev.gold - 16, baseAtk: prev.baseAtk + 4 };
      if (type === "def_plate") return { ...prev, gold: prev.gold - 16, baseDef: prev.baseDef + 4 };
      if (type === "mp_shard") return { ...prev, gold: prev.gold - 16, maxMp: prev.maxMp + 15, mp: Math.min(prev.maxMp + 15, prev.mp + 15) };
      return prev;
    });
    notify(`Bought ${item.name || type}!`, "success");
  }, [hero.gold, updateHero]);

  // ── TALENT ──
  const buyTalent = useCallback((talent) => {
    if (hero.talentPoints < talent.cost) { notify("Not enough talent points!", "danger"); return; }
    if (hero.talents[talent.name]) { notify("Already owned!", "danger"); return; }
    updateHero(prev => {
      const newH = { ...prev, talentPoints: prev.talentPoints - talent.cost, talents: { ...prev.talents, [talent.name]: 1 } };
      if (talent.effect === "max_hp") { newH.maxHp += talent.amount; newH.hp = newH.maxHp; }
      if (talent.effect === "max_mp") { newH.maxMp += talent.amount; newH.mp = newH.maxMp; }
      if (talent.effect === "base_def") newH.baseDef += talent.amount;
      if (talent.effect === "base_atk") newH.baseAtk += talent.amount;
      if (talent.effect === "tough") { newH.maxHp += talent.amount; newH.baseDef += 5; newH.hp = newH.maxHp; }
      return newH;
    });
    notify(`Talent '${talent.name}' purchased!`, "success");
  }, [hero.talentPoints, hero.talents, updateHero]);

  // ── COMPANION ──
  const hireCompanion = useCallback((comp) => {
    if (hero.gold < comp.hire_cost) { notify("Not enough gold!", "danger"); return; }
    updateHero(prev => ({ ...prev, gold: prev.gold - comp.hire_cost, companion: comp }));
    notify(`${comp.name} joins your party!`, "success");
  }, [hero.gold, updateHero]);

  // ── INN ──
  const innRest = useCallback((type) => {
    const cost = 12 + hero.level * 2;
    updateHero(prev => {
      if (type === "full") {
        if (prev.gold < cost) { notify("Not enough gold!", "danger"); return prev; }
        notify("Fully rested!", "success");
        return { ...prev, gold: prev.gold - cost, hp: prev.maxHp, mp: prev.maxMp, statuses: {} };
      }
      const half = Math.floor(cost / 2);
      if (prev.gold < half) { notify("Not enough gold!", "danger"); return prev; }
      if (type === "hp") { const g = Math.floor(prev.maxHp * 0.45); notify(`+${g} HP`, "success"); return { ...prev, gold: prev.gold - half, hp: Math.min(prev.maxHp, prev.hp + g) }; }
      if (type === "mp") { const g = Math.floor(prev.maxMp * 0.5); notify(`+${g} MP`, "success"); return { ...prev, gold: prev.gold - half, mp: Math.min(prev.maxMp, prev.mp + g) }; }
      return prev;
    });
  }, [hero.level, updateHero]);

  // ── BANK ──
  const bankOp = useCallback((type, amt) => {
    updateHero(prev => {
      if (type === "deposit") {
        const a = Math.min(amt, prev.gold);
        return { ...prev, gold: prev.gold - a, bank: prev.bank + a };
      }
      if (type === "withdraw") {
        const a = Math.min(amt, prev.bank);
        return { ...prev, gold: prev.gold + a, bank: prev.bank - a };
      }
      if (type === "interest") {
        const i = Math.floor(prev.bank * 0.05);
        if (i <= 0) { notify("No interest yet!", "danger"); return prev; }
        notify(`+${i} gold interest!`, "success");
        return { ...prev, gold: prev.gold + i };
      }
      return prev;
    });
  }, [updateHero]);

  // ── GAMBLE ──
  const doGamble = useCallback((type, bet, guess) => {
    if (hero.gold < bet) { notify("Not enough gold!", "danger"); return; }
    updateHero(prev => {
      let won = false, winnings = 0;
      if (type === "flip") { const flip = Math.random() < 0.5 ? "H" : "T"; won = flip === guess; winnings = bet * 2; }
      if (type === "highroll") { const roll = rnd(1, 6); won = roll >= 4; winnings = Math.floor(bet * 2.5); }
      if (type === "lucky") { const roll = rnd(1, 6); won = roll === guess; winnings = bet * 5; }
      if (type === "double") { won = Math.random() < 0.4; winnings = bet * 3; }
      if (won) { notify(`Won! +${winnings} gold!`, "success"); return { ...prev, gold: prev.gold - bet + winnings, totalGoldEarned: prev.totalGoldEarned + winnings - bet, gamblesWon: prev.gamblesWon + 1 }; }
      else { notify(`Lost ${bet} gold!`, "danger"); return { ...prev, gold: prev.gold - bet }; }
    });
  }, [hero.gold, updateHero]);

  const isBossFloor = [5, 10, 15, 20, 25, 30, 36, 40].includes(floor);

  // ── RENDER ───────────────────────────────────────────────────────
  const tierColor = (tier) => ["#888", "#2d8a4e", "#2563eb", "#7c3aed", "#c2400c", "#92400e"][tier] || "#888";

  if (scene === "victory") return (
    <div style={{ maxWidth: 480, margin: "0 auto", padding: "3rem 1rem", textAlign: "center" }}>
      <div style={{ fontSize: 56, marginBottom: 12 }}>🏆</div>
      <h1 style={{ fontSize: 24, fontWeight: 500 }}>Victory!</h1>
      <p style={{ color: "var(--color-text-secondary)" }}>The Dragon Lord is slain. {hero.name} is a legend!</p>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, margin: "1.5rem 0" }}>
        {[["Level", hero.level], ["Kills", hero.kills], ["Floors", "40/40"], ["Gold earned", hero.totalGoldEarned]].map(([k, v]) => (
          <div key={k} style={{ background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)", padding: 12 }}>
            <div style={{ fontSize: 12, color: "var(--color-text-secondary)" }}>{k}</div>
            <div style={{ fontSize: 20, fontWeight: 500 }}>{v}</div>
          </div>
        ))}
      </div>
    </div>
  );

  if (scene === "defeat") return (
    <div style={{ maxWidth: 480, margin: "0 auto", padding: "3rem 1rem", textAlign: "center" }}>
      <div style={{ fontSize: 56, marginBottom: 12 }}>💀</div>
      <h1 style={{ fontSize: 24, fontWeight: 500 }}>Defeated</h1>
      <p style={{ color: "var(--color-text-secondary)" }}>{hero.name} fell on floor {floor}.</p>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, margin: "1.5rem 0" }}>
        {[["Level", hero.level], ["Kills", hero.kills], ["Floors", hero.floorsCleared], ["Gold earned", hero.totalGoldEarned]].map(([k, v]) => (
          <div key={k} style={{ background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)", padding: 12 }}>
            <div style={{ fontSize: 12, color: "var(--color-text-secondary)" }}>{k}</div>
            <div style={{ fontSize: 20, fontWeight: 500 }}>{v}</div>
          </div>
        ))}
      </div>
    </div>
  );

  // ── BATTLE SCREEN ──
  if (scene === "battle") return (
    <div style={{ padding: "0.75rem" }}>
      {notification && (
        <div style={{ position: "absolute", top: 8, right: 8, zIndex: 10, background: notification.type === "success" ? "var(--color-background-success)" : notification.type === "danger" ? "var(--color-background-danger)" : "var(--color-background-info)", color: notification.type === "success" ? "var(--color-text-success)" : notification.type === "danger" ? "var(--color-text-danger)" : "var(--color-text-info)", padding: "6px 14px", borderRadius: "var(--border-radius-md)", fontSize: 13, border: "0.5px solid", borderColor: notification.type === "success" ? "var(--color-border-success)" : notification.type === "danger" ? "var(--color-border-danger)" : "var(--color-border-info)" }}>
          {notification.msg}
        </div>
      )}

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: 10 }}>
        {/* Enemy card */}
        <div style={{ background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-lg)", padding: "10px 12px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 6 }}>
            <span style={{ fontSize: 22 }}>{enemy?.emoji}</span>
            <div>
              <div style={{ fontSize: 13, fontWeight: 500 }}>{enemy?.name}</div>
              <div style={{ fontSize: 11, color: "var(--color-text-secondary)" }}>{enemy?.boss ? "⚠️ BOSS" : enemy?.elite ? "⭐ ELITE" : "Enemy"} · Turn {turn}</div>
            </div>
          </div>
          <HpBar cur={enemy?.hp || 0} max={enemy?.maxHp || 1} />
          <div style={{ fontSize: 11, color: "var(--color-text-secondary)", marginTop: 3 }}>{enemy?.hp || 0}/{enemy?.maxHp || 0} HP</div>
          <div style={{ display: "flex", gap: 10, marginTop: 6, fontSize: 12, color: "var(--color-text-secondary)" }}>
            <span>⚔️ {enemy?.atk}</span><span>🛡️ {enemy?.def || 0}</span>
          </div>
          <StatusBadges statuses={enemy?.statuses || {}} />
        </div>

        {/* Hero card */}
        <div style={{ background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-lg)", padding: "10px 12px" }}>
          <div style={{ fontSize: 13, fontWeight: 500, marginBottom: 4 }}>{hero.name} · Lv.{hero.level}</div>
          <HpBar cur={hero.hp} max={hero.maxHp} />
          <div style={{ fontSize: 11, color: "var(--color-text-secondary)", marginTop: 2, marginBottom: 4 }}>{hero.hp}/{hero.maxHp} HP</div>
          <MpBar cur={hero.mp} max={hero.maxMp} />
          <div style={{ fontSize: 11, color: "var(--color-text-secondary)", marginTop: 2 }}>{hero.mp}/{hero.maxMp} MP</div>
          <div style={{ display: "flex", gap: 8, marginTop: 6, fontSize: 12, color: "var(--color-text-secondary)" }}>
            <span>⚔️ {heroAtk(hero)}</span><span>🛡️ {heroDef(hero)}</span><span>🧪×{hero.potions}</span>
          </div>
          <StatusBadges statuses={hero.statuses} />
        </div>
      </div>

      <CombatLog log={combatLog} />

      {battlePhase === "end" ? (
        <div style={{ marginTop: 10 }}>
          <button style={{ width: "100%", padding: 10, fontWeight: 500 }} onClick={advanceFloor}>
            Continue to Floor {floor + 1 <= 40 ? floor + 1 : "..."} ↗
          </button>
        </div>
      ) : skillMenu ? (
        <div style={{ marginTop: 10 }}>
          <div style={{ fontSize: 13, fontWeight: 500, marginBottom: 6, color: "var(--color-text-secondary)" }}>Choose skill ({hero.mp} MP)</div>
          <div style={{ display: "grid", gap: 6 }}>
            {hero.skills.map((sk, i) => (
              <button key={i} onClick={() => doSkill(sk)} disabled={hero.mp < sk.mp || battlePhase !== "player"} style={{ padding: "8px 12px", textAlign: "left", display: "flex", justifyContent: "space-between", opacity: hero.mp < sk.mp ? 0.45 : 1 }}>
                <span>{sk.name} <span style={{ fontSize: 11, color: "var(--color-text-tertiary)" }}>{sk.desc}</span></span>
                <span style={{ fontSize: 12, color: "var(--color-text-secondary)" }}>{sk.mp} MP</span>
              </button>
            ))}
          </div>
          <button onClick={() => setSkillMenu(false)} style={{ width: "100%", marginTop: 6, padding: 8 }}>Cancel</button>
        </div>
      ) : (
        <div style={{ marginTop: 10, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 6 }}>
          <button onClick={doAttack} disabled={battlePhase !== "player"} style={{ padding: "10px 12px", fontWeight: 500 }}>⚔️ Attack</button>
          <button onClick={() => setSkillMenu(true)} disabled={battlePhase !== "player" || hero.skills.length === 0} style={{ padding: "10px 12px", fontWeight: 500 }}>✨ Skill</button>
          <button onClick={doPotion} disabled={battlePhase !== "player" || hero.potions === 0} style={{ padding: "10px 12px", opacity: hero.potions === 0 ? 0.4 : 1 }}>🧪 Potion ({hero.potions})</button>
          <button onClick={doElixir} disabled={battlePhase !== "player" || hero.elixirs === 0} style={{ padding: "10px 12px", opacity: hero.elixirs === 0 ? 0.4 : 1 }}>💊 Elixir ({hero.elixirs})</button>
          <button onClick={doDefend} disabled={battlePhase !== "player"} style={{ padding: "10px 12px" }}>🛡️ Defend</button>
          {!enemy?.boss && !enemy?.elite && <button onClick={doFlee} disabled={battlePhase !== "player"} style={{ padding: "10px 12px" }}>🏃 Flee</button>}
        </div>
      )}
    </div>
  );

  // ── SHOP SCREEN ──
  if (scene === "shop") return (
    <div style={{ padding: "0.75rem" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
        <button onClick={() => setScene("town")} style={{ padding: "4px 10px", fontSize: 12 }}>← Back</button>
        <h2 style={{ fontSize: 16, margin: 0 }}>Shop</h2>
        <span style={{ marginLeft: "auto", fontSize: 13, color: "var(--color-text-secondary)" }}>💰 {hero.gold}g</span>
      </div>

      <div style={{ marginBottom: 12 }}>
        <div style={{ fontSize: 12, fontWeight: 500, color: "var(--color-text-secondary)", marginBottom: 6, textTransform: "uppercase", letterSpacing: "0.05em" }}>Consumables</div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 6 }}>
          {[{ label: "🧪 Potion", price: 8, type: "potion", name: "Potion" }, { label: "💊 Elixir", price: 30, type: "elixir", name: "Elixir" }, { label: "💉 Antidote", price: 7, type: "antidote", name: "Antidote" }, { label: "⚔️ ATK Dust", price: 16, type: "atk_dust", name: "ATK Dust" }, { label: "🛡️ DEF Plate", price: 16, type: "def_plate", name: "DEF Plate" }, { label: "💎 MP Shard", price: 16, type: "mp_shard", name: "MP Shard" }].map(item => (
            <button key={item.type} onClick={() => buyItem(item.type, item)} disabled={hero.gold < item.price} style={{ padding: "8px 6px", fontSize: 12, opacity: hero.gold < item.price ? 0.45 : 1 }}>
              {item.label}<br /><span style={{ color: "var(--color-text-secondary)", fontSize: 11 }}>{item.price}g</span>
            </button>
          ))}
        </div>
      </div>

      {[{ label: "Weapons", items: WEAPONS.slice(1), type: "weapon", prop: "atk", unit: " ATK" }, { label: "Armor", items: ARMORS.slice(1), type: "armor", prop: "def", unit: " DEF" }].map(({ label, items, type, prop, unit }) => (
        <div key={type} style={{ marginBottom: 12 }}>
          <div style={{ fontSize: 12, fontWeight: 500, color: "var(--color-text-secondary)", marginBottom: 6, textTransform: "uppercase", letterSpacing: "0.05em" }}>{label}</div>
          <div style={{ display: "grid", gap: 4 }}>
            {items.map(item => {
              const owned = (type === "weapon" && hero.weapon.name === item.name) || (type === "armor" && hero.armor.name === item.name);
              return (
                <div key={item.name} onClick={() => buyItem(type, item)} style={{ display: "flex", alignItems: "center", padding: "8px 10px", background: owned ? "var(--color-background-success)" : "var(--color-background-primary)", border: `0.5px solid ${owned ? "var(--color-border-success)" : "var(--color-border-tertiary)"}`, borderRadius: "var(--border-radius-md)", cursor: "pointer", gap: 8 }}>
                  <span style={{ fontSize: 11, padding: "1px 5px", borderRadius: 8, background: "var(--color-background-secondary)", color: "var(--color-text-secondary)", fontWeight: 500 }}>T{item.tier}</span>
                  <span style={{ fontSize: 13, flex: 1 }}>{item.name}</span>
                  <span style={{ fontSize: 11, color: "var(--color-text-secondary)" }}>+{item[prop]}{unit}</span>
                  <span style={{ fontSize: 12, color: "var(--color-text-secondary)", minWidth: 32 }}>{owned ? "✅" : `${item.price}g`}</span>
                </div>
              );
            })}
          </div>
        </div>
      ))}

      <div style={{ marginBottom: 12 }}>
        <div style={{ fontSize: 12, fontWeight: 500, color: "var(--color-text-secondary)", marginBottom: 6, textTransform: "uppercase", letterSpacing: "0.05em" }}>Accessories</div>
        <div style={{ display: "grid", gap: 4 }}>
          {ACCESSORIES.slice(1).map(item => {
            const owned = hero.accessory.name === item.name;
            return (
              <div key={item.name} onClick={() => buyItem("accessory", item)} style={{ display: "flex", alignItems: "center", padding: "8px 10px", background: owned ? "var(--color-background-success)" : "var(--color-background-primary)", border: `0.5px solid ${owned ? "var(--color-border-success)" : "var(--color-border-tertiary)"}`, borderRadius: "var(--border-radius-md)", cursor: "pointer", gap: 8 }}>
                <span style={{ fontSize: 11, padding: "1px 5px", borderRadius: 8, background: "var(--color-background-secondary)", color: "var(--color-text-secondary)", fontWeight: 500 }}>T{item.tier}</span>
                <span style={{ fontSize: 13, flex: 1 }}>{item.name}</span>
                <span style={{ fontSize: 11, color: "var(--color-text-secondary)", flex: 1 }}>{item.desc}</span>
                <span style={{ fontSize: 12, color: "var(--color-text-secondary)", minWidth: 32 }}>{owned ? "✅" : `${item.price}g`}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );

  // ── TALENT SCREEN ──
  if (scene === "talent") return (
    <div style={{ padding: "0.75rem" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
        <button onClick={() => setScene("town")} style={{ padding: "4px 10px", fontSize: 12 }}>← Back</button>
        <h2 style={{ fontSize: 16, margin: 0 }}>Talent Tree</h2>
        <span style={{ marginLeft: "auto", fontSize: 13, color: "var(--color-text-secondary)" }}>🧠 {hero.talentPoints} pts</span>
      </div>
      <div style={{ display: "grid", gap: 6 }}>
        {TALENT_TREE.map(t => {
          const owned = !!hero.talents[t.name];
          return (
            <div key={t.name} style={{ display: "flex", alignItems: "center", padding: "10px 12px", background: owned ? "var(--color-background-success)" : "var(--color-background-primary)", border: `0.5px solid ${owned ? "var(--color-border-success)" : "var(--color-border-tertiary)"}`, borderRadius: "var(--border-radius-md)", gap: 10 }}>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 13, fontWeight: 500 }}>{t.name} {owned ? "✅" : ""}</div>
                <div style={{ fontSize: 12, color: "var(--color-text-secondary)" }}>{t.desc}</div>
              </div>
              <button onClick={() => buyTalent(t)} disabled={owned || hero.talentPoints < t.cost} style={{ padding: "5px 10px", fontSize: 12, opacity: (owned || hero.talentPoints < t.cost) ? 0.45 : 1 }}>
                {owned ? "Owned" : `${t.cost} pt`}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );

  // ── COMPANION SCREEN ──
  if (scene === "companion") return (
    <div style={{ padding: "0.75rem" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
        <button onClick={() => setScene("town")} style={{ padding: "4px 10px", fontSize: 12 }}>← Back</button>
        <h2 style={{ fontSize: 16, margin: 0 }}>Tavern</h2>
        <span style={{ marginLeft: "auto", fontSize: 13, color: "var(--color-text-secondary)" }}>💰 {hero.gold}g</span>
      </div>
      {hero.companion && (
        <div style={{ padding: "10px 12px", background: "var(--color-background-success)", border: "0.5px solid var(--color-border-success)", borderRadius: "var(--border-radius-md)", marginBottom: 12, display: "flex", alignItems: "center", gap: 8 }}>
          <span style={{ fontSize: 20 }}>{hero.companion.emoji}</span>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 13, fontWeight: 500 }}>{hero.companion.name} (active)</div>
            <div style={{ fontSize: 12, color: "var(--color-text-secondary)" }}>{hero.companion.ability}</div>
          </div>
          <button onClick={() => { updateHero(h => ({ ...h, companion: null })); notify("Companion dismissed", "info"); }} style={{ padding: "4px 8px", fontSize: 11 }}>Dismiss</button>
        </div>
      )}
      {!hero.companion && (
        <div style={{ display: "grid", gap: 8 }}>
          {COMPANIONS.map(c => (
            <div key={c.name} style={{ display: "flex", alignItems: "center", padding: "10px 12px", background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-md)", gap: 10 }}>
              <span style={{ fontSize: 24 }}>{c.emoji}</span>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 13, fontWeight: 500 }}>{c.name}</div>
                <div style={{ fontSize: 12, color: "var(--color-text-secondary)" }}>{c.ability}</div>
                <div style={{ fontSize: 11, color: "var(--color-text-tertiary)" }}>Upkeep: {c.upkeep}g/floor</div>
              </div>
              <button onClick={() => hireCompanion(c)} disabled={hero.gold < c.hire_cost} style={{ padding: "6px 10px", fontSize: 12, opacity: hero.gold < c.hire_cost ? 0.4 : 1 }}>{c.hire_cost}g</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );

  // ── INN SCREEN ──
  if (scene === "inn") return (
    <div style={{ padding: "0.75rem" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 16 }}>
        <button onClick={() => setScene("town")} style={{ padding: "4px 10px", fontSize: 12 }}>← Back</button>
        <h2 style={{ fontSize: 16, margin: 0 }}>Inn</h2>
        <span style={{ marginLeft: "auto", fontSize: 13, color: "var(--color-text-secondary)" }}>💰 {hero.gold}g</span>
      </div>
      <div style={{ display: "grid", gap: 8 }}>
        {[{ type: "full", label: "Full Rest", sub: "HP+MP+clear debuffs", price: 12 + hero.level * 2 }, { type: "hp", label: "Quick Nap", sub: "Restore 45% HP", price: Math.floor((12 + hero.level * 2) / 2) }, { type: "mp", label: "Meditation", sub: "Restore 50% MP", price: Math.floor((12 + hero.level * 2) / 2) }].map(o => (
          <div key={o.type} style={{ display: "flex", alignItems: "center", padding: "12px 14px", background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-md)", gap: 10 }}>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 14, fontWeight: 500 }}>{o.label}</div>
              <div style={{ fontSize: 12, color: "var(--color-text-secondary)" }}>{o.sub}</div>
            </div>
            <button onClick={() => innRest(o.type)} disabled={hero.gold < o.price} style={{ padding: "7px 12px", opacity: hero.gold < o.price ? 0.4 : 1 }}>{o.price}g</button>
          </div>
        ))}
      </div>
    </div>
  );

  // ── BANK SCREEN ──
  if (scene === "bank") {
    const [bankAmt, setBankAmt] = useState(0);
    return (
      <div style={{ padding: "0.75rem" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 16 }}>
          <button onClick={() => setScene("town")} style={{ padding: "4px 10px", fontSize: 12 }}>← Back</button>
          <h2 style={{ fontSize: 16, margin: 0 }}>Bank</h2>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginBottom: 16 }}>
          <div style={{ background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)", padding: 12, textAlign: "center" }}>
            <div style={{ fontSize: 11, color: "var(--color-text-secondary)" }}>Wallet</div>
            <div style={{ fontSize: 22, fontWeight: 500 }}>💰 {hero.gold}g</div>
          </div>
          <div style={{ background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)", padding: 12, textAlign: "center" }}>
            <div style={{ fontSize: 11, color: "var(--color-text-secondary)" }}>Savings</div>
            <div style={{ fontSize: 22, fontWeight: 500 }}>🏦 {hero.bank}g</div>
          </div>
        </div>
        <div style={{ marginBottom: 12 }}>
          <input type="number" value={bankAmt} onChange={e => setBankAmt(parseInt(e.target.value) || 0)} min={0} style={{ width: "100%", boxSizing: "border-box", marginBottom: 6 }} placeholder="Amount..." />
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 6 }}>
            <button onClick={() => { bankOp("deposit", bankAmt); setBankAmt(0); }}>Deposit</button>
            <button onClick={() => { bankOp("withdraw", bankAmt); setBankAmt(0); }}>Withdraw</button>
          </div>
        </div>
        <button onClick={() => bankOp("interest")} style={{ width: "100%" }}>Collect 5% Interest</button>
      </div>
    );
  }

  // ── GAMBLE SCREEN ──
  if (scene === "gamble") {
    const [localBet, setLocalBet] = useState(10);
    const [flipGuess, setFlipGuess] = useState("H");
    const [luckyNum, setLuckyNum] = useState(3);
    return (
      <div style={{ padding: "0.75rem" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 16 }}>
          <button onClick={() => setScene("town")} style={{ padding: "4px 10px", fontSize: 12 }}>← Back</button>
          <h2 style={{ fontSize: 16, margin: 0 }}>Gambling Den</h2>
          <span style={{ marginLeft: "auto", fontSize: 13, color: "var(--color-text-secondary)" }}>💰 {hero.gold}g</span>
        </div>
        <div style={{ marginBottom: 12 }}>
          <label style={{ fontSize: 12, color: "var(--color-text-secondary)" }}>Bet amount</label>
          <input type="number" value={localBet} onChange={e => setLocalBet(Math.max(1, parseInt(e.target.value) || 0))} style={{ width: "100%", boxSizing: "border-box", marginTop: 4 }} min={1} max={hero.gold} />
        </div>
        <div style={{ display: "grid", gap: 8 }}>
          <div style={{ border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-md)", padding: "10px 12px" }}>
            <div style={{ fontSize: 13, fontWeight: 500, marginBottom: 6 }}>Coin Flip (50/50, win 2×)</div>
            <div style={{ display: "flex", gap: 6 }}>
              <button onClick={() => setFlipGuess("H")} style={{ padding: "4px 12px", background: flipGuess === "H" ? "var(--color-background-info)" : "var(--color-background-primary)" }}>Heads</button>
              <button onClick={() => setFlipGuess("T")} style={{ padding: "4px 12px", background: flipGuess === "T" ? "var(--color-background-info)" : "var(--color-background-primary)" }}>Tails</button>
              <button onClick={() => doGamble("flip", localBet, flipGuess)} disabled={hero.gold < localBet} style={{ marginLeft: "auto", padding: "4px 12px" }}>Bet {localBet}g</button>
            </div>
          </div>
          <div style={{ border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-md)", padding: "10px 12px" }}>
            <div style={{ fontSize: 13, fontWeight: 500, marginBottom: 6 }}>High Roll (roll 4+, win 2.5×)</div>
            <button onClick={() => doGamble("highroll", localBet, null)} disabled={hero.gold < localBet} style={{ padding: "6px 14px" }}>Bet {localBet}g</button>
          </div>
          <div style={{ border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-md)", padding: "10px 12px" }}>
            <div style={{ fontSize: 13, fontWeight: 500, marginBottom: 6 }}>Lucky Number (pick 1-6, win 5×)</div>
            <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
              {[1, 2, 3, 4, 5, 6].map(n => <button key={n} onClick={() => setLuckyNum(n)} style={{ padding: "4px 10px", background: luckyNum === n ? "var(--color-background-info)" : "var(--color-background-primary)" }}>{n}</button>)}
              <button onClick={() => doGamble("lucky", localBet, luckyNum)} disabled={hero.gold < localBet} style={{ padding: "4px 12px" }}>Bet {localBet}g</button>
            </div>
          </div>
          <div style={{ border: "0.5px solid var(--color-border-tertiary)", borderRadius: "var(--border-radius-md)", padding: "10px 12px" }}>
            <div style={{ fontSize: 13, fontWeight: 500, marginBottom: 6 }}>Double Down (40% win 3×)</div>
            <button onClick={() => doGamble("double", localBet, null)} disabled={hero.gold < localBet} style={{ padding: "6px 14px" }}>Bet {localBet}g</button>
          </div>
        </div>
      </div>
    );
  }

  // ── STATS SCREEN ──
  if (showStats) return (
    <div style={{ padding: "0.75rem" }}>
      <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 12 }}>
        <button onClick={() => setShowStats(false)} style={{ padding: "4px 10px", fontSize: 12 }}>← Back</button>
        <h2 style={{ fontSize: 16, margin: 0 }}>Hero Stats</h2>
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginBottom: 12 }}>
        {[["Level", hero.level], ["Class", hero.cls], ["XP", `${hero.xp}/${hero.xpNext}`], ["Talent pts", hero.talentPoints], ["ATK", heroAtk(hero)], ["DEF", heroDef(hero)], ["HP", `${hero.hp}/${hero.maxHp}`], ["MP", `${hero.mp}/${hero.maxMp}`], ["Kills", hero.kills], ["Bosses", hero.bossKills], ["Gold", hero.gold], ["Bank", hero.bank]].map(([k, v]) => (
          <div key={k} style={{ background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)", padding: "8px 10px" }}>
            <div style={{ fontSize: 11, color: "var(--color-text-secondary)" }}>{k}</div>
            <div style={{ fontSize: 15, fontWeight: 500 }}>{v}</div>
          </div>
        ))}
      </div>
      <div style={{ marginBottom: 10 }}>
        <div style={{ fontSize: 12, fontWeight: 500, color: "var(--color-text-secondary)", marginBottom: 6 }}>Equipment</div>
        {[["⚔️ Weapon", hero.weapon.name, `+${hero.weapon.atk} ATK`], ["🛡️ Armor", hero.armor.name, `+${hero.armor.def} DEF`], ["💍 Accessory", hero.accessory.name, hero.accessory.desc]].map(([icon, name, stat]) => (
          <div key={icon} style={{ display: "flex", justifyContent: "space-between", padding: "6px 0", borderBottom: "0.5px solid var(--color-border-tertiary)", fontSize: 13 }}>
            <span>{icon} {name}</span><span style={{ color: "var(--color-text-secondary)" }}>{stat}</span>
          </div>
        ))}
      </div>
      {hero.companion && (
        <div style={{ padding: "8px 10px", background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)", fontSize: 13, marginBottom: 10 }}>
          🤝 {hero.companion.emoji} {hero.companion.name}
        </div>
      )}
      {Object.keys(hero.talents).length > 0 && (
        <div>
          <div style={{ fontSize: 12, fontWeight: 500, color: "var(--color-text-secondary)", marginBottom: 6 }}>Talents</div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 4 }}>
            {Object.keys(hero.talents).map(t => (
              <span key={t} style={{ fontSize: 11, padding: "2px 8px", background: "var(--color-background-info)", color: "var(--color-text-info)", borderRadius: 10 }}>{t}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );

  // ── TOWN (main hub) ──
  const isBoss = [5, 10, 15, 20, 25, 30, 36, 40].includes(floor);
  return (
    <div style={{ padding: "0.75rem" }}>
      {notification && (
        <div style={{ marginBottom: 8, padding: "6px 12px", background: notification.type === "success" ? "var(--color-background-success)" : notification.type === "danger" ? "var(--color-background-danger)" : "var(--color-background-info)", color: notification.type === "success" ? "var(--color-text-success)" : notification.type === "danger" ? "var(--color-text-danger)" : "var(--color-text-info)", borderRadius: "var(--border-radius-md)", fontSize: 13, border: "0.5px solid", borderColor: notification.type === "success" ? "var(--color-border-success)" : notification.type === "danger" ? "var(--color-border-danger)" : "var(--color-border-info)" }}>
          {notification.msg}
        </div>
      )}

      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 10 }}>
        <div style={{ flex: 1 }}>
          <div style={{ fontSize: 14, fontWeight: 500 }}>Floor {floor}/40 {isBoss ? "⚠️ Boss!" : ""}</div>
          <div style={{ fontSize: 12, color: "var(--color-text-secondary)" }}>{hero.name} · {hero.cls} · Lv.{hero.level}</div>
        </div>
        <div style={{ fontSize: 12, color: "var(--color-text-secondary)", textAlign: "right" }}>
          <div>💰 {hero.gold}g</div>
          <div>🧪×{hero.potions} 💊×{hero.elixirs}</div>
        </div>
        <button onClick={() => setShowStats(true)} style={{ padding: "4px 8px", fontSize: 11 }}>Stats</button>
      </div>

      {/* HP / MP */}
      <div style={{ marginBottom: 12 }}>
        <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, color: "var(--color-text-secondary)", marginBottom: 3 }}>
          <span>❤️ {hero.hp}/{hero.maxHp}</span><span>⚔️ {heroAtk(hero)} / 🛡️ {heroDef(hero)}</span>
        </div>
        <HpBar cur={hero.hp} max={hero.maxHp} height={10} />
        <div style={{ marginTop: 4 }}>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, color: "var(--color-text-secondary)", marginBottom: 2 }}>
            <span>💎 {hero.mp}/{hero.maxMp} MP</span><span>XP: {hero.xp}/{hero.xpNext}</span>
          </div>
          <MpBar cur={hero.mp} max={hero.maxMp} />
        </div>
        <StatusBadges statuses={hero.statuses} />
      </div>

      {/* Boss warning */}
      {isBoss && (
        <div style={{ padding: "10px 12px", background: "var(--color-background-danger)", border: "0.5px solid var(--color-border-danger)", borderRadius: "var(--border-radius-md)", marginBottom: 10, fontSize: 13, color: "var(--color-text-danger)" }}>
          ⚠️ Boss floor! {BOSSES[floor]?.emoji} {BOSSES[floor]?.name} awaits. Prepare before entering!
        </div>
      )}

      {/* Actions */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 6, marginBottom: 8 }}>
        <button onClick={() => startBattle(isBoss ? "boss" : "normal")} style={{ padding: "12px 8px", fontWeight: 500, background: isBoss ? "var(--color-background-danger)" : undefined, color: isBoss ? "var(--color-text-danger)" : undefined, border: isBoss ? "0.5px solid var(--color-border-danger)" : undefined }}>
          {isBoss ? `⚔️ Face ${BOSSES[floor]?.name}` : "⚔️ Explore & Fight"}
        </button>
        <button onClick={() => startBattle("elite")} style={{ padding: "12px 8px" }}>⭐ Elite Battle</button>
        <button onClick={() => setScene("shop")} style={{ padding: "10px 8px" }}>🏪 Shop</button>
        <button onClick={() => setScene("inn")} style={{ padding: "10px 8px" }}>🏨 Inn</button>
        <button onClick={() => setScene("talent")} style={{ padding: "10px 8px" }}>🧠 Talents {hero.talentPoints > 0 ? `(${hero.talentPoints}!)` : ""}</button>
        <button onClick={() => setScene("companion")} style={{ padding: "10px 8px" }}>🤝 Tavern</button>
        <button onClick={() => setScene("bank")} style={{ padding: "10px 8px" }}>🏦 Bank</button>
        <button onClick={() => setScene("gamble")} style={{ padding: "10px 8px" }}>🎲 Gamble</button>
      </div>

      {/* Skills quick view */}
      {hero.skills.length > 0 && (
        <div style={{ background: "var(--color-background-secondary)", borderRadius: "var(--border-radius-md)", padding: "8px 10px" }}>
          <div style={{ fontSize: 12, color: "var(--color-text-secondary)", marginBottom: 4 }}>Skills ({hero.skills.length})</div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 4 }}>
            {hero.skills.map(s => (
              <span key={s.name} style={{ fontSize: 11, padding: "2px 8px", background: "var(--color-background-primary)", border: "0.5px solid var(--color-border-tertiary)", borderRadius: 10, color: hero.mp >= s.mp ? "var(--color-text-primary)" : "var(--color-text-tertiary)" }}>
                {s.name} ({s.mp}mp)
              </span>
            ))}
          </div>
        </div>
      )}

      {hero.companion && (
        <div style={{ marginTop: 8, padding: "6px 10px", background: "var(--color-background-success)", border: "0.5px solid var(--color-border-success)", borderRadius: "var(--border-radius-md)", fontSize: 12, color: "var(--color-text-success)" }}>
          🤝 {hero.companion.emoji} {hero.companion.name} · {hero.companion.ability}
        </div>
      )}
    </div>
  );
}

// ── ROOT ─────────────────────────────────────────────────────────────
export default function DragonQuest() {
  const [hero, setHero] = useState(null);
  if (!hero) return <CharSelect onStart={(name, cls) => setHero(makeHero(name, cls))} />;
  return <Game heroInit={hero} />;
}