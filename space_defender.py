"""
╔══════════════════════════════════════════════════════════════════╗
║        🚀  SPACE DEFENDER  —  Enhanced Edition  🚀               ║
╠══════════════════════════════════════════════════════════════════╣
║  ← → / A D   Move ship      SPACE   Shoot      P   Pause        ║
╚══════════════════════════════════════════════════════════════════╝
  Features: Parallax stars · Power-ups · Enemy bullets · Boss fights
            Combo system · Shield · Pause · High-score save
"""

import turtle, random, math, time

# ═══════════════════════════════════════════════════════════════
#  SCREEN
# ═══════════════════════════════════════════════════════════════
SCR = turtle.Screen()
SCR.title("🚀 Space Defender  ·  Enhanced Edition")
SCR.bgcolor("#050514")
SCR.setup(width=860, height=720)
SCR.tracer(0)

W, H   = 860, 720
HW, HH = W // 2, H // 2

# ═══════════════════════════════════════════════════════════════
#  CONSTANTS
# ═══════════════════════════════════════════════════════════════
PLAYER_SPEED    = 20
BASE_SHOOT_CD   = 9
INVINCIBLE_DUR  = 72
COMBO_TIMEOUT   = 100
BOSS_EVERY      = 5
MAX_SPARKS      = 40
MAX_EBULLETS    = 12
HS_FILE         = "hs.txt"
PLAYER_Y        = -HH + 82

# ═══════════════════════════════════════════════════════════════
#  MUTABLE GAME STATE  (reset by init_game)
# ═══════════════════════════════════════════════════════════════
score = lives = level = frame = 0
shoot_cd = spawn_cd = 0
running = paused = False
combo = combo_timer = max_combo = 0
invincible = shield_hp = 0
rapid_timer = spread_timer = 0
boss_alive = False
boss       = None
boss_hp    = boss_dir = 0
flash_timer = high_score = 0
hud_dirty   = True
prev_boss_hp = -1

bullets   : list = []
e_bullets : list = []
enemies   : list = []
powerups  : list = []
sparks    : list = []
near_stars: list = []

keys = {"left": False, "right": False, "fire": False}

# ═══════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════
def mkturt(shape="circle", color="white",
           sx=1.0, sy=1.0, x=0, y=0, hdg=90, vis=True):
    t = turtle.Turtle()
    t.shape(shape); t.color(color); t.shapesize(sx, sy)
    t.penup(); t.speed(0); t.setheading(hdg); t.goto(x, y)
    if not vis: t.hideturtle()
    return t

def sq_dist(a, b):
    return (a.xcor()-b.xcor())**2 + (a.ycor()-b.ycor())**2

def load_hs():
    try:
        with open(HS_FILE) as f: return int(f.read().strip())
    except: return 0

def save_hs(s):
    try:
        with open(HS_FILE, "w") as f: f.write(str(s))
    except: pass

# ═══════════════════════════════════════════════════════════════
#  STATIC BACKGROUND  (grid + deep stars + nebula glows)
# ═══════════════════════════════════════════════════════════════
_bg = mkturt(vis=False)

def draw_background():
    # Subtle nebula clouds
    for (x, y, r, c) in [(160, 100, 120, "#0d0830"), (-200, -80, 100, "#080d20"),
                          (30, -160, 90, "#0a0820"), (-100, 180, 110, "#080f28")]:
        _bg.goto(x, y); _bg.dot(r * 2, c)

    # Faint grid
    _bg.color("#0b0b2a"); _bg.width(1)
    for x in range(-HW, HW + 1, 70):
        _bg.goto(x, -HH+55); _bg.pendown()
        _bg.goto(x,  HH-5);  _bg.penup()
    for y in range(-HH+55, HH - 4, 70):
        _bg.goto(-HW, y); _bg.pendown()
        _bg.goto( HW, y); _bg.penup()

    # Deep (static) stars
    random.seed(27182)
    for _ in range(115):
        x = random.randint(-HW+5, HW-5)
        y = random.randint(-HH+60, HH-5)
        c = random.choice(["#252564","#30307a","#1d1d50","#383890"])
        _bg.goto(x, y); _bg.dot(random.choice([1, 1, 2]), c)

    # Arena border
    _bg.color("#1a2855"); _bg.width(2)
    corners = [(-HW+10, HH-52),(HW-10, HH-52),(HW-10,-HH+10),(-HW+10,-HH+10)]
    _bg.goto(corners[0]); _bg.pendown()
    for pt in corners[1:]: _bg.goto(pt)
    _bg.goto(corners[0]); _bg.penup()

