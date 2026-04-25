import tkinter as tk

root = tk.Tk()
root.title("Princess and the Black Man")
root.geometry("1366x768")
root.resizable(False, False)

canvas = tk.Canvas(root, width=1366, height=768, bg="#1f1f1f")
canvas.pack()

current_level = 0
game_won = False
game_lost = False

# ================= MAPES (Fireboy stilā) =================
levels = [

# ===== LEVEL 1 =====
{
    "spawn_player": (50, 650, 90, 700),
    "spawn_princess": (120, 650, 160, 700),

    "platforms": [
        (0,700,1366,768),

        # apakša
        (0,600,400,630),
        (450,600,900,630),
        (950,600,1366,630),

        # vidus
        (200,480,600,510),
        (700,480,1100,510),

        # augša
        (100,350,400,380),
        (500,350,900,380),
        (1000,350,1300,380),

        # finiša platforma
        (1100,200,1350,230)
    ],

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
    "spawn_player": (50, 650, 90, 700),
    "spawn_princess": (120, 650, 160, 700),

    "platforms":[
        (0,700,1366,768),

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

# ===== LEVEL 3 (GRŪTS) =====
{
    "spawn_player": (50, 650, 90, 700),
    "spawn_princess": (120, 650, 160, 700),

    "platforms":[
        (0,700,1366,768),

        # apakša
        (0,630,300,660),
        (350,630,700,660),
        (750,630,1100,660),
        (1150,630,1366,660),

        # šauri lēcieni
        (200,520,260,550),
        (350,480,420,510),
        (500,440,570,470),
        (650,400,720,430),
        (800,360,870,390),
        (950,320,1020,350),

        # augšējā daļa
        (200,250,500,280),
        (600,200,900,230),
        (1000,160,1300,190)
    ],

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


platforms = []
water_areas = []
lava_areas = []

player = None
princess = None
finish = None

player_speed = 7
slow_speed = 1
gravity = 1
player_jump = -18
player_velocity_y = 0
player_on_ground = False
slow_timer = 0

princess_speed = 4
princess_jump = -16
princess_velocity_y = 0
princess_on_ground = False

left_pressed = False
right_pressed = False
space_pressed = False

def key_press(event):
    global left_pressed, right_pressed, space_pressed

    if event.keysym == "Left":
        left_pressed = True

    if event.keysym == "Right":
        right_pressed = True

    if event.keysym == "space":
        space_pressed = True

    if game_won and event.keysym == "Return":
        next_level()

def key_release(event):
    global left_pressed, right_pressed, space_pressed

    if event.keysym == "Left":
        left_pressed = False

    if event.keysym == "Right":
        right_pressed = False

    if event.keysym == "space":
        space_pressed = False

root.bind("<KeyPress>", key_press)
root.bind("<KeyRelease>", key_release)

def check_collision(obj1, obj2):
    x1, y1, x2, y2 = canvas.coords(obj1)
    a1, b1, a2, b2 = canvas.coords(obj2)

    return x1 < a2 and x2 > a1 and y1 < b2 and y2 > b1

def load_level(index):
    global platforms, water_areas, lava_areas
    global player, princess, finish
    global princess_speed
    global player_velocity_y, princess_velocity_y
    global player_on_ground, princess_on_ground
    global slow_timer, game_won, game_lost

    canvas.delete("all")

    platforms = []
    water_areas = []
    lava_areas = []

    game_won = False
    game_lost = False

    player_velocity_y = 0
    princess_velocity_y = 0
    player_on_ground = False
    princess_on_ground = False
    slow_timer = 0

    level = levels[index]

    for p in level["platforms"]:
        platforms.append(
            canvas.create_rectangle(
                p[0], p[1], p[2], p[3],
                fill="#8c7b4f",
                outline="black",
                width=2
            )
        )

    for w in level["waters"]:
        water_areas.append(
            canvas.create_rectangle(
                w[0], w[1], w[2], w[3],
                fill="deepskyblue",
                outline="blue",
                width=2
            )
        )

    for l in level["lavas"]:
        lava_areas.append(
            canvas.create_rectangle(
                l[0], l[1], l[2], l[3],
                fill="red",
                outline="darkred",
                width=2
            )
        )

    f = level["finish"]
    finish = canvas.create_rectangle(
        f[0], f[1], f[2], f[3],
        fill="gold",
        outline="yellow",
        width=3
    )

    player = canvas.create_rectangle(50, 640, 90, 690, fill="black")
    princess = canvas.create_rectangle(120, 640, 160, 690, fill="pink")

    princess_speed = level["princess_speed"]

def next_level():
    global current_level

    current_level += 1

    if current_level >= len(levels):
        canvas.delete("all")
        canvas.create_text(
            683, 300,
            text="TU PABEIDZI VISUS LĪMEŅUS!",
            fill="white",
            font=("Arial", 40, "bold")
        )
        return

    load_level(current_level)

def princess_touching_lava():
    for lava in lava_areas:
        if check_collision(princess, lava):
            return True
    return False

def game_loop():
    global player_velocity_y, player_on_ground
    global princess_velocity_y, princess_on_ground
    global slow_timer, game_won, game_lost

    if not game_won and not game_lost:

        current_speed = slow_speed if slow_timer > 0 else player_speed

        move_x = 0

        if left_pressed:
            move_x -= current_speed

        if right_pressed:
            move_x += current_speed

        canvas.move(player, move_x, 0)

        px1, py1, px2, py2 = canvas.coords(player)

        if px1 < 0:
            canvas.move(player, -px1, 0)

        if px2 > 1366:
            canvas.move(player, 1366 - px2, 0)

        for platform in platforms:
            if check_collision(player, platform):
                bx1, by1, bx2, by2 = canvas.coords(platform)

                if move_x > 0:
                    canvas.coords(player, bx1 - 40, py1, bx1, py2)

                if move_x < 0:
                    canvas.coords(player, bx2, py1, bx2 + 40, py2)

        if space_pressed and player_on_ground:
            player_velocity_y = player_jump
            player_on_ground = False

        player_velocity_y += gravity
        canvas.move(player, 0, player_velocity_y)

        px1, py1, px2, py2 = canvas.coords(player)
        player_on_ground = False

        for platform in platforms:
            bx1, by1, bx2, by2 = canvas.coords(platform)

            if check_collision(player, platform):

                if player_velocity_y > 0 and py2 > by1 and py1 < by1:
                    canvas.coords(player, px1, by1 - 50, px2, by1)
                    player_velocity_y = 0
                    player_on_ground = True

                elif player_velocity_y < 0 and py1 < by2 and py2 > by2:
                    canvas.coords(player, px1, by2, px2, by2 + 50)
                    player_velocity_y = 3

        for water in water_areas:
            if check_collision(player, water):
                slow_timer = 300

        if slow_timer > 0:
            slow_timer -= 1

        for lava in lava_areas:
            if check_collision(player, lava):
                game_lost = True

        princess_velocity_y += gravity
        canvas.move(princess, 0, princess_velocity_y)

        prx1, pry1, prx2, pry2 = canvas.coords(princess)
        princess_on_ground = False

        for platform in platforms:
            bx1, by1, bx2, by2 = canvas.coords(platform)

            if check_collision(princess, platform):
                if princess_velocity_y > 0 and pry2 > by1 and pry1 < by1:
                    canvas.coords(princess, prx1, by1 - 50, prx2, by1)
                    princess_velocity_y = 0
                    princess_on_ground = True

                elif princess_velocity_y < 0 and pry1 < by2 and pry2 > by2:
                    canvas.coords(princess, prx1, by2, prx2, by2 + 50)
                    princess_velocity_y = 2

        px1, py1, px2, py2 = canvas.coords(player)
        fx1, fy1, fx2, fy2 = canvas.coords(finish)

        princess_move = princess_speed

        if abs(prx1 - px1) < 140:
            if prx1 > px1:
                princess_move = princess_speed + 2
            else:
                princess_move = -(princess_speed + 1)
        else:
            if prx1 < fx1:
                princess_move = princess_speed
            else:
                princess_move = -1

        canvas.move(princess, princess_move, 0)

        prx1, pry1, prx2, pry2 = canvas.coords(princess)

        if prx1 < 0:
            canvas.move(princess, -prx1, 0)

        if prx2 > 1366:
            canvas.move(princess, 1366 - prx2, 0)

        # Princess avoids lava
        for lava in lava_areas:
            lx1, ly1, lx2, ly2 = canvas.coords(lava)

            if (
                prx2 + 20 > lx1
                and prx1 < lx1
                and abs(pry2 - ly1) < 80
            ):
                if princess_on_ground:
                    princess_velocity_y = princess_jump

            if check_collision(princess, lava):
                canvas.move(princess, -40, -20)
                princess_velocity_y = princess_jump

        # Princess jumps on platforms
        for platform in platforms:
            bx1, by1, bx2, by2 = canvas.coords(platform)

            if (
                prx2 + 25 > bx1
                and prx1 < bx1
                and by1 < pry2
                and by1 > pry1 - 140
                and princess_on_ground
            ):
                princess_velocity_y = princess_jump
                princess_on_ground = False

        if check_collision(princess, finish):
            game_lost = True

        if abs(prx1 - px1) < 35 and abs(pry1 - py1) < 35:
            game_won = True

    canvas.delete("ui")

    canvas.create_text(
        250, 30,
        text=f"Līmenis {current_level + 1} | LEFT / RIGHT | SPACE",
        fill="white",
        font=("Arial", 16),
        tags="ui"
    )

    if slow_timer > 0:
        canvas.create_text(
            330, 60,
            text="Ūdens tevi palēnina uz 5 sekundēm!",
            fill="deepskyblue",
            font=("Arial", 16),
            tags="ui"
        )

    if game_won:
        canvas.create_text(
            683, 300,
            text="TU NOĶĒRI PRINCESI!",
            fill="white",
            font=("Arial", 35, "bold"),
            tags="ui"
        )

        canvas.create_text(
            683, 350,
            text="Nospied ENTER nākamajam līmenim",
            fill="yellow",
            font=("Arial", 20),
            tags="ui"
        )

    if game_lost:
        canvas.create_text(
            683, 300,
            text="TU ZAUDĒJI!",
            fill="red",
            font=("Arial", 40, "bold"),
            tags="ui"
        )

    root.after(20, game_loop)

load_level(current_level)
game_loop()
root.mainloop()