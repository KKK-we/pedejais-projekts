import tkinter as tk

root = tk.Tk()
root.title("Princess and the Black Man")
root.geometry("1366x768")
root.resizable(False, False)

canvas = tk.Canvas(root, width=1366, height=768, bg="#2d2d1a")
canvas.pack()

# =====================
# PLATFORMAS
# =====================
platforms = [
    (0, 700, 1366, 768),
    (0, 150, 300, 200),
    (200, 200, 800, 250),
    (850, 180, 1200, 230),
    (150, 450, 850, 500),
    (900, 450, 1200, 500),
    (250, 600, 700, 650),
    (850, 620, 1300, 670),
    (1050, 300, 1200, 350),
    (500, 400, 600, 430),
]

platform_rects = []
for p in platforms:
    platform_rects.append(
        canvas.create_rectangle(p, fill="#8c7b4f", outline="black")
    )

# =====================
# ŪDENS
# =====================
water_areas = [
    canvas.create_rectangle(250, 230, 350, 250, fill="deepskyblue"),
    canvas.create_rectangle(450, 480, 650, 500, fill="deepskyblue"),
]

# =====================
# FINIŠS
# =====================
finish = canvas.create_rectangle(1220, 100, 1300, 180, fill="gold")

# =====================
# SPĒLĒTĀJS
# =====================
player = canvas.create_rectangle(50, 640, 90, 690, fill="black")

# =====================
# PRINCESE (BLAKUS SPĒLĒTĀJAM)
# =====================
princess = canvas.create_rectangle(120, 640, 160, 690, fill="pink")

# =====================
# FIZIKA
# =====================
player_speed = 7
jump_strength = -18
gravity = 0.9
velocity_y = 0
on_ground = False

# princeses fizika
princess_vy = 0
princess_gravity = 0.9
princess_jump = -16
princess_on_ground = False

slow_timer = 0

# =====================
# POGAS
# =====================
keys = {"Left": False, "Right": False, "space": False, "w": False}

def key_press(e):
    if e.keysym in keys:
        keys[e.keysym] = True

def key_release(e):
    if e.keysym in keys:
        keys[e.keysym] = False

root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)

# =====================
# SADURSMES
# =====================
def collide(a, b):
    x1, y1, x2, y2 = canvas.coords(a)
    a1, b1, a2, b2 = canvas.coords(b)
    return x1 < a2 and x2 > a1 and y1 < b2 and y2 > b1

# =====================
# SPĒLES CIKLS
# =====================
def game_loop():
    global velocity_y, on_ground
    global princess_vy, princess_on_ground, slow_timer

    speed = 3 if slow_timer > 0 else player_speed

    # =====================
    # SPĒLĒTĀJS
    # =====================
    if keys["Left"]:
        canvas.move(player, -speed, 0)

    if keys["Right"]:
        canvas.move(player, speed, 0)

    if keys["space"] and on_ground:
        velocity_y = jump_strength
        on_ground = False

    velocity_y += gravity
    canvas.move(player, 0, velocity_y)

    px1, py1, px2, py2 = canvas.coords(player)
    on_ground = False

    for p in platform_rects:
        if collide(player, p):
            x1, y1, x2, y2 = canvas.coords(p)
            if velocity_y >= 0:
                canvas.coords(player, px1, y1 - 50, px2, y1)
                velocity_y = 0
                on_ground = True

    # ūdens
    for w in water_areas:
        if collide(player, w):
            slow_timer = 120

    if slow_timer > 0:
        slow_timer -= 1

    # =====================
    # PRINCESE (AI + LĒCIENS)
    # =====================
    if keys["w"] and princess_on_ground:
        princess_vy = princess_jump
        princess_on_ground = False

    princess_vy += princess_gravity
    canvas.move(princess, 0, princess_vy)

    px1, py1, px2, py2 = canvas.coords(princess)
    princess_on_ground = False

    for p in platform_rects:
        x1, y1, x2, y2 = canvas.coords(p)
        if collide(princess, p):
            if princess_vy >= 0:
                canvas.coords(princess, px1, y1 - 50, px2, y1)
                princess_vy = 0
                princess_on_ground = True

    # kustas uz finišu
    f1, f2, f3, f4 = canvas.coords(finish)
    if px1 < f1:
        canvas.move(princess, 1.5, 0)

    # =====================
    # WIN / LOSE
    # =====================
    if collide(player, princess):
        canvas.create_text(683, 300, text="TU UZVARĒJI!", fill="white", font=("Arial", 40))
        return

    if collide(princess, finish):
        canvas.create_text(683, 300, text="TU ZAUDĒJI!", fill="white", font=("Arial", 40))
        return

    root.after(20, game_loop)

game_loop()
root.mainloop()