draw_background()

# ═══════════════════════════════════════════════════════════════
#  SCROLLING PARALLAX STARS
# ═══════════════════════════════════════════════════════════════
def make_near_stars():
    for _ in range(26):
        sz = random.choice([0.17, 0.22, 0.28])
        t  = mkturt("circle",
                    random.choice(["white","#aaccff","#ffeecc","#aaffbb"]),
                    sz, sz,
                    random.randint(-HW+5, HW-5),
                    random.randint(-HH+58, HH-5))
        t._speed = random.uniform(1.0, 3.0)
        near_stars.append(t)

def scroll_stars():
    for s in near_stars:
        ny = s.ycor() - s._speed
        if ny < -HH+52:
            s.goto(random.randint(-HW+5, HW-5), HH-8)
        else:
            s.sety(ny)

# ═══════════════════════════════════════════════════════════════
#  HUD PENS  (separate pens so they don't stomp each other)
# ═══════════════════════════════════════════════════════════════
_hud      = mkturt(vis=False)   # score / level / lives / powerups
_boss_bar = mkturt(vis=False)   # boss health bar
_combo_p  = mkturt(vis=False)   # combo counter
_flash_p  = mkturt(vis=False)   # flash messages

def refresh_hud():
    global hud_dirty
    _hud.clear()
    _hud.color("#1e3060"); _hud.width(2)
    _hud.goto(-HW+12, HH-50); _hud.pendown()
    _hud.goto( HW-12, HH-50); _hud.penup(); _hud.width(1)

    _hud.color("#00e5cc"); _hud.goto(-HW+20, HH-42)
    _hud.write(f"SCORE  {score:07d}", font=("Courier", 13, "bold"))

    _hud.color("#ffd700"); _hud.goto(-82, HH-42)
    _hud.write(f"LEVEL  {level:02d}", font=("Courier", 13, "bold"))

    _hud.color("#ff4466"); _hud.goto(HW-185, HH-42)
    _hud.write(f"LIVES  {'♥ '*lives}", font=("Courier", 13, "bold"))

    pw_x = -HW + 20
    if rapid_timer > 0:
        _hud.color("#ffff00"); _hud.goto(pw_x, HH-66)
        _hud.write("⚡ RAPID", font=("Courier", 9, "bold")); pw_x += 105
    if spread_timer > 0:
        _hud.color("#00ff88"); _hud.goto(pw_x, HH-66)
        _hud.write("✦ SPREAD", font=("Courier", 9, "bold")); pw_x += 115
    if shield_hp > 0:
        _hud.color("#00aaff"); _hud.goto(pw_x, HH-66)
        _hud.write(f"🛡 {'▮'*shield_hp}", font=("Courier", 9, "bold"))

    _hud.color("#444466"); _hud.goto(-HW+18, -HH+14)
    _hud.write(f"BEST  {high_score:07d}", font=("Courier", 9, "normal"))
    hud_dirty = False

def draw_boss_bar():
    global prev_boss_hp
    if not boss_alive:
        if prev_boss_hp != -1:
            _boss_bar.clear(); prev_boss_hp = -1
        return
    if boss_hp == prev_boss_hp: return
    prev_boss_hp = boss_hp
    _boss_bar.clear()
    total  = 20 + level * 5
    filled = max(0, int(30 * boss_hp / total))
    _boss_bar.color("#ff0066"); _boss_bar.goto(-165, 68)
    _boss_bar.write(
        f"BOSS  {'█'*filled}{'░'*(30-filled)}",
        font=("Courier", 10, "bold"))

def update_combo_display():
    _combo_p.clear()
    if combo < 3: return
    col = next(c for t, c in [(20,"#ff0088"),(12,"#ff3300"),
               (8,"#ff6600"),(5,"#ffaa00"),(3,"#ffff88")] if combo >= t)
    _combo_p.color(col); _combo_p.goto(HW-138, HH-80)
    _combo_p.write(f"x{combo} COMBO!", font=("Courier", 11, "bold"))

