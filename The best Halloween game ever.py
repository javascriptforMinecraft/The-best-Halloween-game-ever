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
time = pygame.time.Clock()

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
    pygame.Rect(500, 300, 100, 100),
    pygame.Rect(600, 300, 100, 100),
    pygame.Rect(700, 300, 100, 100),
    pygame.Rect(800, 300, 100, 100),
    pygame.Rect(900, 300, 100, 100),

    pygame.Rect(500, 400, 100, 100),
    pygame.Rect(600, 400, 100, 100),
    pygame.Rect(700, 400, 100, 100),
    pygame.Rect(800, 400, 100, 100),
    pygame.Rect(900, 400, 100, 100),

    pygame.Rect(500, 500, 100, 100),
    pygame.Rect(600, 500, 100, 100),
    pygame.Rect(700, 500, 100, 100),
    pygame.Rect(800, 500, 100, 100),
    pygame.Rect(900, 500, 100, 100),

    pygame.Rect(500, 600, 100, 100),
    pygame.Rect(600, 600, 100, 100),
    pygame.Rect(700, 600, 100, 100),
    pygame.Rect(800, 600, 100, 100),
    pygame.Rect(900, 600, 100, 100),
]

bob = pygame.Rect(400, 600, 100, 100)

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
    if key[pygame.K_a] == True:
        for rect in gameplay:
            rect.move_ip(-3, 0)
    elif key[pygame.K_d] == True:
        for rect in gameplay:
            rect.move_ip(3, 0)

    pygame.display.flip()
    time.tick(60)

pygame.quit()