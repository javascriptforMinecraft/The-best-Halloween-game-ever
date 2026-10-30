#Modules required
from PIL import Image
from pathlib import Path
import sys
import os
import random
import pygame

#Initialisation
pygame.init()
pygame.font.init()
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "Assets"
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
pygame.mixer.set_num_channels(32)

#Loading fonts and text objects
font = pygame.font.SysFont("Retro Pixel", 30)
instruction_jump = font.render("W to jump", False, (255, 255, 255))
instruction_jump_rect = instruction_jump.get_rect(topleft = (200, 300))
instruction_move = font.render("A/D to move left/right", False, (255, 255, 255))
instruction_move_rect = instruction_move.get_rect(topleft = (200, 330))
instruction_crouch = font.render("S to crouch", False, (255, 255, 255))
instruction_crouch_rect = instruction_crouch.get_rect(topleft = (200, 360))
instruction_interact = font.render("F to interact with things", False, (255, 255, 255))
instruction_interact_rect = instruction_interact.get_rect(topleft = (200, 390))

#Loading background function
def load_background(image_path, screen_size):
    try:
        img = Image.open(image_path).convert("RGBA")
        img = img.resize(screen_size, Image.LANCZOS)
        img_bytes = img.tobytes()
        surface = pygame.image.frombuffer(img_bytes, img.size, "RGBA").copy()
        return surface
    except Exception as e:
        print(f"Error loading background: {e}")
        sys.exit(1)

#Loading backgrounds
outside = load_background(ASSETS_DIR / "Art" / "Backgrounds" / "Outside.png", screen_size)
stormy_outside = load_background(ASSETS_DIR / "Art" / "Backgrounds" / "Stormy.png", screen_size)
lightning1 = load_background(ASSETS_DIR / "Art" / "Backgrounds" / "Lightning1.png", screen_size)
lightning2 = load_background(ASSETS_DIR / "Art" / "Backgrounds" / "Lightning2.png", screen_size)
lightning3 = load_background(ASSETS_DIR / "Art" / "Backgrounds" / "Lightning3.png", screen_size)
lightning4 = load_background(ASSETS_DIR / "Art" / "Backgrounds" / "Lightning4.png", screen_size)
lightning5 = load_background(ASSETS_DIR / "Art" / "Backgrounds" / "Lightning5.png", screen_size)
lightning6 = load_background(ASSETS_DIR / "Art" / "Backgrounds" / "Lightning6.png", screen_size)
creepy_house = load_background(ASSETS_DIR / "Art" / "Backgrounds" / "Creepy House.png", screen_size)

#Art
def load_art(art):
    try:
        return pygame.image.load(art)
    except Exception as e:
        print(f"Error: Could not load '{art}'. {e}")
        pygame.quit()
        sys.exit()

#Loading art
crate = load_art(ASSETS_DIR / "Art" / "Objects" / "Crate.png")
not_pressed_button_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Button (not pressed).png")
not_pressed_button_art = pygame.transform.rotate(not_pressed_button_art, 90)
pressed_button_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Button (pressed).png")
pressed_button_art = pygame.transform.rotate(pressed_button_art, 90)
passable_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Passable crate.png")
balcony_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Balcony.png")
door_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Door.png")
fireplace_closed_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Fireplace closed.png")
fireplace_open_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Fireplace open.png")
fireplace_with_coal_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Fireplace with coal.png")
fireplace_lit_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Fireplace lit.png")
fireplace_chimney_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Fireplace chimney.png")
chair_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Chair.png")
other_chair_art = pygame.transform.flip(chair_art, True, False)
floorboard_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Floorboard.png")
dining_table_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Dining table.png")
stove_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Stove.png")
cupboard_closed_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Cupboard closed.png")
cupboard_open_art = load_art(ASSETS_DIR / "Art" / "Objects" / "Cupboard open.png")

#Loading player models
bob_art = load_art(ASSETS_DIR / "Art" / "BOB" / "BOB.png")
crouching_art = load_art(ASSETS_DIR / "Art" / "BOB" / "BOB_crouch.png")