def flash_message(msg, col="#ffffff", dur=60):
    global flash_timer
    flash_timer = dur
    _flash_p.clear(); _flash_p.color(col)
    _flash_p.goto(0, 28)
    _flash_p.write(msg, align="center", font=("Courier", 22, "bold"))

def tick_flash():
    global flash_timer
    if flash_timer > 0:
        flash_timer -= 1
        if flash_timer == 0: _flash_p.clear()

# ═══════════════════════════════════════════════════════════════
#  PLAYER SHIP
# ═══════════════════════════════════════════════════════════════
player      = mkturt("triangle", "#00e5ff", 1.6, 1.1, 0, PLAYER_Y, 90)
_glow       = mkturt("circle", "#0044ff", 0.44, 0.44, 0, PLAYER_Y - 18)
_glow2      = mkturt("circle", "#001e88", 0.27, 0.27, 0, PLAYER_Y - 26)
_shield_vis = mkturt("circle", "#00aaff", 1.88, 1.88, 0, PLAYER_Y, 90, False)

def update_player_vis():
    px, py = player.xcor(), player.ycor()
    _glow.goto(px, py - 18); _glow2.goto(px, py - 26)
    player.color("#ff4466" if invincible > 0 and (invincible//5)%2 == 0
                 else "#00e5ff")
    if shield_hp > 0:
        _shield_vis.showturtle(); _shield_vis.goto(px, py)
        _shield_vis.color(["#00aaff","#0088cc","#006699"][3 - shield_hp])
    else:
        _shield_vis.hideturtle()
    _glow.color("#0055ff" if frame % 4 < 2 else "#003399")

# ═══════════════════════════════════════════════════════════════
#  ENEMIES
# ═══════════════════════════════════════════════════════════════
ENEMY_DEFS = [
    dict(shape="circle",   color="#ff3355", sz=1.0,  hp=1, pts=10, shoots=False),
    dict(shape="square",   color="#ff7700", sz=0.9,  hp=2, pts=25, shoots=True ),
    dict(shape="triangle", color="#bb33ff", sz=1.15, hp=1, pts=15, shoots=False),
    dict(shape="circle",   color="#ff55aa", sz=0.65, hp=1, pts=8,  shoots=False),
    dict(shape="square",   color="#00ddff", sz=1.2,  hp=3, pts=40, shoots=True ),
]

def spawn_enemy():
    if boss_alive: return
    d = random.choice(ENEMY_DEFS)
    e = mkturt(d["shape"], d["color"], d["sz"], d["sz"],
               random.randint(-HW+36, HW-36), HH - 60, 270)
    e._hp       = d["hp"]
    e._pts      = d["pts"]
    e._shoots   = d["shoots"]
    e._vy       = 1.6 + level * 0.42 + random.uniform(0, 0.5)
    e._vx       = random.uniform(-0.9, 0.9)
    e._shoot_cd = random.randint(50, 160)
    enemies.append(e)

# ═══════════════════════════════════════════════════════════════
#  BOSS
# ═══════════════════════════════════════════════════════════════
def spawn_boss():
    global boss, boss_alive, boss_hp, boss_dir
    boss_hp = 20 + level * 5; boss_dir = 1
    boss = mkturt("circle", "#ff0066", 3.7, 3.7, 0, HH - 80, 270)
    boss_alive = True
    flash_message("⚠  BOSS  INCOMING  ⚠", "#ff0066", 100)
    draw_boss_bar()

def tick_boss():
    global boss_alive, boss_dir, boss_hp, score, hud_dirty
    if not boss_alive or boss is None: return
    boss.setx(boss.xcor() + boss_dir * (2.2 + level * 0.25))
    if boss.ycor() > 110: boss.sety(boss.ycor() - 1.0)
    if abs(boss.xcor()) > HW - 58: boss_dir *= -1
    # Spread bullets
    if frame % 22 == 0 and len(e_bullets) < MAX_EBULLETS:
        for ang_off in [-20, 0, 20]:
            if len(e_bullets) >= MAX_EBULLETS: break
            b = mkturt("circle","#ff4400", 0.4, 0.4,
                       boss.xcor(), boss.ycor() - 38, 270)
            b._angle = math.radians(270 + ang_off)
            e_bullets.append(b)
    # Bullet collision
    for b in bullets[:]:
        if sq_dist(b, boss) < 2916:
            b.hideturtle(); bullets.remove(b)
            boss_hp -= 1
            boss.color("#ffffff" if boss_hp % 2 == 0 else "#ff0066")
            draw_boss_bar()
            if boss_hp <= 0:
                for ox, oy in [(0,0),(-45,28),(45,-22),(0,-38),(-22,44)]:
                    blast(boss.xcor()+ox, boss.ycor()+oy, n=14)
                boss.hideturtle(); boss_alive = False
                score += (220 + level * 55) * max(1, combo // 2)
                flash_message(f"BOSS DESTROYED! +{220+level*55}", "#ffd700", 100)
                hud_dirty = True
            break
    if boss_alive and sq_dist(player, boss) < 4100:
        handle_player_hit()

# ═══════════════════════════════════════════════════════════════
#  POWER-UPS
# ═══════════════════════════════════════════════════════════════
PUPS = [
    dict(color="#ffff00", kind="rapid"),
    dict(color="#00ff88", kind="spread"),
    dict(color="#00aaff", kind="shield"),
    dict(color="#ff6600", kind="nuke"),
]

def maybe_drop(x, y):
    if random.random() > 0.18: return
    d = random.choice(PUPS)
    p = mkturt("circle", d["color"], 0.72, 0.72, x, y)
    p._kind = d["kind"]; p._vy = 1.6
    powerups.append(p)

def activate(p):
    global rapid_timer, spread_timer, shield_hp, score, hud_dirty
    k = p._kind
    if   k == "rapid":  rapid_timer  = 320; flash_message("⚡ RAPID FIRE!",  "#ffff00", 60)
    elif k == "spread": spread_timer = 320; flash_message("✦ SPREAD SHOT!", "#00ff88", 60)
    elif k == "shield":
        shield_hp = min(shield_hp + 3, 3); flash_message("🛡 SHIELD UP!",  "#00aaff", 60)
    elif k == "nuke":
        bonus = 50 * len(enemies); score += bonus
        flash_message(f"💥 NUKE!  +{bonus}", "#ff6600", 60)
        for e in enemies[:]:
            blast(e.xcor(), e.ycor(), n=6); e.hideturtle()
        enemies.clear()
    hud_dirty = True
    p.hideturtle(); powerups.remove(p)

def tick_powerups():
    for p in powerups[:]:
        # Gentle pulse (grow/shrink)
        sz = 0.72 + 0.18 * math.sin(frame * 0.15)
        p.shapesize(sz, sz)
        p.sety(p.ycor() - p._vy)
        if p.ycor() < -HH + 20:
            p.hideturtle(); powerups.remove(p); continue
        if sq_dist(player, p) < 625: activate(p)

# ═══════════════════════════════════════════════════════════════
#  SPARK EXPLOSIONS  (gravity-affected)
# ═══════════════════════════════════════════════════════════════
_SPARK_COLS = ["#ff6600","#ffaa00","#ffff44","#ff3300","#ffffff","#ffccaa","#ff88cc"]

def blast(x, y, n=9):
    for _ in range(min(n, MAX_SPARKS - len(sparks))):
        s = mkturt("circle", random.choice(_SPARK_COLS), 0.28, 0.28, x, y)
        angle  = random.uniform(0, 2 * math.pi)
        speed  = random.uniform(2.5, 7.5)
        s._vx  = math.cos(angle) * speed
        s._vy  = math.sin(angle) * speed
        s._life = random.randint(6, 18)
        sparks.append(s)

def tick_sparks():
    for s in sparks[:]:
        s.setx(s.xcor() + s._vx)
        s.sety(s.ycor() + s._vy)
        s._vy -= 0.22          # gravity
        s._life -= 1
        if s._life <= 0:
            s.hideturtle(); sparks.remove(s)

# ═══════════════════════════════════════════════════════════════
#  PLAYER HIT
# ═══════════════════════════════════════════════════════════════
def handle_player_hit():
    global lives, shield_hp, invincible, running, hud_dirty
    if invincible > 0: return
    if shield_hp > 0:
        shield_hp -= 1; invincible = 30
        flash_message("SHIELD HIT!", "#00aaff", 30)
    else:
        blast(player.xcor(), player.ycor(), n=14)
        lives -= 1; invincible = INVINCIBLE_DUR
        if lives > 0: flash_message("HIT!", "#ff2244", 40)
        else: running = False
    hud_dirty = True

# ═══════════════════════════════════════════════════════════════
#  KEYBOARD
# ═══════════════════════════════════════════════════════════════
def kp(k): keys[k] = True
def kr(k): keys[k] = False

def toggle_pause():
    global paused
    paused = not paused
    if paused:
        _flash_p.clear(); _flash_p.color("#ffd700")
        _flash_p.goto(0, 28)
        _flash_p.write("—  PAUSED  —", align="center",
                       font=("Courier", 30, "bold"))
    else:
        _flash_p.clear()

SCR.listen()
for (key, name) in [("Left","left"),("a","left"),
                    ("Right","right"),("d","right"),("space","fire")]:
    SCR.onkeypress(   (lambda k=name: kp(k)), key)
    SCR.onkeyrelease( (lambda k=name: kr(k)), key)
SCR.onkey(toggle_pause, "p")

# ═══════════════════════════════════════════════════════════════
#  TITLE SCREEN
# ═══════════════════════════════════════════════════════════════
def title_screen():
    hs = load_hs()
    t  = mkturt(vis=False)
    t.width(3)
    for r, c in [(130,"#0a1a3a"),(108,"#0d2255"),(86,"#1033aa")]:
        t.goto(0, 85); t.pendown(); t.color(c); t.circle(r); t.penup()
    t.width(1)
    t.color("#00e5ff"); t.goto(0, 110)
    t.write("SPACE", align="center", font=("Courier", 52, "bold"))
    t.color("#ffd700"); t.goto(0, 54)
    t.write("DEFENDER", align="center", font=("Courier", 44, "bold"))
    t.color("#8888bb"); t.goto(0, 18)
    t.write("Enhanced  Edition", align="center", font=("Courier", 14, "italic"))
    t.color("#445577"); t.goto(0, -18)
    t.write("──────────────────────────────────────────",
            align="center", font=("Courier", 9, "normal"))
    for (k, act, col), y in zip(
        [("← → / A D","Move ship","white"),("SPACE","Shoot","white"),
         ("P","Pause / Resume","#9999cc")], [-42,-68,-94]):
        t.color(col); t.goto(-220, y)
        t.write(f"{k:<15} ▸  {act}", font=("Courier", 12, "normal"))
    t.color("#887799"); t.goto(0, -128)
    t.write("Power-ups:  ⚡ Rapid   ✦ Spread   🛡 Shield   💥 Nuke",
            align="center", font=("Courier", 10, "normal"))
    t.color("#555588"); t.goto(0, -150)
    t.write("Enemies shoot back  ·  Boss every 5 levels  ·  Combos give bonus points",
            align="center", font=("Courier", 9, "normal"))
    if hs:
        t.color("#ffd700"); t.goto(0, -178)
        t.write(f"Best Score:  {hs:07d}",
                align="center", font=("Courier", 11, "bold"))
    prompt  = mkturt(vis=False)
    started = [False]
    def start(): started[0] = True
    SCR.onkey(start, "space"); SCR.listen()
    pulse = 0
    while not started[0]:
        pulse += 0.1
        b = int(128 + 127 * math.sin(pulse))
        prompt.clear(); prompt.color(f"#{b:02x}ff{b:02x}")
        prompt.goto(0, -218)
        prompt.write("▶▶  Press  SPACE  to  Launch  ◀◀",
                     align="center", font=("Courier", 15, "bold"))
        SCR.update(); time.sleep(0.04)
    SCR.onkey(None, "space")
    t.clear(); prompt.clear(); prompt.hideturtle(); t.hideturtle()
    SCR.onkeypress(   (lambda: kp("fire")), "space")
    SCR.onkeyrelease( (lambda: kr("fire")), "space")

# ═══════════════════════════════════════════════════════════════
#  GAME OVER SCREEN
# ═══════════════════════════════════════════════════════════════
def show_game_over():
    new_hs = score > high_score
    if new_hs: save_hs(score)
    t = mkturt(vis=False)
    t.color("#ff1144"); t.goto(0, 115)
    t.write("G A M E   O V E R", align="center",
            font=("Courier", 42, "bold"))
    if new_hs:
        t.color("#ffd700"); t.goto(0, 64)
        t.write("✦  NEW  HIGH  SCORE  ✦", align="center",
                font=("Courier", 18, "bold"))
    t.color("white"); t.goto(0, 16)
    t.write(
        f"Score {score:07d}  ·  Level {level}  ·  Best Combo x{max_combo}",
        align="center", font=("Courier", 13, "normal"))
    stars = min(score // 700, 5)
    t.color("#ffd700"); t.goto(0, -30)
    t.write("★ "*stars + "☆ "*(5-stars),
            align="center", font=("Courier", 24, "normal"))
    t.color("#aaffaa"); t.goto(0, -92)
    t.write("Press  Escape  to  quit",
            align="center", font=("Courier", 12, "normal"))
    SCR.onkey(SCR.bye, "Escape"); SCR.listen()

# ═══════════════════════════════════════════════════════════════
#  INIT GAME
# ═══════════════════════════════════════════════════════════════
def init_game():
    global score, lives, level, frame, shoot_cd, spawn_cd, running, paused
    global combo, combo_timer, max_combo, invincible, shield_hp
    global rapid_timer, spread_timer
    global boss_alive, boss, boss_hp, boss_dir
    global flash_timer, high_score, hud_dirty, prev_boss_hp

    high_score  = load_hs()
    score = 0; lives = 3; level = 1
    frame = 0; shoot_cd = 0; spawn_cd = 0; paused = False
    combo = 0; combo_timer = 0; max_combo = 0
    invincible = 0; shield_hp = 0
    rapid_timer = 0; spread_timer = 0
    boss_alive = False; boss = None; boss_hp = 0; boss_dir = 1
    flash_timer = 0; hud_dirty = True; prev_boss_hp = -1; running = True

    for lst in (bullets, e_bullets, enemies, powerups, sparks):
        for obj in lst: obj.hideturtle()
        lst.clear()

    for pen in (_hud, _boss_bar, _combo_p, _flash_p): pen.clear()
    player.goto(0, PLAYER_Y); player.showturtle()
    _shield_vis.hideturtle()
    refresh_hud()

# ═══════════════════════════════════════════════════════════════
#  MAIN GAME LOOP
# ═══════════════════════════════════════════════════════════════
def run_game():
    global score, lives, level, frame, shoot_cd, spawn_cd, running
    global combo, combo_timer, max_combo, invincible
    global rapid_timer, spread_timer, boss_alive, hud_dirty

    SPAWN_BASE = 44
    prev_level = 1

    while running:
        SCR.update()
        time.sleep(0.016)
        frame += 1
        if paused: continue

        # ── Countdown timers ─────────────────────────────────────────────
        if invincible > 0: invincible -= 1
        if rapid_timer  > 0:
            rapid_timer  -= 1
            if rapid_timer == 0: hud_dirty = True
        if spread_timer > 0:
            spread_timer -= 1
            if spread_timer == 0: hud_dirty = True
        if combo_timer > 0:
            combo_timer -= 1
            if combo_timer == 0: combo = 0; _combo_p.clear()
        tick_flash()

        # ── Level progression ─────────────────────────────────────────────
        new_level = score // 350 + 1
        if new_level > level:
            level = new_level
            flash_message(f"LEVEL  {level}  !", "#ffd700", 70)
            hud_dirty = True

        # Boss check — once when we first arrive at a boss level
        if level % BOSS_EVERY == 0 and not boss_alive and level != prev_level:
            spawn_boss()
        prev_level = level

        # ── HUD refresh (only when dirty) ─────────────────────────────────
        if hud_dirty: refresh_hud()
        draw_boss_bar()

        # ── Player movement ───────────────────────────────────────────────
        px = player.xcor()
        if keys["left"]  and px > -HW + 36: player.setx(px - PLAYER_SPEED)
        if keys["right"] and px <  HW - 36: player.setx(px + PLAYER_SPEED)
        update_player_vis()

        # ── Shoot ─────────────────────────────────────────────────────────
        shoot_cd = max(0, shoot_cd - 1)
        eff_cd   = max(3, BASE_SHOOT_CD - (4 if rapid_timer > 0 else 0))
        if keys["fire"] and shoot_cd == 0:
            px_, py_ = player.xcor(), player.ycor() + 22
            b = mkturt("circle", "#ffff44", 0.32, 0.32, px_, py_, 90)
            b._angle = math.pi / 2
            bullets.append(b)
            if spread_timer > 0:
                for ang in [70, 110]:
                    b2 = mkturt("circle","#00ff88", 0.28, 0.28, px_, py_, ang)
                    b2._angle = math.radians(ang)
                    bullets.append(b2)
            shoot_cd = eff_cd

        # ── Move player bullets ───────────────────────────────────────────
        for b in bullets[:]:
            b.setx(b.xcor() + math.cos(b._angle) * 20)
            b.sety(b.ycor() + math.sin(b._angle) * 20)
            if b.ycor() > HH - 55 or abs(b.xcor()) > HW:
                b.hideturtle(); bullets.remove(b)

        # ── Move enemy bullets ────────────────────────────────────────────
        for eb in e_bullets[:]:
            eb.setx(eb.xcor() + math.cos(eb._angle) * 5.5)
            eb.sety(eb.ycor() + math.sin(eb._angle) * 5.5)
            if eb.ycor() < -HH + 20 or abs(eb.xcor()) > HW:
                eb.hideturtle(); e_bullets.remove(eb); continue
            if sq_dist(player, eb) < 400:
                eb.hideturtle(); e_bullets.remove(eb)
                handle_player_hit()

        # ── Spawn enemies ─────────────────────────────────────────────────
        spawn_cd -= 1
        interval = max(9, SPAWN_BASE - level * 4)
        if spawn_cd <= 0 and not boss_alive:
            spawn_enemy()
            if level >= 4: spawn_enemy()
            if level >= 7: spawn_enemy()
            spawn_cd = interval

        # ── Update enemies ────────────────────────────────────────────────
        for e in enemies[:]:
            e.sety(e.ycor() - e._vy)
            e.setx(e.xcor() + e._vx)
            if abs(e.xcor()) > HW - 22: e._vx *= -1

            # Slipped past the bottom
            if e.ycor() < -HH + 18:
                e.hideturtle(); enemies.remove(e)
                combo = 0; _combo_p.clear()
                lives -= 1; hud_dirty = True
                if lives <= 0: running = False
                continue

            # Enemy fires
            if e._shoots and len(e_bullets) < MAX_EBULLETS:
                e._shoot_cd -= 1
                if e._shoot_cd <= 0:
                    eb = mkturt("circle","#ff5500", 0.38, 0.38,
                                e.xcor(), e.ycor() - 18, 270)
                    eb._angle = math.radians(270)
                    e_bullets.append(eb)
                    e._shoot_cd = random.randint(50, 160)

            # Bullet hits enemy
            hit = False
            for b in bullets[:]:
                if sq_dist(b, e) < 490:
                    b.hideturtle(); bullets.remove(b)
                    e._hp -= 1
                    if e._hp <= 0:
                        blast(e.xcor(), e.ycor(), n=9)
                        maybe_drop(e.xcor(), e.ycor())
                        e.hideturtle(); enemies.remove(e)
                        combo += 1
                        if combo > max_combo: max_combo = combo
                        combo_timer = COMBO_TIMEOUT
                        pts = e._pts * level * max(1, combo // 3)
                        score += pts
                        hud_dirty = True
                        update_combo_display()
                    hit = True; break

            # Player runs into enemy
            if not hit and e in enemies and sq_dist(player, e) < 686:
                blast(e.xcor(), e.ycor(), n=9)
                e.hideturtle(); enemies.remove(e)
                handle_player_hit()

        # ── Boss ──────────────────────────────────────────────────────────
        if boss_alive: tick_boss()

        # ── Power-ups ─────────────────────────────────────────────────────
        tick_powerups()

        # ── Sparks ────────────────────────────────────────────────────────
        tick_sparks()

        # ── Parallax stars ────────────────────────────────────────────────
        scroll_stars()

# ═══════════════════════════════════════════════════════════════
#  LAUNCH
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    make_near_stars()
    title_screen()
    init_game()
    run_game()
    show_game_over()
    SCR.mainloop()