#Modules required
from PIL import Image
import sys
import pygame

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

pygame.init()
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
background = load_background("Coloured Bricks.png", screen_size)
time = pygame.time.Clock()

gameplay = [
    pygame.Rect(400, 300, 500, 300)
]

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
        pygame.draw.rect(screen, (0, 50, 0), gameplay)
    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        for rect in gameplay:
            gameplay.move_ip(-3, 0)
    elif key[pygame.K_d] == True:
        for rect in gameplay:
            gameplay.move_ip(3, 0)

    pygame.display.flip()
    time.tick(60)
    pygame.display.update()

pygame.quit()