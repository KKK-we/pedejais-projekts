import tkinter as tk
import random

root = tk.Tk()
root.title("Princess and the Black Man")
root.geometry("1366x768")

canvas = tk.Canvas(root, width=1366, height=768, bg="black")
canvas.pack()

# =====================
# GLOBAL
# =====================
player = None
princess = None
finish = None

platforms = []
lavas = []

gravity = 1

p_vel = 0
p_on_ground = False

ai_vel = 0
ai_on_ground = False

left = right = jump = False

# =====================
# LEVEL
# =====================
level = {
"spawn_player":(50,650,90,690),
"spawn_princess":(200,650,240,690),

"platforms":[
(0,700,1366,768),
(0,0,20,768),(1346,0,1366,768),

(200,600,400,630),
(500,550,700,580),
(800,500,1000,530),

(300,400,500,430),
(700,350,900,380),

(1000,250,1200,280)
],

"lavas":[(400,690,800,700)],
"finish":(1100,200,1200,240)
}

# =====================
# INPUT
# =====================
def key_press(e):
    global left,right,jump
    if e.keysym=="Left": left=True
    if e.keysym=="Right": right=True
    if e.keysym=="space": jump=True

def key_release(e):
    global left,right,jump
    if e.keysym=="Left": left=False
    if e.keysym=="Right": right=False
    if e.keysym=="space": jump=False

root.bind("<KeyPress>",key_press)
root.bind("<KeyRelease>",key_release)

# =====================
# LOAD
# =====================
def load_level():
    global player, princess, finish
    global p_vel, ai_vel

    canvas.delete("all")
    platforms.clear()
    lavas.clear()

    for p in level["platforms"]:
        platforms.append(canvas.create_rectangle(*p, fill="#8c7b4f"))

    for l in level["lavas"]:
        lavas.append(canvas.create_rectangle(*l, fill="red"))

    finish = canvas.create_rectangle(*level["finish"], fill="gold")

    # 🔥 PLAYER (tumši brūns)
    player = canvas.create_rectangle(*level["spawn_player"], fill="#3b2f2f")

    princess = canvas.create_rectangle(*level["spawn_princess"], fill="pink")

    p_vel = 0
    ai_vel = 0

# =====================
# COLLISION
# =====================
def hit(a,b):
    x1,y1,x2,y2 = canvas.coords(a)
    a1,b1,a2,b2 = canvas.coords(b)
    return x1<a2 and x2>a1 and y1<b2 and y2>b1

# =====================
# AI
# =====================
def ai_move():
    global ai_vel, ai_on_ground

    prx1, pry1, prx2, pry2 = canvas.coords(princess)
    px1, _, _, _ = canvas.coords(player)
    fx1, _, _, _ = canvas.coords(finish)

    move = 0

    # TARGET
    if abs(prx1 - px1) < 120:
        target = 0 if prx1 > px1 else 1366
    else:
        target = fx1

    move = 4 if prx1 < target else -4

    # WALL DETECT → JUMP
    for p in platforms:
        x1,y1,x2,y2 = canvas.coords(p)

        if (
            prx2 + 5 > x1
            and prx1 < x1
            and pry2 > y1 - 20
            and pry2 < y1 + 20
        ):
            if ai_on_ground:
                ai_vel = -16

    # DON'T FALL
    safe = False
    for p in platforms:
        x1,y1,x2,y2 = canvas.coords(p)

        if (
            prx1 + move > x1
            and prx2 + move < x2
            and abs(pry2 - y1) < 5
        ):
            safe = True

    if not safe:
        move = 0

    # AVOID LAVA
    for l in lavas:
        lx1,ly1,lx2,ly2 = canvas.coords(l)

        if prx2 + move > lx1 and prx1 + move < lx2:
            if ai_on_ground:
                ai_vel = -18
            move = -move

    return move

# =====================
# LOOP
# =====================
def game_loop():
    global p_vel,p_on_ground
    global ai_vel,ai_on_ground

    # PLAYER
    dx = (-7 if left else 0) + (7 if right else 0)
    canvas.move(player, dx, 0)

    if jump and p_on_ground:
        p_vel = -18

    p_vel += gravity
    canvas.move(player, 0, p_vel)

    px1,py1,px2,py2 = canvas.coords(player)
    p_on_ground = False

    for p in platforms:
        if hit(player,p):
            x1,y1,x2,y2 = canvas.coords(p)

            if p_vel > 0:
                canvas.coords(player, px1, y1-40, px2, y1)
                p_vel = 0
                p_on_ground = True

    # PLAYER LAVA
    for l in lavas:
        if hit(player,l):
            load_level()

    # PRINCESS
    ai_vel += gravity
    canvas.move(princess, 0, ai_vel)

    prx1,pry1,prx2,pry2 = canvas.coords(princess)
    ai_on_ground = False

    for p in platforms:
        if hit(princess,p):
            x1,y1,x2,y2 = canvas.coords(p)

            if ai_vel > 0:
                canvas.coords(princess, prx1, y1-40, prx2, y1)
                ai_vel = 0
                ai_on_ground = True

    move = ai_move()
    canvas.move(princess, move, 0)

    # WALL COLLISION FIX
    for p in platforms:
        if hit(princess, p):
            x1,y1,x2,y2 = canvas.coords(p)

            if move > 0:
                canvas.coords(princess, x1-40, pry1, x1, pry2)
            if move < 0:
                canvas.coords(princess, x2, pry1, x2+40, pry2)

    # WIN
    if abs(prx1 - px1) < 40:
        canvas.create_text(600,300,text="TU VINNĒJI!",fill="white",font=("Arial",30))
        root.after(1500, load_level)

    root.after(20, game_loop)

# =====================
# START
# =====================
load_level()
game_loop()
root.mainloop()