#SFX
jump_sfx = pygame.mixer.Sound(ASSETS_DIR / "SFX" / "Jump.mp3")
landing_sfx = pygame.mixer.Sound(ASSETS_DIR / "SFX" / "Landing.mp3")
raining_sfx = pygame.mixer.Sound(ASSETS_DIR / "SFX" / "Raining.mp3")
click_sfx = pygame.mixer.Sound(ASSETS_DIR / "SFX" / "Button clicked.mp3")
thunder_sfx = pygame.mixer.Sound(ASSETS_DIR / "SFX" / "Thunder.mp3")
balcony_creaking_sfx = pygame.mixer.Sound(ASSETS_DIR / "SFX" / "Balcony creaking.mp3")
creaking_channel = pygame.mixer.Channel(1)
walking_grass = pygame.mixer.Sound(ASSETS_DIR / "SFX" / "Walking on grass.mp3")
landing_grass = pygame.mixer.Sound(ASSETS_DIR / "SFX" / "Landing on grass.mp3")
walking_wood = pygame.mixer.Sound(ASSETS_DIR / "SFX" / "Walking on wood.mp3")

#Objects
darkness = pygame.Surface((800, 600))
darkness.fill((0, 0, 0))
darkness.set_alpha(100)


wall0 = [
    pygame.Rect(2000, 0, 100, 100),
    pygame.Rect(2000, 100, 100, 100),
    pygame.Rect(2000, 200, 100, 100),
    pygame.Rect(2000, 300, 100, 100),
    pygame.Rect(2000, 400, 100, 100)
]
button = pygame.Rect(1300, 413, 40, 74)
passable_gameplay = [
    pygame.Rect(2200, 400, 100, 20),
    pygame.Rect(2200, 300, 100, 20)
]
gameplay = [
    pygame.Rect(800, 200, 100, 100),
    pygame.Rect(900, 200, 100, 100),
    pygame.Rect(700, 300, 100, 100),
    pygame.Rect(800, 300, 100, 100),
    pygame.Rect(900, 300, 100, 100),
    pygame.Rect(600, 400, 100, 100),
    pygame.Rect(700, 400, 100, 100),
    pygame.Rect(800, 400, 100, 100),
    pygame.Rect(900, 400, 100, 100),

    pygame.Rect(1200, 400, 100, 100),
    pygame.Rect(1200, 300, 100, 100),
    pygame.Rect(1300, 300, 100, 100),
    pygame.Rect(1400, 300, 100, 100),
    pygame.Rect(1500, 300, 100, 100),
    pygame.Rect(1600, 300, 100, 100),
    pygame.Rect(1700, 300, 100, 100), 
    pygame.Rect(1500, 150, 100, 100), 
    pygame.Rect(1600, 150, 100, 100),
    pygame.Rect(1700, 150, 100, 100),
    pygame.Rect(1700, 50, 100, 100),
    pygame.Rect(1700, -50, 100, 100),

    pygame.Rect(2300, 200, 100, 100),
    pygame.Rect(2400, 200, 100, 100),
    pygame.Rect(2500, 200, 100, 100),
    pygame.Rect(2600, 200, 100, 100),
    pygame.Rect(2300, 300, 100, 100),
    pygame.Rect(2400, 300, 100, 100),
    pygame.Rect(2500, 300, 100, 100),
    pygame.Rect(2600, 300, 100, 100),
    pygame.Rect(2300, 400, 100, 100),
    pygame.Rect(2400, 400, 100, 100),
    pygame.Rect(2500, 400, 100, 100),
    pygame.Rect(2600, 400, 100, 100),

]
gameplay.extend(wall0)

