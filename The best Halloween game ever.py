#Modules required
from PIL import Image
import sys
import os
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
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
background = load_background("Coloured Bricks.png", screen_size)
clock = pygame.time.Clock()

#Art
def load_art(art):
    try:
        return pygame.image.load(art)
    except Exception as e:
        print(f"Error: Could not load '{art}'. {e}")
        pygame.quit()
        sys.exit()
gameplay_art = load_art("Coloured_Block.png")
bob_art = load_art("BOB.png")
crouching_art = load_art("BOB_crouch.png")

#Objects
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

    pygame.Rect(500, 500, 100, 100),
    pygame.Rect(600, 500, 100, 100),
    pygame.Rect(700, 500, 100, 100),
    pygame.Rect(800, 500, 100, 100),
    pygame.Rect(900, 500, 100, 100),
]

bob = pygame.Rect(300, 500, 100, 100)
isJumping = False
on_ground = True
jump_speed = 15
gravity = 0.8
velocity_y = 0
ground_y = 500

running = True
while running:

    #Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Background
    screen.blit(background, (0, 0))

    #Gameplay
    for rect in gameplay:
        screen.blit(gameplay_art, rect.topleft)
    screen.blit(bob_art, bob.topleft)
    key = pygame.key.get_pressed()
    scroll_x = 0
    if key[pygame.K_a]:
        scroll_x = 3
    elif key[pygame.K_d]:
        scroll_x = -3
    can_scroll = True
    if scroll_x != 0:
        for rect in gameplay:
            future_rect = rect.move(scroll_x, 0)
            if bob.colliderect(future_rect):
                can_scroll = False
                break
    if can_scroll:
        for rect in gameplay:
            rect.move_ip(scroll_x, 0)
    if key[pygame.K_w] == True and on_ground == True:
        velocity_y = -jump_speed
        on_ground = False
        isJumping = True
    velocity_y += gravity
    previous = bob.copy()
    bob.y += velocity_y
    on_ground = False
    for rect in gameplay:
        if bob.colliderect(rect):
            if velocity_y >= 0 and previous.bottom <= rect.top:
                bob.bottom = rect.top
                velocity_y = 0
                on_ground = True
                isJumping = False
            elif velocity_y < 0 and previous.top >= rect.bottom:
                bob.top = rect.bottom
                velocity_y = 0
    if bob.bottom >= 600:
        bob.bottom = 600
        velocity_y = 0
        on_ground = True
        isJumping = False
    previous = bob.copy()
    for rect in gameplay:
        if bob.colliderect(rect):
            if previous.right <= rect.left:
                bob.right = rect.left
            elif previous.left >= rect.right:
                bob.left = rect.right

    pygame.display.flip()
    clock.tick(60)

pygame.quit()