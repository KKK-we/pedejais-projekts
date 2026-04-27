import tkinter as tk

root = tk.Tk()
root.title("Princess and the Black Man")
root.geometry("1366x768")
root.resizable(False, False)

canvas = tk.Canvas(root, width=1366, height=768, bg="#1f1f1f")
canvas.pack()

# ================== STATE ==================
current_level = 0
game_won = False
game_lost = False
restart_timer = 0

# ================== LEVELS ==================
levels = [

# LEVEL 1
{
    "spawn_player": (50,650,90,690),
    "spawn_princess": (140,650,180,690),

    "platforms":[
        (0,700,1366,768),
        (0,600,300,630),
        (400,600,700,630),
        (800,600,1100,630),

        (200,450,400,480),
        (600,450,800,480),

        (300,300,500,330),
        (700,300,900,330),

        (1000,200,1300,230)
    ],

    "waters":[
        (220,440,380,450),
    ],

    "lavas":[
        (450,690,700,700)
    ],

    "finish":(1100,150,1200,200),
    "princess_speed":4
},

# LEVEL 2
{
    "spawn_player": (50,650,90,690),
    "spawn_princess": (140,650,180,690),

    "platforms":[
        (0,700,1366,768),

        (0,620,250,650),
        (350,580,600,610),
        (700,540,950,570),
        (1000,500,1250,530),

        (200,420,450,450),
        (650,380,900,410),

        (300,250,550,280),
        (700,200,1000,230)
    ],

    "waters":[
        (370,570,580,580),
    ],

    "lavas":[
        (200,690,600,700),
        (800,690,1200,700)
    ],

    "finish":(1050,150,1200,200),
    "princess_speed":5
},

# LEVEL 3
{
    "spawn_player": (50,650,90,690),
    "spawn_princess": (140,650,180,690),

    "platforms":[
        (0,700,1366,768),

        (0,620,300,650),
        (400,620,700,650),
        (800,620,1100,650),

        (250,500,350,530),
        (500,450,600,480),
        (750,400,850,430),

        (300,300,500,330),
        (650,250,900,280),

        (1000,180,1300,210)
    ],

    "waters":[
        (260,490,340,500),
        (760,390,840,400)
    ],

    "lavas":[
        (300,690,700,700)
    ],

    "finish":(1100,120,1250,170),
    "princess_speed":6
},

# LEVEL 4 - FLOOR IS LAVA
{
    "spawn_player": (50,200,90,240),
    "spawn_princess": (140,200,180,240),

    "platforms":[
        (100,300,250,330),
        (350,260,500,290),
        (600,220,750,250),
        (850,260,1000,290),
        (1050,200,1250,230)
    ],

    "waters":[],

    "lavas":[
        (0,700,1366,768)
    ],

    "finish":(1150,150,1300,200),
    "princess_speed":7
}
]

# ================== OBJECTS ==================
platforms=[]
water_areas=[]
lava_areas=[]

player=None
princess=None
finish=None

# ================== PHYSICS ==================
gravity=1
player_vel=0
player_on_ground=False

princess_vel=0
princess_on_ground=False

player_speed=7
slow_timer=0

# ================== INPUT ==================
left=False
right=False
jump=False

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

# ================== UTILS ==================
def collide(a,b):
    x1,y1,x2,y2 = canvas.coords(a)
    a1,b1,a2,b2 = canvas.coords(b)
    return x1<a2 and x2>a1 and y1<b2 and y2>b1

