#Modules required
from PIL import Image
import sys
import os
import random
import pygame

#Initialisation
pygame.init()
pygame.font.init()
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

#Loading background function
def load_background(image_path, screen_size):
    try:
        img = Image.open(image_path).convert("RGB")
        img = img.resize(screen_size, Image.LANCZOS)
        img_bytes = img.tobytes()
        surface = pygame.image.frombuffer(img_bytes, img.size, "RGB")
        return surface
    except Exception as e:
        print(f"Error loading background: {e}")
        sys.exit(1)

#Loading backgrounds
outside = load_background("Outside.png", screen_size)
stormy_outside = load_background("Stormy.png", screen_size)
lightning1 = load_background("Lightning1.png", screen_size)
lightning2 = load_background("Lightning2.png", screen_size)
lightning3 = load_background("Lightning3.png", screen_size)
lightning4 = load_background("Lightning4.png", screen_size)
lightning5 = load_background("Lightning5.png", screen_size)
lightning6 = load_background("Lightning6.png", screen_size)
creepy_house = load_background("Creepy House.png", screen_size)

#Art
def load_art(art):
    try:
        return pygame.image.load(art)
    except Exception as e:
        print(f"Error: Could not load '{art}'. {e}")
        pygame.quit()
        sys.exit()

#Loading art
crate = load_art("Crate.png")
bob_art = load_art("BOB.png")
crouching_art = load_art("BOB_crouch.png")
not_pressed_button_art = load_art("Button (not pressed).png")
not_pressed_button_art = pygame.transform.rotate(not_pressed_button_art, 90)
pressed_button_art = load_art("Button (pressed).png")
pressed_button_art = pygame.transform.rotate(pressed_button_art, 90)
passable_art = load_art("Passable crate.png")
balcony_art = load_art("Balcony.png")
door_art = load_art("Door.png")

#SFX
jump_sfx = pygame.mixer.Sound("Jump.mp3")
landing_sfx = pygame.mixer.Sound("Landing.mp3")
raining_sfx = pygame.mixer.Sound("Raining.mp3")
click_sfx = pygame.mixer.Sound("Button clicked.mp3")
thunder_sfx = pygame.mixer.Sound("Thunder.mp3")
balcony_creaking_sfx = pygame.mixer.Sound("Balcony creaking.mp3")
creaking_channel = pygame.mixer.Channel(1)
walking_grass = pygame.mixer.Sound("Walking on grass.mp3")
landing_grass = pygame.mixer.Sound("Landing on grass.mp3")
walking_wood = pygame.mixer.Sound("Walking on wood.mp3")

#Objects
darkness = pygame.Surface((800, 600))
darkness.fill((0, 0, 0))
darkness.set_alpha(100)

raining_area = pygame.Rect(3000, 0, 10, 600)

wall0 = [
    pygame.Rect(2000, 0, 100, 100),
    pygame.Rect(2000, 100, 100, 100),
    pygame.Rect(2000, 200, 100, 100),
    pygame.Rect(2000, 300, 100, 100),
    pygame.Rect(2000, 400, 100, 100)
]
buttons = [
    pygame.Rect(1300, 413, 40, 74)
]
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

house = [
    pygame.Rect(4000, 0, 100, 100),
    pygame.Rect(4000, 100, 100, 100),
    pygame.Rect(4000, 200, 100, 100),
]
door = pygame.Rect(4000, 300, 100, 200)
balcony = [
    pygame.Rect(3800, 200, 100, 100),
    pygame.Rect(3900, 200, 100, 100)
]

camera_change = pygame.Rect(3670, 0, 10, 600)
transition_rect = pygame.Rect(4200, 0, 10, 600)

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

#Main loop
while running:
    #If game is quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
            inHouse = True
            start_of_fade = pygame.time.get_ticks()
            if pygame.time.get_ticks() - start_of_fade >= 0:
                alpha_fade(darkness, darkness.get_alpha(), 150, 8)

    #Left-Right movement
    scroll_x = 0
    if transitioning == False:
        if key[pygame.K_a] == True:
            scroll_x = 5
        elif key[pygame.K_d] == True:
            scroll_x = -5
        isMoving = (key[pygame.K_a] or key[pygame.K_d]) and not transitioning
        if isMoving:
            if bobs_hitbox.bottom >= screen_size[1] - 100:
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
                if not any(future_hitbox.colliderect(rect) for rect in gameplay + balcony + house):
                    bobs_hitbox.x -= scroll_x
            else:
                can_scroll = True
                for rect in gameplay:
                    future_rect = rect.move(scroll_x, 0)
                    if bobs_hitbox.colliderect(future_rect) == True:
                        can_scroll = False
                        break
                if can_scroll == True:

                    for rect in gameplay + buttons + passable_gameplay + house + balcony + [raining_area] + [door] + [camera_change] + [transition_rect]:
                        rect.move_ip(scroll_x, 0)
                    instruction_jump_rect.x += scroll_x
                    instruction_move_rect.x += scroll_x
                    instruction_crouch_rect.x += scroll_x

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
    for rect in gameplay + balcony:
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
    if bobs_hitbox.bottom >= screen_size[1] - 100:
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
    screen.blit(door_art, door.topleft)
    for rect in gameplay + house:
        screen.blit(crate, rect.topleft)
    for rect in buttons:
        screen.blit(not_pressed_button_art, rect.topleft)
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

    #Button collision
    if bobs_hitbox.colliderect(buttons[0]) == True and clicked == False:
        for rect in wall0:
            if rect in gameplay:
                gameplay.remove(rect)
        wall0.clear()
        not_pressed_button_art = pressed_button_art
        click_sfx.play()
        clicked = True

    #Raining function
    def raining():
        global rain, outside, lightning_duration, lightning_active, lightning_end_time, remainder_time, darkness, gameplay, passable_gameplay
        if transitioning == False:
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
        if transitioning == False:
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

    if inHouse == True:
        screen.blit(creepy_house, (0,0))
        if isCrouching == True:
            current_art = crouching_art
        else:
            current_art = bob_art
        art_x = bobs_hitbox.centerx - current_art.get_width() // 2
        art_y = bobs_hitbox.bottom - current_art.get_height()
        screen.blit(current_art, (art_x, art_y))

    #Darkness overlay
    screen.blit(darkness, (0,0))

    #Refresh rate
    pygame.display.flip()
    clock.tick(60)

#Once loop is exited
pygame.quit()