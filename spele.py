import tkinter as tk

root = tk.Tk()
root.title("Princess and the Black Man")
root.geometry("1366x768")

canvas = tk.Canvas(root, width=1366, height=768, bg="#1f1f1f")
canvas.pack()

# ===== STATE =====
current_level = 0
game_won = False
game_lost = False

platforms = []
moving_platforms = []
lava_areas = []

player = None
princess = None
finish = None

gravity = 1
player_vel = 0
player_on_ground = False

princess_vel = 0
princess_on_ground = False

left = right = jump = False

# ===== INPUT =====
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

# ===== COLLISION =====
def collide(a, b):
    x1,y1,x2,y2 = canvas.coords(a)
    a1,b1,a2,b2 = canvas.coords(b)
    return x1<a2 and x2>a1 and y1<b2 and y2>b1

# ===== LEVELS (SALABOTS) =====
levels = [

# ===== LEVEL 0 =====
{
    "spawn_player": (80,650,120,690),
    "spawn_princess": (160,650,200,690),

    "platforms":[
        (0,700,1366,768),
        (0,0,20,768),
        (1346,0,1366,768),

        (200,600,400,630),
        (500,550,700,580),
        (800,500,1000,530),

        (300,400,500,430),
        (700,350,900,380),

        (1000,250,1200,280)
    ],

    "moving":[
        [400,300,550,330,2]
    ],

    "waters":[],
    "lavas":[
        (300,690,700,700),
        (800,690,1200,700)
    ],

    "finish":(1050,200,1150,240)
},

# ===== LEVEL 1 =====
{
    "spawn_player": (50,650,90,700),
    "spawn_princess": (120,650,160,700),

    "platforms":[
        (0,700,1366,768),
        (0,0,20,768),
        (1346,0,1366,768),

        (0,600,400,630),
        (450,600,900,630),
        (950,600,1366,630),

        (200,480,600,510),
        (700,480,1100,510),

        (100,350,400,380),
        (500,350,900,380),
        (1000,350,1300,380),

        (1100,200,1350,230)
    ],

    "moving":[],

    "waters":[
        (250,470,350,480),
        (750,470,850,480)
    ],

    "lavas":[
        (500,690,700,700)
    ],

    "finish":(1200,150,1300,200),
    "princess_speed":4
},

# ===== LEVEL 2 =====
{
    "spawn_player": (50,650,90,700),
    "spawn_princess": (120,650,160,700),

    "platforms":[
        (0,700,1366,768),
        (0,0,20,768),
        (1346,0,1366,768),

        (0,620,200,650),
        (250,580,450,610),
        (500,540,700,570),
        (750,500,950,530),
        (1000,460,1200,490),

        (300,420,600,450),
        (700,380,1000,410),

        (200,300,400,330),
        (500,260,700,290),
        (800,220,1000,250),

        (1100,150,1300,180)
    ],

    "moving":[],

    "waters":[
        (520,530,680,540),
        (820,370,950,380)
    ],

    "lavas":[
        (300,690,600,700),
        (900,690,1200,700)
    ],

    "finish":(1150,100,1250,140),
    "princess_speed":5
},

# ===== LEVEL 3 =====
{
    "spawn_player": (50,650,90,700),
    "spawn_princess": (120,650,160,700),

    "platforms":[
        (0,700,1366,768),
        (0,0,20,768),
        (1346,0,1366,768),

        (0,630,300,660),
        (350,630,700,660),
        (750,630,1100,660),
        (1150,630,1366,660),

        (200,520,260,550),
        (350,480,420,510),
        (500,440,570,470),
        (650,400,720,430),
        (800,360,870,390),
        (950,320,1020,350),

        (200,250,500,280),
        (600,200,900,230),
        (1000,160,1300,190)
    ],

    "moving":[],

    "waters":[
        (210,510,250,520),
        (660,390,710,400),
        (960,310,1010,320)
    ],

    "lavas":[
        (350,690,700,700),
        (750,690,1100,700)
    ],

    "finish":(1150,100,1300,140),
    "princess_speed":6
}

]

