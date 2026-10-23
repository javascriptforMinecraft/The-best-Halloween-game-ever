#Modules required
from PIL import Image
import sys
import os
import random
import pygame


#Background
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

#Initialisation
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Retro Pixel", 20)
instruction1 = font.render("W to jump", False, (255, 255, 255))
instruction2 = font.render("A/D to move left/right", False, (255, 255, 255))
instruction3 = font.render("S to crouch", False, (255, 255, 255))
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
background = load_background("Outside.png", screen_size)
clock = pygame.time.Clock()

#Art
def load_art(art):
    try:
        return pygame.image.load(art)
    except Exception as e:
        print(f"Error: Could not load '{art}'. {e}")
        pygame.quit()
        sys.exit()
gameplay_art = load_art("Crate.png")
bob_art = load_art("BOB.png")
crouching_art = load_art("BOB_crouch.png")
button_art = load_art("Button.png")
button_art = pygame.transform.rotate(button_art, 90)
passable_art = load_art("Passable crate.png")

#SFX
jump_sfx = pygame.mixer.Sound("Jump.mp3")
landing_sfx = pygame.mixer.Sound("Landing.mp3")
raining_sfx = pygame.mixer.Sound("Raining.mp3")

#Objects
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

running = True
isRaining = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()

    screen.blit(background, (0, 0))
    screen.blit(instruction1, (200, 300))
    screen.blit(instruction2, (200, 330))
    screen.blit(instruction3, (200, 360))

    was_on_ground = on_ground

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

    scroll_x = 0
    if key[pygame.K_a] == True:
        scroll_x = 5
    elif key[pygame.K_d] == True:
        scroll_x = -5
    if scroll_x != 0:
        can_scroll = True
        for rect in gameplay:
            future_rect = rect.move(scroll_x, 0)
            if bobs_hitbox.colliderect(future_rect) == True:
                can_scroll = False
                break

        if can_scroll == True:
            for rect in gameplay:
                rect.move_ip(scroll_x, 0)
            for rect in buttons:
                rect.move_ip(scroll_x, 0)
            for rect in passable_gameplay:
                rect.move_ip(scroll_x, 0)
            raining_area.move_ip(scroll_x, 0)

    if key[pygame.K_w] == True and on_ground == True and isCrouching == False:
        velocity_y = -jump_speed
        on_ground = False
        jump_sfx.play()

    previous = bobs_hitbox.copy()
    velocity_y += gravity
    bobs_hitbox.y += round(velocity_y)
    on_ground = False

    for rect in gameplay:
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

    for rect in gameplay:
        screen.blit(gameplay_art, rect.topleft)
    for rect in buttons:
        screen.blit(button_art, rect.topleft)
    for rect in passable_gameplay:
        screen.blit(passable_art, rect.topleft)
    if isCrouching == True:
        current_art = crouching_art
    else:
        current_art = bob_art
    art_x = bobs_hitbox.centerx - current_art.get_width() // 2
    art_y = bobs_hitbox.bottom - current_art.get_height()
    screen.blit(current_art, (art_x, art_y))

    if bobs_hitbox.colliderect(buttons[0]) == True:
        for rect in wall0:
            if rect in gameplay:
                gameplay.remove(rect)
        wall0.clear()

    def raining():
            rain = []
            for k in range(150):
                x = random.randint(0, screen_size[0])
                y = random.randint(0, screen_size[1])
                speed = random.randint(8, 15)
                length = random.randint(8, 18)
                rain.append([x, y, speed, length])
            for drop in rain:
                drop[1] += drop[2]
                if drop[1] > screen_size[1] - 100:
                    drop[0] = random.randint(0, screen_size[0])
                    drop[1] = random.randint(-20, -5)
                pygame.draw.line(
                    screen,
                    (150, 180, 220),
                    (drop[0], drop[1]),
                    (drop[0] - 3, drop[1] + drop[3]),
                    2
                )
    if bob.colliderect(raining_area) == True and isRaining == False:
        raining_sfx.play(-1)
        isRaining = True
    if isRaining == True:
        raining()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()