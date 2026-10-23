"""
╔══════════════════════════════════════════════════════════════════╗
║         🏰  DARK  DUNGEON  —  Python 3D Raycasting               ║
╠══════════════════════════════════════════════════════════════════╣
║  W / S       Move forward / back                                 ║
║  A / D       Turn left / right                                   ║
║  Q / E       Strafe left / right                                 ║
║  ←  →        Also turn (arrow keys)                              ║
║  ESC         Quit                                                ║
╠══════════════════════════════════════════════════════════════════╣
║  Collect all 3 gold keys  ·  Find the glowing EXIT portal        ║
║  Avoid red enemies  ·  Grab red health packs to heal             ║
╚══════════════════════════════════════════════════════════════════╝

  HOW IT WORKS:
  Classic Wolfenstein-style raycasting.  For every screen column a
  ray is marched through the map grid (DDA algorithm).  The hit
  distance is used to calculate a wall-strip height and shade.
  Sprites are projected with an inverse camera transform and
  rendered column-by-column against a per-column depth (z) buffer.
"""

import pygame, math, sys, random

pygame.init()
pygame.font.init()
pygame.mouse.set_visible(False)

# ═══════════════════════════════════════════════════════════════
#  SCREEN & RAYCASTING SETUP
# ═══════════════════════════════════════════════════════════════
SW, SH  = 960, 620           # window size
HH      = SH // 2
STRIP   = 2                  # wall-strip pixel width
RAYS    = SW // STRIP        # 480 rays per frame

screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption("🏰  Dark Dungeon  ·  3D Raycasting")
clock  = pygame.time.Clock()

# ── Fonts ──────────────────────────────────────────────────────
F_XL = pygame.font.SysFont("Courier", 62, bold=True)
F_LG = pygame.font.SysFont("Courier", 36, bold=True)
F_MD = pygame.font.SysFont("Courier", 21, bold=True)
F_SM = pygame.font.SysFont("Courier", 14)

# ═══════════════════════════════════════════════════════════════
#  MAP   0=floor  1=stone  2=brick  3=arcane  4=mossy
# ═══════════════════════════════════════════════════════════════
MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,2,2,0,0,2,0,1,0,2,1,1,2,0,1,1,0,0,1],
    [1,0,2,0,0,0,2,0,0,0,1,0,0,2,0,0,1,0,0,1],
    [1,0,2,0,1,1,1,0,2,0,1,0,0,1,0,0,0,0,0,1],
    [1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,3,3,0,0,1],
    [1,1,1,0,1,0,1,1,1,1,1,0,1,1,0,3,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,1,0,1],
    [1,0,2,1,1,1,0,2,0,0,1,0,1,0,1,1,0,1,0,1],
    [1,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,1],
    [1,1,0,1,0,1,0,1,1,2,0,2,1,0,0,0,1,1,0,1],
    [1,0,0,1,0,0,0,0,0,1,0,0,1,0,2,0,0,1,0,1],
    [1,0,1,1,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,1],
    [1,0,0,0,0,0,1,0,2,1,1,0,2,0,0,1,0,1,0,1],
    [1,4,4,4,4,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1],
    [1,0,0,0,4,0,0,0,1,0,0,0,1,1,0,2,0,0,0,1],
    [1,0,1,0,4,0,1,1,1,0,1,0,1,0,0,1,0,1,0,1],
    [1,0,1,1,4,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1],
    [1,0,0,0,0,0,1,0,1,1,1,0,2,1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]
MH, MW = len(MAP), len(MAP[0])

def mat(xi, yi):
    """Return map cell (1 if out of bounds = treat as wall)."""
    if 0 <= xi < MW and 0 <= yi < MH:
        return MAP[yi][xi]
    return 1

# ── Wall face colours ──────────────────────────────────────────
WALL_BASE = {
    1: (90, 85, 100),    # stone — grey-purple
    2: (115, 62, 50),    # brick — terracotta
    3: (48, 54, 122),    # arcane — deep blue
    4: (52, 96, 52),     # mossy — dark green
}

