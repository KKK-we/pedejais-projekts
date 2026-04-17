import tkinter as tk

root = tk.Tk()
root.title("Princess and the Black Man")
root.geometry("1366x768")
root.resizable(False, False)

canvas = tk.Canvas(root, width=1366, height=768, bg="#2d2d1a")
canvas.pack()

# =========================
# PLATFORMAS
# =========================
platform_data = [
    # Zeme
    (0, 700, 1366, 768),

    # Kreisā puse
    (0, 580, 180, 620),
    (220, 520, 420, 560),
    (470, 450, 650, 490),

    # Vidus
    (700, 600, 950, 640),
    (850, 500, 1050, 540),
    (600, 380, 800, 420),
    (350, 320, 550, 360),

    # Augšējā daļa
    (150, 220, 350, 260),
    (450, 180, 650, 220),
    (800, 180, 1000, 220),
    (1100, 250, 1280, 290),

    # Labā puse ceļā uz finišu
    (1050, 420, 1200, 460),
    (1180, 340, 1320, 380),
    (1080, 140, 1220, 180),
]

platforms = []

for p in platform_data:
    rect = canvas.create_rectangle(
        p[0], p[1], p[2], p[3],
        fill="#8c7b4f",
        outline="black",
        width=2
    )
    platforms.append(rect)

# =========================
# ŪDENS
# =========================
water_areas = [
   canvas.create_rectangle(180, 680, 320, 700, fill="deepskyblue", outline="blue"),
    canvas.create_rectangle(520, 680, 700, 700, fill="deepskyblue", outline="blue"),
    canvas.create_rectangle(980, 680, 1150, 700, fill="deepskyblue", outline="blue"),
    canvas.create_rectangle(730, 620, 850, 640, fill="deepskyblue", outline="blue"),
]

# =========================
# FINIŠS
# =========================
finish = canvas.create_rectangle(
    1220, 100, 1300, 180,
    fill="gold",
    outline="yellow",
    width=3
)

# =========================
# SPĒLĒTĀJS
# =========================
player = canvas.create_rectangle(
    50, 640, 90, 690,
    fill="black"
)

# =========================
# PRINCESE
# =========================
princess = canvas.create_rectangle(
    120, 640, 160, 690,
    fill="pink"
)

# =========================
# SPĒLĒTĀJA FIZIKA
# =========================
player_speed = 7
slow_speed = 3
player_jump = -18
gravity = 1
player_velocity_y = 0
player_on_ground = False
slow_timer = 0

# =========================
# PRINCESES FIZIKA
# =========================
princess_speed = 2
princess_jump = -16
princess_velocity_y = 0
princess_on_ground = False

# =========================
# TAUSTIŅI
# =========================
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

# =========================
# SADURSMJU FUNKCIJA
# =========================
def check_collision(obj1, obj2):
    x1, y1, x2, y2 = canvas.coords(obj1)
    a1, b1, a2, b2 = canvas.coords(obj2)

    return x1 < a2 and x2 > a1 and y1 < b2 and y2 > b1