# ===== LOAD =====
def load_level(i):
    global platforms, moving_platforms, lava_areas
    global player, princess, finish
    global player_vel, princess_vel

    canvas.delete("all")

    platforms = []
    moving_platforms = []
    lava_areas = []

    lvl = levels[i]

    for p in lvl["platforms"]:
        platforms.append(canvas.create_rectangle(*p, fill="#8c7b4f"))

    for m in lvl.get("moving", []):
        rect = canvas.create_rectangle(m[0], m[1], m[2], m[3], fill="orange")
        moving_platforms.append([rect, m[4]])

    for l in lvl["lavas"]:
        lava_areas.append(canvas.create_rectangle(*l, fill="red"))

    finish = canvas.create_rectangle(*lvl["finish"], fill="gold")

    player = canvas.create_rectangle(*lvl["spawn_player"], fill="black")
    princess = canvas.create_rectangle(*lvl["spawn_princess"], fill="pink")

    player_vel = 0
    princess_vel = 0

# ===== AI =====
def princess_ai():
    global princess_vel

    prx1, pry1, prx2, pry2 = canvas.coords(princess)
    px1, _, _, _ = canvas.coords(player)
    fx1, _, _, _ = canvas.coords(finish)

    move = 4 if prx1 < fx1 else -3

    if abs(prx1 - px1) < 120:
        move = 6 if prx1 > px1 else -6

    # lava check
    for lava in lava_areas:
        lx1, ly1, lx2, ly2 = canvas.coords(lava)

        if prx2 + 20 > lx1 and prx1 < lx1 and abs(pry2 - ly1) < 60:
            if princess_on_ground:
                princess_vel = -16
            else:
                move = -move

    return move

# ===== GAME LOOP =====
def game_loop():
    global player_vel, player_on_ground
    global princess_vel, princess_on_ground
    global game_won, game_lost

    if not game_won and not game_lost:

        # PLAYER
        dx = (-7 if left else 0) + (7 if right else 0)
        canvas.move(player, dx, 0)

        if jump and player_on_ground:
            player_vel = -18

        player_vel += gravity
        canvas.move(player, 0, player_vel)

        px1,py1,px2,py2 = canvas.coords(player)
        player_on_ground = False

        for p in platforms:
            if collide(player, p):
                x1,y1,x2,y2 = canvas.coords(p)
                if player_vel > 0:
                    canvas.coords(player, px1, y1-40, px2, y1)
                    player_vel = 0
                    player_on_ground = True

        # lava player
        for l in lava_areas:
            if collide(player, l):
                game_lost = True

        # PRINCESS
        princess_vel += gravity
        canvas.move(princess, 0, princess_vel)

        prx1,pry1,prx2,pry2 = canvas.coords(princess)
        princess_on_ground = False

        for p in platforms:
            if collide(princess, p):
                x1,y1,x2,y2 = canvas.coords(p)
                if princess_vel > 0:
                    canvas.coords(princess, prx1, y1-40, prx2, y1)
                    princess_vel = 0
                    princess_on_ground = True

        move = princess_ai()
        canvas.move(princess, move, 0)

        # lava princess = win
        for l in lava_areas:
            if collide(princess, l):
                game_won = True

        # catch
        if abs(prx1 - px1) < 40:
            game_won = True

    canvas.delete("ui")

    if game_won:
        canvas.create_text(683,300,text="TU UZVARĒJI!",fill="white",font=("Arial",40),tags="ui")

    if game_lost:
        canvas.create_text(683,300,text="TU ZAUDĒJI!",fill="red",font=("Arial",40),tags="ui")

    root.after(20, game_loop)

# ===== START =====
load_level(0)
game_loop()
root.mainloop()