# ═══════════════════════════════════════════════════════════════
#  PRE-RENDERED SURFACES
# ═══════════════════════════════════════════════════════════════

# Sky-to-floor gradient (blit every frame before casting walls)
sky = pygame.Surface((SW, SH))
for y in range(HH + 1):
    t = y / HH
    pygame.draw.line(sky, (int(13*(1-t)), int(9*(1-t)), int(36+15*t)),
                     (0, y), (SW-1, y))
for y in range(HH, SH):
    t = (y - HH) / HH
    pygame.draw.line(sky, (int(28*(1-t*0.55)), int(22*(1-t*0.55)), int(16*(1-t*0.38))),
                     (0, y), (SW-1, y))

# Vignette (radial darkening at screen edges, pre-rendered with rect strokes)
vign = pygame.Surface((SW, SH), pygame.SRCALPHA)
for i in range(90):
    a = max(0, int(210 * (1 - i / 90) ** 2.4))
    if a:
        pygame.draw.rect(vign, (0, 0, 0, a), (i, i, SW - 2*i, SH - 2*i), 1)

# Damage-flash overlay (re-filled each frame when active)
dmg_surf = pygame.Surface((SW, SH), pygame.SRCALPHA)

# ═══════════════════════════════════════════════════════════════
#  PLAYER STATE
# ═══════════════════════════════════════════════════════════════
px,  py   = 1.5,  1.5     # world position
dx,  dy   = 1.0,  0.0     # unit direction vector
plx, ply  = 0.0,  0.66    # camera-plane vector (|plane| = tan(FOV/2))

MOV_SPD   = 0.055
ROT_SPD   = 0.044
COLL_R    = 0.25           # collision radius

health    = 100
keys_held = 0
KEYS_NEED = 3
dmg_flash = 0              # countdown frames for damage flash
hurt_cd   = 0              # frames until next enemy damage tick

# ═══════════════════════════════════════════════════════════════
#  SPRITES   [x, y, kind, alive]
# ═══════════════════════════════════════════════════════════════
sprites = [
    # ── 3 keys (gold)
    [3.5,  3.5,  "key",    True],
    [9.5,  14.5, "key",    True],
    [16.5, 5.5,  "key",    True],
    # ── 2 health packs (red)
    [6.5,  7.5,  "health", True],
    [14.5, 11.5, "health", True],
    # ── 5 enemies (red skull)
    [4.5,  8.5,  "enemy",  True],
    [11.5, 3.5,  "enemy",  True],
    [7.5,  16.5, "enemy",  True],
    [15.5, 15.5, "enemy",  True],
    [3.5,  16.5, "enemy",  True],
    # ── Exit portal (green)
    [18.5, 18.5, "exit",   True],
]
SPR_COL = {
    "key":    (255, 210, 30),
    "health": (220, 50,  50),
    "enemy":  (225, 38,  38),
    "exit":   (48,  255, 105),
}

# Per-column depth buffer, filled during wall pass, read by sprite pass
z_buf = [0.0] * SW

# ═══════════════════════════════════════════════════════════════
#  GAME STATE
# ═══════════════════════════════════════════════════════════════
STATE = "title"    # "title" | "game" | "win" | "lose"
tick  = 0

