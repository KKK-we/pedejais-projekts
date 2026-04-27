import tkinter as tk

# =====================
# WINDOW
# =====================
root = tk.Tk()
root.title("Princess and the Black Man")
root.geometry("800x500")

canvas = tk.Canvas(root, width=800, height=500, bg="black")
canvas.pack()

# =====================
# GLOBALS
# =====================
player = None
princess = None
finish = None

platforms = []

gravity = 1

p_vel = 0
p_on_ground = False

ai_vel = 0
ai_on_ground = False

level_index = 0

left = right = jump = False

# =====================
# LEVELS
# =====================
levels = [

# ===== LEVEL 1 =====
{
"player":(50,400,80,430),
"princess":(300,400,330,430),
"finish":(700,200,760,260),

"platforms":[
(0,450,800,500),
(0,0,10,500),(790,0,800,500),

(150,380,300,400),
(350,330,500,350),
(550,280,700,300)
]
},

# ===== LEVEL 2 =====
{
"player":(50,400,80,430),
"princess":(350,400,380,430),
"finish":(700,150,760,210),

"platforms":[
(0,450,800,500),
(0,0,10,500),(790,0,800,500),

(100,380,200,400),
(250,340,350,360),
(400,300,500,320),
(550,260,650,280),
(700,220,780,240)
]
},

# ===== LEVEL 3 =====
{
"player":(50,400,80,430),
"princess":(400,400,430,430),
"finish":(700,100,760,160),

"platforms":[
(0,450,800,500),
(0,0,10,500),(790,0,800,500),

(150,380,200,400),
(250,330,300,350),
(350,280,400,300),
(450,230,500,250),
(550,180,600,200),
(650,130,700,150)
]
}
]

# =====================
# INPUT
# =====================
def key_press(e):
    global left, right, jump
    if e.keysym == "Left": left = True
    if e.keysym == "Right": right = True
    if e.keysym == "space": jump = True

def key_release(e):
    global left, right, jump
    if e.keysym == "Left": left = False
    if e.keysym == "Right": right = False
    if e.keysym == "space": jump = False

root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)

# =====================
# COLLISION
# =====================
def hit(a, b):
    x1,y1,x2,y2 = canvas.coords(a)
    a1,b1,a2,b2 = canvas.coords(b)
    return x1<a2 and x2>a1 and y1<b2 and y2>b1

# =====================
# LOAD LEVEL
# =====================
def load_level(i):
    global player, princess, finish, platforms
    global p_vel, ai_vel

    canvas.delete("all")
    platforms.clear()

    lvl = levels[i]

    for p in lvl["platforms"]:
        platforms.append(canvas.create_rectangle(*p, fill="#8c7b4f"))

    finish = canvas.create_rectangle(*lvl["finish"], fill="gold")

    player = canvas.create_rectangle(*lvl["player"], fill="#3b2f2f")
    princess = canvas.create_rectangle(*lvl["princess"], fill="pink")

    p_vel = 0
    ai_vel = 0

# =====================
# PRINCESS AI (uzlabots)
# =====================
def princess_ai():
    global ai_vel, ai_on_ground

    prx1, pry1, prx2, pry2 = canvas.coords(princess)
    px1, _, _, _ = canvas.coords(player)
    fx1, _, _, _ = canvas.coords(finish)

    dist_player = abs(prx1 - px1)

    # ===== STRATEGY =====
    if dist_player < 90:
        move = 5 if prx1 > px1 else -5   # bēg no spēlētāja
    else:
        move = 3 if prx1 < fx1 else -3   # iet uz finišu

    # ===== WALL DETECT + JUMP =====
    for p in platforms:
        x1,y1,x2,y2 = canvas.coords(p)

        if (
            prx2 + 5 > x1 and prx1 < x1
            and pry2 > y1 - 20 and pry2 < y1 + 20
        ):
            if ai_on_ground:
                ai_vel = -15

    # ===== SAFE CHECK =====
    safe = False
    for p in platforms:
        x1,y1,x2,y2 = canvas.coords(p)

        if (
            prx1 + move > x1 and prx2 + move < x2
            and abs(pry2 - y1) < 5
        ):
            safe = True

    if not safe:
        move = 0

    return move

# =====================
# GAME LOOP
# =====================
def game_loop():
    global p_vel, p_on_ground
    global ai_vel, ai_on_ground
    global level_index

    # ===== PLAYER =====
    dx = 0
    if left: dx -= 5
    if right: dx += 5

    canvas.move(player, dx, 0)

    if jump and p_on_ground:
        p_vel = -15

    p_vel += gravity
    canvas.move(player, 0, p_vel)

    px1, py1, px2, py2 = canvas.coords(player)
    p_on_ground = False

    for p in platforms:
        if hit(player, p):
            x1,y1,x2,y2 = canvas.coords(p)
            if p_vel > 0:
                canvas.coords(player, px1, y1-30, px2, y1)
                p_vel = 0
                p_on_ground = True

    # ===== PRINCESS =====
    ai_vel += gravity
    canvas.move(princess, 0, ai_vel)

    prx1, pry1, prx2, pry2 = canvas.coords(princess)
    ai_on_ground = False

    for p in platforms:
        if hit(princess, p):
            x1,y1,x2,y2 = canvas.coords(p)
            if ai_vel > 0:
                canvas.coords(princess, prx1, y1-30, prx2, y1)
                ai_vel = 0
                ai_on_ground = True

    move = princess_ai()
    canvas.move(princess, move, 0)

    # ===== WIN (FIXED COLLISION) =====
    if hit(player, princess):
        level_index += 1
        if level_index >= len(levels):
            canvas.create_text(400,200,text="TU VINNĒJI VISU!",fill="white",font=("Arial",25))
            return
        load_level(level_index)

    # ===== LOSE =====
    if hit(princess, finish):
        canvas.create_text(400,200,text="PRINCESE AIZBĒGA!",fill="red",font=("Arial",25))
        return

    root.after(20, game_loop)

# =====================
# START
# =====================
load_level(level_index)
game_loop()
root.mainloop()