# ================== LOAD ==================
def load_level(i):
    global platforms,water_areas,lava_areas
    global player,princess,finish
    global player_vel,princess_vel
    global game_won,game_lost,slow_timer

    canvas.delete("all")

    platforms=[]
    water_areas=[]
    lava_areas=[]

    level = levels[i]

    for p in level["platforms"]:
        platforms.append(canvas.create_rectangle(*p,fill="#8c7b4f"))

    for w in level["waters"]:
        water_areas.append(canvas.create_rectangle(*w,fill="blue"))

    for l in level["lavas"]:
        lava_areas.append(canvas.create_rectangle(*l,fill="red"))

    finish = canvas.create_rectangle(*level["finish"],fill="gold")

    player = canvas.create_rectangle(*level["spawn_player"],fill="black")
    princess = canvas.create_rectangle(*level["spawn_princess"],fill="pink")

    player_vel=0
    princess_vel=0

    game_won=False
    game_lost=False
    slow_timer=0

# ================== RESET ==================
def reset_game():
    global current_level
    current_level=0
    load_level(current_level)

# ================== LOOP ==================
def game_loop():
    global player_vel,player_on_ground
    global princess_vel,princess_on_ground
    global game_won,game_lost,restart_timer
    global current_level, slow_timer

    if game_lost:
        restart_timer -= 1
        canvas.delete("ui")
        canvas.create_text(683,300,text=f"ZAUDĒJI! Restart pēc {restart_timer//50}s",
                           fill="red",font=("Arial",30),tags="ui")

        if restart_timer <= 0:
            reset_game()

        root.after(20,game_loop)
        return

    if not game_won:

        # ===== PLAYER =====
        speed = 2 if slow_timer>0 else player_speed
        dx = (-speed if left else 0) + (speed if right else 0)

        canvas.move(player,dx,0)

        if jump and player_on_ground:
            player_vel = -18

        player_vel += gravity
        canvas.move(player,0,player_vel)

        px1,py1,px2,py2 = canvas.coords(player)
        player_on_ground=False

        for p in platforms:
            if collide(player,p):
                x1,y1,x2,y2 = canvas.coords(p)
                if player_vel>0:
                    canvas.coords(player,px1,y1-40,px2,y1)
                    player_vel=0
                    player_on_ground=True

        for w in water_areas:
            if collide(player,w):
                slow_timer=250

        if slow_timer>0:
            slow_timer-=1

        for l in lava_areas:
            if collide(player,l):
                game_lost=True
                restart_timer=250

        # ===== PRINCESS =====
        princess_vel += gravity
        canvas.move(princess,0,princess_vel)

        prx1,pry1,prx2,pry2 = canvas.coords(princess)
        princess_on_ground=False

        for p in platforms:
            if collide(princess,p):
                x1,y1,x2,y2 = canvas.coords(p)
                if princess_vel>0:
                    canvas.coords(princess,prx1,y1-40,prx2,y1)
                    princess_vel=0
                    princess_on_ground=True

        px1,py1,px2,py2 = canvas.coords(player)
        fx1,fy1,fx2,fy2 = canvas.coords(finish)

        # virziens
        if abs(prx1-px1) < 120:
            move = 6 if prx1 > px1 else -6
        else:
            move = 5 if prx1 < fx1 else -3

        # lava detection
        danger=False
        for lava in lava_areas:
            lx1,ly1,lx2,ly2 = canvas.coords(lava)

            if prx2+20 > lx1 and prx1 < lx1 and abs(pry2-ly1)<80:
                danger=True

        # reakcija
        if danger and princess_on_ground:
            princess_vel = -16
        elif danger:
            move = -move

        canvas.move(princess,move,0)

        # lava princese = win
        for l in lava_areas:
            if collide(princess,l):
                game_won=True

        # win / lose
        if abs(prx1-px1)<40:
            game_won=True

        if collide(princess,finish):
            game_lost=True
            restart_timer=250

    else:
        current_level+=1
        if current_level>=len(levels):
            canvas.delete("all")
            canvas.create_text(683,300,text="TU UZVARĒJI VISU SPĒLI!",
                               fill="white",font=("Arial",40))
            return
        load_level(current_level)

    root.after(20,game_loop)

# ================== START ==================
load_level(current_level)
game_loop()
root.mainloop()