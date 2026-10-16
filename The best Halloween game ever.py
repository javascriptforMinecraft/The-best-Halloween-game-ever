#Modules required
from PIL import Image, ImageDraw
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

try:
    art_image = pygame.image.load("Coloured Block.png").convert_alpha()
except pygame.error:
    print("Error: Could not load 'custom_art.png'. Make sure the file exists.")
    pygame.quit()
    sys.exit()

def create_tessellated_mask(shape_points, texture_path, size):
    mask_img = Image.new("RGB", size, (0, 0, 0, 0))
    texture = Image.open(texture_path).convert("RGB")
    tex_w, tex_h = texture.size
    for y in range(0, size[1], tex_h):
        for x in range(0, size[0], tex_w):
            mask_img.paste(texture, (x, y))
    poly_mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(poly_mask)
    draw.polygon(shape_points, fill=255)
    mask_img.putalpha(poly_mask)
    return mask_img
 
def pil_to_pygame(pil_image):
    mode = pil_image.mode
    size = pil_image.size
    data = pil_image.tobytes()
    return pygame.image.fromstring(data, size, mode)

art_image = pygame.transform.scale(art_image, (100, 100))
mask_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
pygame.draw.circle(mask_surface, (255, 255, 255, 255), (100, 100), 100)
final_surface = pygame.Surface((200, 200), pygame.SRCALPHA)
final_surface.blit(art_image, (0, 0))
final_surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGB_MIN)

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
        pygame.draw.rect(screen, (0, 50, 0), rect)
    screen.blit(final_surface, (150, 150))
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