# ═══════════════════════════════════════════════════════════════
#  ── RENDER: WALLS ──────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════
def cast_rays():
    """DDA raycasting: one ray per STRIP columns."""
    flick_t = tick * 0.0015   # torch-flicker time

    for col in range(RAYS):
        # Ray direction in world space
        cx  = 2.0 * col / RAYS - 1.0     # -1 (left) to +1 (right)
        rdx = dx + plx * cx
        rdy = dy + ply * cx

        # Grid cell the player stands in
        mx_, my_ = int(px), int(py)

        # Delta-distances between consecutive x/y grid crossings
        ddx = abs(1.0 / rdx) if rdx else 1e30
        ddy = abs(1.0 / rdy) if rdy else 1e30

        # Step direction and initial side-distances
        if rdx < 0: sdx = -1; ssx = (px - mx_) * ddx
        else:        sdx = +1; ssx = (mx_ + 1 - px) * ddx
        if rdy < 0: sdy = -1; ssy = (py - my_) * ddy
        else:        sdy = +1; ssy = (my_ + 1 - py) * ddy

        # March until wall
        hit = side = 0
        for _ in range(64):
            if ssx < ssy: ssx += ddx; mx_ += sdx; side = 0
            else:          ssy += ddy; my_ += sdy; side = 1
            w = mat(mx_, my_)
            if w: hit = w; break

        # Perpendicular (non-fisheye) wall distance
        if   side == 0: perp = (mx_ - px + (1 - sdx) / 2) / rdx
        else:            perp = (my_ - py + (1 - sdy) / 2) / rdy
        perp = max(0.0002, perp)

        # Wall strip height and vertical bounds
        lh = int(SH / perp)
        y0 = max(0, HH - lh // 2)
        y1 = min(SH, HH + lh // 2)

        # Colour = base × distance-fog × torch-flicker × side-shade
        base   = WALL_BASE.get(hit, (80, 80, 80))
        fog    = max(0.0, min(1.0, 1.0 - perp / 15.0))
        flick  = 1.0 + 0.055 * math.sin(flick_t * 7.3 + col * 0.11)
        shade  = fog * flick * (0.58 if side == 1 else 1.0)

        r = max(0, min(255, int(base[0] * shade)))
        g = max(0, min(255, int(base[1] * shade)))
        b = max(0, min(255, int(base[2] * shade)))

        # Draw strip (STRIP pixels wide)
        sx = col * STRIP
        pygame.draw.rect(screen, (r, g, b), (sx, y0, STRIP, y1 - y0))

        # Fill z-buffer
        for i in range(STRIP):
            if sx + i < SW:
                z_buf[sx + i] = perp


# ═══════════════════════════════════════════════════════════════
#  ── RENDER: SPRITES ────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════
def draw_sprites():
    """2.5D billboard sprite rendering with z-buffer occlusion."""
    t = tick * 0.003

    # Sort far-to-near so nearer sprites overdraw farther ones
    ordered = sorted(sprites, reverse=True,
                     key=lambda s: (s[0] - px)**2 + (s[1] - py)**2)

    for spr in ordered:
        if not spr[3]: continue

        sx_, sy_, kind = spr[0], spr[1], spr[2]

        # Translate relative to player, then transform into camera space
        rx = sx_ - px
        ry = sy_ - py
        inv = 1.0 / (plx * dy - dx * ply)   # det of 2×2 camera matrix
        tx_ = inv * ( dy * rx -  dx * ry)
        ty_ = inv * (-ply * rx + plx * ry)

        if ty_ <= 0.12: continue   # behind camera or too close

        # Screen-space horizontal centre and size
        scx = int(SW / 2 * (1 + tx_ / ty_))
        sph = abs(int(SH / ty_))             # sprite height in pixels
        spw = sph                             # keep aspect 1:1

        x0 = scx - spw // 2;  x1 = scx + spw // 2
        y0 = HH  - sph // 2;  y1 = HH  + sph // 2

        fog = max(0.0, min(1.0, 1.0 - ty_ / 11.0))
        if kind == "exit":
            fog *= (0.65 + 0.35 * math.sin(t * 4.2))  # pulsing portal

        fc = tuple(int(c * fog) for c in SPR_COL[kind])   # full bright
        dk = tuple(int(c * fog * 0.38) for c in SPR_COL[kind])  # dark

        # Render column-by-column (checking z-buffer per pixel column)
        for x in range(max(0, x0), min(SW, x1)):
            if ty_ >= z_buf[x]: continue      # wall in front → skip

            y0c = max(0, y0);  y1c = min(SH, y1)
            if y0c >= y1c: continue

            rel = (x - x0) / max(1, spw)      # 0 → 1 across sprite width

            # ── Key: vertical bar + bow shape ──────────────────────────
            if kind == "key":
                if 0.30 < rel < 0.70:
                    pygame.draw.line(screen, fc, (x, y0c), (x, y1c))
                if 0.42 < rel < 0.58:
                    mid = y0c + (y1c - y0c) // 2
                    pygame.draw.line(screen, dk, (x, mid), (x, y1c))

            # ── Enemy: red silhouette + dark "eye" stripes ─────────────
            elif kind == "enemy":
                if 0.06 < rel < 0.94:
                    pygame.draw.line(screen, fc, (x, y0c), (x, y1c))
                # Eyes (dark horizontal band)
                if 0.28 < rel < 0.44 or 0.56 < rel < 0.72:
                    ey  = y0 + sph // 3
                    eh  = max(1, sph // 10)
                    ey0 = max(y0c, ey - eh)
                    ey1 = min(y1c, ey + eh)
                    if ey0 < ey1:
                        pygame.draw.line(screen, (8, 8, 8), (x, ey0), (x, ey1))

            # ── Health: red cross ───────────────────────────────────────
            elif kind == "health":
                cx_ = (x0 + x1) // 2
                cy_ = (y0 + y1) // 2
                bw  = max(1, spw // 5)
                bh  = max(1, sph // 5)
                if abs(x - cx_) < bw:
                    pygame.draw.line(screen, fc, (x, y0c), (x, y1c))
                else:
                    ey0 = max(y0c, cy_ - bh)
                    ey1 = min(y1c, cy_ + bh)
                    if ey0 < ey1:
                        pygame.draw.line(screen, fc, (x, ey0), (x, ey1))

            # ── Exit: swirling green portal ─────────────────────────────
            elif kind == "exit":
                wave = math.sin(t * 3.0 + rel * math.pi * 4.5)
                if wave > -0.15:
                    pygame.draw.line(screen, fc, (x, y0c), (x, y1c))
                # Bright core
                if 0.38 < rel < 0.62:
                    bright = tuple(min(255, int(c * 1.5)) for c in fc)
                    pygame.draw.line(screen, bright, (x, y0c), (x, y1c))


# ═══════════════════════════════════════════════════════════════
#  ── RENDER: ANIMATED WEAPON ────────────────────────────────────
# ═══════════════════════════════════════════════════════════════
def draw_weapon():
    """First-person sword with idle bob animation."""
    bob_y = math.sin(tick * 0.07)  * 5
    bob_x = math.sin(tick * 0.035) * 4
    bx = SW // 2 + 188 + int(bob_x)
    by = SH - 115 + int(bob_y)

    # Blade highlight
    pygame.draw.polygon(screen, (195, 210, 222),
                        [(bx, by - 26), (bx - 5, by + 30), (bx + 5, by + 30)])
    # Blade body
    pygame.draw.polygon(screen, (155, 168, 178),
                        [(bx, by), (bx - 12, by + 76), (bx + 12, by + 76)])
    # Fuller (groove down center)
    pygame.draw.line(screen, (100, 112, 122), (bx, by + 5), (bx, by + 70), 2)
    # Cross-guard
    pygame.draw.rect(screen, (102, 82, 52), (bx - 20, by + 76, 40, 8))
    pygame.draw.rect(screen, (82,  65, 40), (bx - 20, by + 76, 40, 8), 1)
    # Handle wrap
    for i in range(0, 28, 5):
        col_ = (88, 58, 38) if i % 10 == 0 else (70, 46, 30)
        pygame.draw.rect(screen, col_, (bx - 5, by + 84 + i, 10, 4))
    # Pommel
    pygame.draw.circle(screen, (110, 90, 62), (bx, by + 114), 6)
    pygame.draw.circle(screen, (130, 108, 78), (bx, by + 114), 4)


# ═══════════════════════════════════════════════════════════════
#  ── RENDER: MINIMAP ────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════
def draw_minimap():
    """Top-right corner overhead map."""
    s  = 7
    ox = SW - MW * s - 9
    oy = 9
    WCOLS = {1:(62,58,72), 2:(88,44,40), 3:(36,40,98), 4:(40,78,40)}

    # Background
    pygame.draw.rect(screen, (0, 0, 0), (ox-2, oy-2, MW*s+4, MH*s+4))
    pygame.draw.rect(screen, (45, 45, 65), (ox-2, oy-2, MW*s+4, MH*s+4), 1)

    # Cells
    for row in range(MH):
        for col in range(MW):
            w = mat(col, row)
            if w:
                pygame.draw.rect(screen, WCOLS.get(w, (62,58,72)),
                                 (ox + col*s, oy + row*s, s-1, s-1))

    # Sprite dots
    for spr in sprites:
        if not spr[3]: continue
        mx_ = ox + int(spr[0] * s)
        my_ = oy + int(spr[1] * s)
        pygame.draw.rect(screen, SPR_COL[spr[2]], (mx_-2, my_-2, 4, 4))

    # Player position + direction arrow
    ppx = ox + int(px * s)
    ppy = oy + int(py * s)
    pygame.draw.circle(screen, (100, 215, 255), (ppx, ppy), 3)
    pygame.draw.line(screen, (185, 235, 255),
                     (ppx, ppy), (ppx + int(dx * 9), ppy + int(dy * 9)), 2)


# ═══════════════════════════════════════════════════════════════
#  ── RENDER: HUD ─────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════
def draw_hud():
    """Crosshair, health bar, key counter, flash & vignette."""

    # Crosshair
    cx, cy = SW // 2, HH
    pygame.draw.line(screen, (200, 200, 200), (cx-9,  cy), (cx+9,  cy), 1)
    pygame.draw.line(screen, (200, 200, 200), (cx,  cy-9), (cx,  cy+9), 1)
    pygame.draw.circle(screen, (185, 185, 185), (cx, cy), 5, 1)

    # HUD panel (bottom-left semi-transparent box)
    panel = pygame.Surface((290, 56), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 145))
    screen.blit(panel, (8, SH - 64))

    # Health bar
    pygame.draw.rect(screen, (50, 10, 10),  (18, SH - 48, 168, 16))
    bar_col = (205, 62, 62) if health > 30 else (255, 32, 32)
    pygame.draw.rect(screen, bar_col, (18, SH - 48, int(168 * health / 100), 16))
    pygame.draw.rect(screen, (135, 72, 72), (18, SH - 48, 168, 16), 1)
    screen.blit(F_SM.render(f"HP  {health}", True, (225, 175, 175)), (192, SH - 48))

    # Key counter
    screen.blit(F_SM.render(f"Keys:  {keys_held} / {KEYS_NEED}", True, (255, 215, 32)),
                (18, SH - 28))

    # "Find exit" hint
    if keys_held >= KEYS_NEED:
        hint = F_SM.render("All keys collected!  Find the glowing EXIT  ▶",
                           True, (55, 255, 100))
        screen.blit(hint, (SW // 2 - hint.get_width() // 2, SH - 26))

    # Damage flash
    if dmg_flash > 0:
        alpha = int(95 * dmg_flash / 20)
        dmg_surf.fill((165, 0, 0, alpha))
        screen.blit(dmg_surf, (0, 0))

    # Vignette (dark edges)
    screen.blit(vign, (0, 0))


# ═══════════════════════════════════════════════════════════════
#  PLAYER UPDATE (movement, collision, sprite interaction)
# ═══════════════════════════════════════════════════════════════
def update_game():
    global px, py, dx, dy, plx, ply
    global health, keys_held, dmg_flash, hurt_cd, STATE

    kp = pygame.key.get_pressed()
    fwd = strafe = 0.0

    # Movement input
    if kp[pygame.K_w] or kp[pygame.K_UP]:    fwd    += MOV_SPD
    if kp[pygame.K_s] or kp[pygame.K_DOWN]:  fwd    -= MOV_SPD
    if kp[pygame.K_q]:                        strafe -= MOV_SPD
    if kp[pygame.K_e]:                        strafe += MOV_SPD

    # Rotation input
    rot = 0.0
    if kp[pygame.K_a] or kp[pygame.K_LEFT]:  rot -= ROT_SPD
    if kp[pygame.K_d] or kp[pygame.K_RIGHT]: rot += ROT_SPD
    if rot:
        cos_r, sin_r = math.cos(rot), math.sin(rot)
        dx,  dy  = dx*cos_r  - dy*sin_r,  dx*sin_r  + dy*cos_r
        plx, ply = plx*cos_r - ply*sin_r, plx*sin_r + ply*cos_r

    # Translate and apply collision (wall sliding)
    if fwd or strafe:
        nx = px + dx * fwd - dy * strafe
        ny = py + dy * fwd + dx * strafe
        R  = COLL_R
        if mat(int(nx + R), int(py)) == 0 and mat(int(nx - R), int(py)) == 0:
            px = nx
        if mat(int(px), int(ny + R)) == 0 and mat(int(px), int(ny - R)) == 0:
            py = ny

    # Sprite interaction (pickups and damage)
    for spr in sprites:
        if not spr[3]: continue
        dist = math.hypot(spr[0] - px, spr[1] - py)

        if spr[2] == "key" and dist < 0.90:
            spr[3] = False
            keys_held += 1

        elif spr[2] == "health" and dist < 0.90 and health < 100:
            spr[3] = False
            health  = min(100, health + 38)

        elif spr[2] == "enemy" and dist < 0.68 and hurt_cd <= 0:
            health    -= 14
            dmg_flash  = 20
            hurt_cd    = 62
            if health <= 0:
                health = 0
                STATE  = "lose"

        elif spr[2] == "exit" and dist < 1.25 and keys_held >= KEYS_NEED:
            STATE = "win"

    if hurt_cd   > 0: hurt_cd   -= 1
    if dmg_flash > 0: dmg_flash -= 1


# ═══════════════════════════════════════════════════════════════
#  SCREEN-STATE RENDERERS
# ═══════════════════════════════════════════════════════════════

def draw_title():
    t = tick * 0.001
    screen.fill((7, 5, 18))

    # Animated starfield
    random.seed(42)
    for _ in range(220):
        rx_ = random.randint(0, SW - 1)
        ry_ = random.randint(0, SH - 1)
        br  = int(50 + 38 * math.sin(t * 2.1 + rx_ * 0.05 + ry_ * 0.07))
        pygame.draw.circle(screen, (br, br, br + 28), (rx_, ry_), 1)

    # Glow behind title
    for rr, aa in [(340, 35), (290, 28), (240, 22)]:
        gs = pygame.Surface((rr * 2, rr), pygame.SRCALPHA)
        gs.fill((60, 30, 120, aa))
        screen.blit(gs, (SW // 2 - rr, SH // 2 - 220))

    # Title text
    t1 = F_XL.render("DARK",    True, (205, 175, 255))
    t2 = F_XL.render("DUNGEON", True, (155, 115, 255))
    t3 = F_MD.render("3D  Raycasting  ·  Python",  True, (145, 125, 205))
    screen.blit(t1, (SW // 2 - t1.get_width() // 2, SH // 2 - 215))
    screen.blit(t2, (SW // 2 - t2.get_width() // 2, SH // 2 - 148))
    screen.blit(t3, (SW // 2 - t3.get_width() // 2, SH // 2 -  72))

    # Divider
    div_col = (80, 60, 130)
    pygame.draw.line(screen, div_col,
                     (SW // 2 - 240, SH // 2 - 40), (SW // 2 + 240, SH // 2 - 40), 1)

    # Controls
    ctls = [
        ("W / S",    "Move forward / back"),
        ("A / D",    "Turn left / right"),
        ("Q / E",    "Strafe left / right"),
        ("ESC",      "Quit"),
    ]
    y = SH // 2 - 20
    for ks, ac in ctls:
        screen.blit(F_SM.render(ks, True, (255, 215, 55)), (SW // 2 - 175, y))
        screen.blit(F_SM.render(ac, True, (185, 162, 215)), (SW // 2 - 60, y))
        y += 26

    obj = F_SM.render(
        "Collect 3 gold keys  ·  Find the green EXIT  ·  Avoid enemies",
        True, (95, 210, 115))
    screen.blit(obj, (SW // 2 - obj.get_width() // 2, y + 14))

    # Pulsing prompt
    pa  = int(178 + 77 * math.sin(t * 5))
    prm = F_LG.render("PRESS  SPACE  TO  ENTER", True, (pa, pa, pa))
    screen.blit(prm, (SW // 2 - prm.get_width() // 2, SH // 2 + 165))


def draw_win():
    t  = tick * 0.001
    screen.fill((4, 16, 5))
    w1 = F_XL.render("YOU  ESCAPED!", True, (55, 255, 105))
    w2 = F_MD.render("The dungeon lies far behind you…", True, (135, 215, 140))
    pa = int(178 + 77 * math.sin(t * 4))
    w3 = F_MD.render("SPACE to play again  ·  ESC to quit", True, (pa, pa, pa))
    for surf, y_off in [(w1, -115), (w2, -28), (w3, 58)]:
        screen.blit(surf, (SW // 2 - surf.get_width() // 2, SH // 2 + y_off))


def draw_lose():
    t  = tick * 0.001
    screen.fill((16, 3, 3))
    l1 = F_XL.render("YOU  PERISHED", True, (225, 42, 42))
    l2 = F_MD.render("The darkness consumed you…", True, (158, 82, 82))
    pa = int(178 + 77 * math.sin(t * 4))
    l3 = F_MD.render("SPACE to try again  ·  ESC to quit",
                      True, (pa, pa // 2, pa // 2))
    for surf, y_off in [(l1, -115), (l2, -28), (l3, 58)]:
        screen.blit(surf, (SW // 2 - surf.get_width() // 2, SH // 2 + y_off))


# ═══════════════════════════════════════════════════════════════
#  RESET
# ═══════════════════════════════════════════════════════════════
def reset():
    global px, py, dx, dy, plx, ply
    global health, keys_held, dmg_flash, hurt_cd, STATE, tick

    px, py   = 1.5, 1.5
    dx, dy   = 1.0, 0.0
    plx, ply = 0.0, 0.66
    health     = 100
    keys_held  = 0
    dmg_flash  = 0
    hurt_cd    = 0
    tick       = 0
    STATE      = "game"
    for s in sprites:
        s[3] = True


# ═══════════════════════════════════════════════════════════════
#  MAIN LOOP
# ═══════════════════════════════════════════════════════════════
def main():
    global STATE, tick

    while True:
        tick += 1
        clock.tick(60)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.mouse.set_visible(True)
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    pygame.mouse.set_visible(True)
                    pygame.quit(); sys.exit()
                if ev.key == pygame.K_SPACE:
                    if STATE in ("title", "win", "lose"):
                        reset()

        if STATE == "title":
            draw_title()

        elif STATE == "game":
            update_game()
            screen.blit(sky, (0, 0))          # sky + floor gradient
            cast_rays()                        # 3D walls
            draw_sprites()                     # 2.5D billboards
            draw_weapon()                      # first-person sword
            draw_minimap()                     # overhead map
            draw_hud()                         # health / keys / overlay

        elif STATE == "win":
            draw_win()

        elif STATE == "lose":
            draw_lose()

        pygame.display.flip()


if __name__ == "__main__":
    main()