entrance = [
    pygame.Rect(4000, 0, 100, 100),
    pygame.Rect(4000, 100, 100, 100),
    pygame.Rect(4000, 200, 100, 100),
]
door = pygame.Rect(4000, 300, 100, 200)
balcony = [
    pygame.Rect(3800, 200, 100, 100),
    pygame.Rect(3900, 200, 100, 100)
]
floor = [
    pygame.Rect(0, 500, 100, 100),
    pygame.Rect(100, 500, 100, 100),
    pygame.Rect(200, 500, 100, 100),
    pygame.Rect(300, 500, 100, 100),
    pygame.Rect(400, 500, 100, 100),
    pygame.Rect(500, 500, 100, 100),
    pygame.Rect(600, 500, 100, 100),
    pygame.Rect(700, 500, 100, 100),
    pygame.Rect(800, 500, 100, 100),
    pygame.Rect(900, 500, 100, 100),
    pygame.Rect(1000, 500, 100, 100),
    pygame.Rect(1100, 500, 100, 100),
    pygame.Rect(1200, 500, 100, 100),
    pygame.Rect(1300, 500, 100, 100),
    pygame.Rect(1400, 500, 100, 100),
    pygame.Rect(1500, 500, 100, 100),
    pygame.Rect(1600, 500, 100, 100),
    pygame.Rect(1700, 500, 100, 100),
    pygame.Rect(1800, 500, 100, 100),
    pygame.Rect(1900, 500, 100, 100),
    pygame.Rect(2000, 500, 100, 100),
    pygame.Rect(2100, 500, 100, 100),
    pygame.Rect(2300, 500, 100, 100),
]
ceiling = [
    pygame.Rect(0, 0, 100, 100),
    pygame.Rect(100, 0, 100, 100),
    pygame.Rect(200, 0, 100, 100),
    pygame.Rect(300, 0, 100, 100),
    pygame.Rect(400, 0, 100, 100),
    pygame.Rect(500, 0, 100, 100),
    pygame.Rect(600, 0, 100, 100),
    pygame.Rect(700, 0, 100, 100),
    pygame.Rect(800, 0, 100, 100),
    pygame.Rect(900, 0, 100, 100),
    pygame.Rect(1000, 0, 100, 100),
    pygame.Rect(1100, 0, 100, 100),
    pygame.Rect(1200, 0, 100, 100),
    pygame.Rect(1300, 0, 100, 100),
    pygame.Rect(1400, 0, 100, 100),
    pygame.Rect(1500, 0, 100, 100),
    pygame.Rect(1600, 0, 100, 100),
    pygame.Rect(1700, 0, 100, 100),
    pygame.Rect(1800, 0, 100, 100),
    pygame.Rect(1900, 0, 100, 100),
    pygame.Rect(2000, 0, 100, 100),
    pygame.Rect(2100, 0, 100, 100),
    pygame.Rect(2300, 0, 100, 100),
]
fireplace = pygame.Rect(3600, 400, 100, 100)
fireplace_chimney = [
    pygame.Rect(3640, 300, 20, 100),
    pygame.Rect(3640, 200, 20, 100),
    pygame.Rect(3640, 100, 20, 100),
    pygame.Rect(3640, 0, 20, 100)
]
chair = [
    pygame.Rect(3450, 300, 100, 200),
    pygame.Rect(4300, 300, 100, 200)
]
other_chair = [
    pygame.Rect(3750, 300, 100, 200),
    pygame.Rect(4600, 300, 100, 200)
]
dining_table = pygame.Rect(4375, 400, 150, 100)
cupboards = [
    pygame.Rect(5100, 300, 100, 200),
    pygame.Rect(5100, 100, 100, 100)
]
stove = pygame.Rect(5000, 400, 100, 100)
house = [fireplace, dining_table]
house.extend(fireplace_chimney + chair + other_chair + floor + cupboards)

raining_area = pygame.Rect(3000, 0, 10, 600)
camera_change = pygame.Rect(3670, 0, 10, 600)
transition_rect = pygame.Rect(4200, 0, 10, 600)
house_wall_left = pygame.Rect(4500, -600, 10, 1200)
house_wall_right = pygame.Rect(5000, -600, 10, 1200)
move_left_in_house = pygame.Rect(4500, 0, 10, 600)
move_right_in_house = pygame.Rect(5300, 0, 10, 600)

house.append(house_wall_left)
house.append(house_wall_right)

#BOB
bob = pygame.Rect(300, 400, 100, 100)
normal_hitbox_height = 100
crouch_hitbox_height = 50
hitbox_width = 75
bobs_hitbox = pygame.Rect(bob.left, bob.bottom - normal_hitbox_height, hitbox_width, normal_hitbox_height)
isCrouching = False
on_ground = False
jump_speed = 15
gravity = 0.8
velocity_y = 0
house.append(bob)
house.append(bobs_hitbox)