# =========================
# SPĒLES CIKLS
# =========================
def game_loop():
    global player_velocity_y
    global player_on_ground
    global slow_timer
    global princess_velocity_y
    global princess_on_ground

    current_speed = slow_speed if slow_timer > 0 else player_speed

    # =========================
    # SPĒLĒTĀJA KUSTĪBA
    # =========================
    if left_pressed:
        canvas.move(player, -current_speed, 0)

    if right_pressed:
        canvas.move(player, current_speed, 0)

    if space_pressed and player_on_ground:
        player_velocity_y = player_jump
        player_on_ground = False

    player_velocity_y += gravity
    canvas.move(player, 0, player_velocity_y)

    player_x1, player_y1, player_x2, player_y2 = canvas.coords(player)

    # Robežas spēlētājam
    if player_x1 < 0:
        canvas.move(player, -player_x1, 0)

    if player_x2 > 1366:
        canvas.move(player, 1366 - player_x2, 0)

    player_on_ground = False

    for platform in platforms:
        plat_x1, plat_y1, plat_x2, plat_y2 = canvas.coords(platform)

        if check_collision(player, platform):
            player_x1, player_y1, player_x2, player_y2 = canvas.coords(player)

            if player_velocity_y > 0 and player_y2 > plat_y1 and player_y1 < plat_y1:
                canvas.coords(
                    player,
                    player_x1,
                    plat_y1 - 50,
                    player_x2,
                    plat_y1
                )
                player_velocity_y = 0
                player_on_ground = True

    # Ja nokrīt zem mapes
    if player_y2 > 768:
        canvas.coords(player, 50, 640, 90, 690)
        player_velocity_y = 0

    # Ūdens palēnina
    for water in water_areas:
        if check_collision(player, water):
            slow_timer = 120

    if slow_timer > 0:
        slow_timer -= 1

    # =========================
    # PRINCESES AI
    # =========================
    princess_velocity_y += gravity
    canvas.move(princess, 0, princess_velocity_y)

    princess_x1, princess_y1, princess_x2, princess_y2 = canvas.coords(princess)
    princess_on_ground = False

    for platform in platforms:
        plat_x1, plat_y1, plat_x2, plat_y2 = canvas.coords(platform)

        if check_collision(princess, platform):
            princess_x1, princess_y1, princess_x2, princess_y2 = canvas.coords(princess)

            if princess_velocity_y > 0 and princess_y2 > plat_y1 and princess_y1 < plat_y1:
                canvas.coords(
                    princess,
                    princess_x1,
                    plat_y1 - 50,
                    princess_x2,
                    plat_y1
                )
                princess_velocity_y = 0
                princess_on_ground = True

    # Kustība uz finišu
    finish_x1, finish_y1, finish_x2, finish_y2 = canvas.coords(finish)

    if princess_x1 < finish_x1:
        canvas.move(princess, princess_speed, 0)

    # Princese lec, ja priekšā ir platforma
    for platform in platforms:
        plat_x1, plat_y1, plat_x2, plat_y2 = canvas.coords(platform)

        if (
            princess_x2 + 20 > plat_x1
            and princess_x1 < plat_x1
            and plat_y1 < princess_y2
            and plat_y1 > princess_y1 - 120
            and princess_on_ground
        ):
            princess_velocity_y = princess_jump
            princess_on_ground = False

    # Ja princese nokrīt zem mapes
    if princess_y2 > 768:
        canvas.coords(princess, 120, 640, 160, 690)
        princess_velocity_y = 0

    # Robežas princesei
    princess_x1, princess_y1, princess_x2, princess_y2 = canvas.coords(princess)

    if princess_x1 < 0:
        canvas.move(princess, -princess_x1, 0)

    if princess_x2 > 1366:
        canvas.move(princess, 1366 - princess_x2, 0)

    # =========================
    # WIN / LOSE
    # =========================
    if check_collision(player, princess):
        canvas.create_text(
            683, 300,
            text="TU UZVARĒJI!",
            fill="white",
            font=("Arial", 40, "bold")
        )
        return

    if check_collision(princess, finish):
        canvas.create_text(
            683, 300,
            text="TU ZAUDĒJI!",
            fill="white",
            font=("Arial", 40, "bold")
        )
        return

    # =========================
    # UI
    # =========================
    canvas.delete("ui")

    canvas.create_text(
        250, 30,
        text="LEFT / RIGHT = kustība | SPACE = lēciens",
        fill="white",
        font=("Arial", 16),
        tags="ui"
    )

    if slow_timer > 0:
        canvas.create_text(
            260, 60,
            text="Tu esi palēnināts, jo iekriti ūdenī!",
            fill="red",
            font=("Arial", 16),
            tags="ui"
        )

    root.after(20, game_loop)

game_loop()
root.mainloop()