#Pre-main loop variables
running = True
isRaining = False
rain = []
for k in range(150):
    x = random.randint(0, screen_size[0])
    y = random.randint(0, 100)
    speed = random.randint(8, 15)
    length = random.randint(8, 18)
    rain.append([x, y, speed, length])
clicked = False
remainder_time = pygame.time.get_ticks() + 5000
lightning_duration = 200
lightning_active = False
lightning_end_time = 0
camera_locked = False
transitioning = False
balcony_falling = False
balcony_fall_distance = 0
balcony_fell = False
creaking_played = False
walking_channel = walking_grass.play()
inHouse = False
isStart_of_fadeSet = False
has_bob_moved_after_transition = False
inventory = []
fireplace_state = "Closed"
current_fireplace_art = fireplace_closed_art

#Main loop
while running:
    #If game is quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #Interactions
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:

                #Button interaction
                if bobs_hitbox.colliderect(button) == True and clicked == False:
                    for rect in wall0:
                        if rect in gameplay:
                            gameplay.remove(rect)
                    wall0.clear()
                    not_pressed_button_art = pressed_button_art
                    click_sfx.play()
                    clicked = True

                #Fireplace interaction
                if bobs_hitbox.colliderect(fireplace) == True:
                    if "Lighter" in inventory and fireplace_state == "Contains Coal":
                        current_fireplace_art = fireplace_lit_art
                        fireplace_state = "Lit"
                    elif "Coal" in inventory and fireplace_state == "Open":
                        current_fireplace_art = fireplace_with_coal_art
                        fireplace_state = "Contains Coal"
                    elif fireplace_state == "Open":
                        current_fireplace_art = fireplace_closed_art
                        fireplace_state = "Closed"
                    else:
                        current_fireplace_art = fireplace_open_art
                        fireplace_state = "Open"

    #Alpha fade function
    def alpha_fade(surface, current_alpha, target_alpha, fade_speed):
        if current_alpha < target_alpha:
            current_alpha = min(
                current_alpha + fade_speed,
                target_alpha
            )
        elif current_alpha > target_alpha:
            current_alpha = max(
                current_alpha - fade_speed,
                target_alpha
        )
        surface.set_alpha(int(current_alpha))
        return current_alpha

    #Detects which key was pressed
    key = pygame.key.get_pressed()

    #Draw background
    screen.blit(outside, (0, 0))

    #Crouch logic
    crouch_request = key[pygame.K_s] and on_ground
    if crouch_request == True:
        isCrouching = True
    else:
        standing_box = bobs_hitbox.copy()
        standing_box = bobs_hitbox.copy()
        standing_box.height = normal_hitbox_height
        standing_box.bottom = bobs_hitbox.bottom
        blocked_above = any(
            standing_box.colliderect(rect)
            for rect in gameplay
        )
        if not blocked_above:
            isCrouching = False
    old_bottom = bobs_hitbox.bottom
    if isCrouching == True:
        bobs_hitbox.height = crouch_hitbox_height
    else:
        bobs_hitbox.height = normal_hitbox_height
    bobs_hitbox.bottom = old_bottom

    #Object interactions
    if bobs_hitbox.colliderect(camera_change) == True:
        camera_locked = True
    if bobs_hitbox.colliderect(transition_rect) == True:
        transitioning = True
        walking_channel.stop()
        if creaking_played == False:
            creaking_played = True
            creaking_channel.play(balcony_creaking_sfx)
        if creaking_channel.get_busy() == False:
            balcony_falling = True
        if balcony_fell == True:
            alpha_fade(darkness, darkness.get_alpha(), 255, 4)
            if isStart_of_fadeSet == False:
                start_of_fade = pygame.time.get_ticks()
                isStart_of_fadeSet = True
            if pygame.time.get_ticks() - start_of_fade >= 3000:
                inHouse = True
                fireplace.topleft = (400, 400)
                chair[0].topleft = (250, 300)
                chair[1].topleft = (1050, 300)
                other_chair[0].topleft = (550, 300)
                other_chair[1].topleft = (1400, 300)
                dining_table.topleft = (1175, 400)
                cupboards[0].topleft = (2300, 300)
                cupboards[1].topleft = (2300, 100)
                stove.topleft = (1600, 400)
                move_left_in_house.topleft = (-100, 0)
                move_right_in_house.topleft = (890, 0)
                house_wall_left.topleft = (-10, -600)
                for k in range(len(fireplace_chimney)):
                    fireplace_chimney[k].topleft = (440, 312 - 100*k)
                alpha_fade(darkness, darkness.get_alpha(), 0, 40)
                transitioning = False
                entrance.clear()
                balcony.clear()

    #Left-Right movement
    scroll_x = 0
    if transitioning == False:
        if key[pygame.K_a] == True:
            scroll_x = 5
        elif key[pygame.K_d] == True:
            scroll_x = -5
        isMoving = (key[pygame.K_a] or key[pygame.K_d]) and not transitioning
        if isMoving == True:
            if bobs_hitbox.bottom >= screen_size[1] - 100 and inHouse == False:
                sound_to_play = walking_grass
            else:
                sound_to_play = walking_wood
            if walking_channel.get_sound() != sound_to_play:
                walking_channel.stop()
                walking_channel = sound_to_play.play(-1)
            elif not walking_channel.get_busy():
                walking_channel = sound_to_play.play(-1)
            else:
                walking_channel.unpause()
        else:
            walking_channel.pause()
        if scroll_x != 0:
            if camera_locked == True:
                future_hitbox = bobs_hitbox.move(-scroll_x, 0)
                if not any(future_hitbox.colliderect(rect) for rect in gameplay + balcony + entrance + cupboards + [dining_table] + [house_wall_right] + [house_wall_left]):
                    bobs_hitbox.x -= scroll_x
                if bobs_hitbox.colliderect(move_left_in_house) == True:
                    for rect in house:
                        rect.move_ip(800, 0)
                elif bobs_hitbox.colliderect(move_right_in_house) == True:
                    for rect in house:
                        rect.move_ip(-800, 0)
            else:
                can_scroll = True
                for rect in gameplay:
                    future_rect = rect.move(scroll_x, 0)
                    if bobs_hitbox.colliderect(future_rect) == True:
                        can_scroll = False
                        break
                if can_scroll == True:

                    for rect in gameplay + [button] + passable_gameplay + entrance + balcony + [raining_area] + [door] + [camera_change] + [transition_rect]:
                        rect.move_ip(scroll_x, 0)
                    instruction_jump_rect.x += scroll_x
                    instruction_move_rect.x += scroll_x
                    instruction_crouch_rect.x += scroll_x
                    instruction_interact_rect.x += scroll_x

    #Jump mechanic
    was_on_ground = on_ground
    if key[pygame.K_w] == True and on_ground == True and isCrouching == False and transitioning == False:
        velocity_y = -jump_speed
        on_ground = False
        jump_sfx.play()

    #Gravity
    previous = bobs_hitbox.copy()
    velocity_y += gravity
    bobs_hitbox.y += round(velocity_y)
    on_ground = False
    for rect in gameplay + balcony + floor + [dining_table]:
        if bobs_hitbox.colliderect(rect) == False:
            continue
        if velocity_y >= 0 and previous.bottom <= rect.top:
            bobs_hitbox.bottom = rect.top
            velocity_y = 0
            on_ground = True
        elif velocity_y < 0 and previous.top >= rect.bottom:
            bobs_hitbox.top = rect.bottom
            velocity_y = 0
    for rect in passable_gameplay:
        if (velocity_y >= 0 and previous.bottom <= rect.top and bobs_hitbox.bottom >= rect.top and bobs_hitbox.right > rect.left and bobs_hitbox.left < rect.right):
            bobs_hitbox.bottom = rect.top
            velocity_y = 0
            on_ground = True
    if bobs_hitbox.bottom >= screen_size[1] - 100 and inHouse == False:
        bobs_hitbox.bottom = screen_size[1] - 100
        velocity_y = 0
        on_ground = True
    if on_ground == True and was_on_ground == False:
        landing_sfx.play()
    bob.midbottom = bobs_hitbox.midbottom

    #Falling baclony logic
    if balcony_falling == True:
        fall_speed = 3
        move_y = min(fall_speed, 200 - balcony_fall_distance)
        for rect in balcony:
            rect.y += move_y
        balcony_fall_distance += move_y
        if balcony_fall_distance >= 200:
            balcony_falling = False
            balcony_fell = True
            landing_grass.play()

    #Drawing most of the custom art onscreen
    screen.blit(instruction_jump, instruction_jump_rect)
    screen.blit(instruction_move, instruction_move_rect)
    screen.blit(instruction_crouch, instruction_crouch_rect)
    screen.blit(instruction_interact, instruction_interact_rect)
    screen.blit(door_art, door.topleft)
    screen.blit(not_pressed_button_art, button.topleft)
    for rect in gameplay + entrance:
        screen.blit(crate, rect.topleft)
    for rect in passable_gameplay:
        screen.blit(passable_art, rect.topleft)
    for rect in balcony:
        screen.blit(balcony_art, rect.topleft)
    if inHouse == False:
        if isCrouching == True:
            current_art = crouching_art
        else:
            current_art = bob_art
        art_x = bobs_hitbox.centerx - current_art.get_width() // 2
        art_y = bobs_hitbox.bottom - current_art.get_height()
        screen.blit(current_art, (art_x, art_y))

    #Raining function
    def raining():
        global rain, outside, lightning_duration, lightning_active, lightning_end_time, remainder_time, darkness, gameplay, passable_gameplay
        if transitioning == False and inHouse == False:
            darkness.set_alpha(150)
        for drop in rain:
            drop[1] += drop[2]
            drop_rect = pygame.Rect(drop[0] - 3, drop[1], 4, drop[3])
            hit_block = any(
                drop_rect.colliderect(block)
                for block in gameplay + passable_gameplay + balcony
            )
            if hit_block or drop[1] > screen_size[1] - 100:
                drop[0] = random.randint(0, screen_size[0])
                drop[1] = random.randint(-20, -5)
            pygame.draw.line(
                screen,
                (150, 180, 220),
                (drop[0], drop[1]),
                (drop[0] - 3, drop[1] + drop[3]),
                2
            )
        #Lightning logic
        if transitioning == False and inHouse == False:
            lightning_timer = pygame.time.get_ticks()
            if lightning_timer - remainder_time >= 5000:
                lightning_strike = random.randint(0, 5)
                lightning_backgrounds = [
                    lightning1, lightning2, lightning3,
                    lightning4, lightning5, lightning6
                ]
                outside = lightning_backgrounds[lightning_strike]
                thunder_sfx.play()
                lightning_active = True
                darkness.set_alpha(0)
                lightning_end_time = lightning_timer + lightning_duration
                remainder_time = lightning_timer
            if lightning_active and lightning_timer >= lightning_end_time:
                outside = stormy_outside
                lightning_active = False
                darkness.set_alpha(150)

    #Activate raining
    if bob.colliderect(raining_area) == True and isRaining == False:
        raining_sfx.play(-1)
        outside = stormy_outside
        isRaining = True
    if isRaining == True:
        raining()

    #Drawing house art
    if inHouse == True:
        screen.blit(creepy_house, (0,0))
        screen.blit(current_fireplace_art, fireplace.topleft)
        screen.blit(dining_table_art, dining_table.topleft)
        screen.blit(stove_art, stove.topleft)
        for rect in chair:
            screen.blit(chair_art, rect.topleft)
        for rect in other_chair:
            screen.blit(other_chair_art, rect.topleft)
        for rect in fireplace_chimney:
            screen.blit(fireplace_chimney_art, rect.topleft)
        for rect in cupboards:
            screen.blit(cupboard_closed_art, rect.topleft)
        for rect in floor + ceiling:
            screen.blit(floorboard_art, rect.topleft)
        if isCrouching == True:
            current_art = crouching_art
        else:
            current_art = bob_art
        art_x = bobs_hitbox.centerx - current_art.get_width() // 2
        art_y = bobs_hitbox.bottom - current_art.get_height()
        screen.blit(current_art, (art_x, art_y))
        if has_bob_moved_after_transition == False:
            bobs_hitbox.move_ip(-600, 0)
            has_bob_moved_after_transition = True

    #Darkness overlay
    #screen.blit(darkness, (0,0))

    #Refresh rate
    pygame.display.flip()
    clock.tick(60)

#Once loop is exited
pygame.quit()