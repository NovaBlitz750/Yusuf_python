import random
import pygame

# Constants for easier adjustments
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 800
MOVEMENT_SPEED = 5
FONT_SIZE = 72

# Initialize Pygame
pygame.init()

# Setup Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite Collision")

# Load and transform the background image 
# (Using a fallback in case your specific image file isn't in the folder)
try:
    background_image = pygame.image.load("game_background.jpeg")
except FileNotFoundError:
    try:
        background_image = pygame.image.load("bg.jpg")
    except FileNotFoundError:
        # If no image files are found, create a blank green fallback surface
        background_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background_image.fill(pygame.Color('darkgreen'))

background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load font
font = pygame.font.SysFont("Times New Roman", FONT_SIZE)

# Properly structured Sprite Class
class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width):  # Fixed underscores here
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color('dodgerblue'))  # Border/Background color of sprite
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()

    def move(self, x_change, y_change):
        # Keeps sprites bounded perfectly inside the screen limits
        self.rect.x = max(min(self.rect.x + x_change, SCREEN_WIDTH - self.rect.width), 0)
        self.rect.y = max(min(self.rect.y + y_change, SCREEN_HEIGHT - self.rect.height), 0)


# Initialize Sprites Group
all_sprites = pygame.sprite.Group()

# Create player sprite (Black)
sprite1 = Sprite(pygame.Color('black'), 20, 30)
sprite1.rect.x = random.randint(0, SCREEN_WIDTH - sprite1.rect.width)
sprite1.rect.y = random.randint(0, SCREEN_HEIGHT - sprite1.rect.height)
all_sprites.add(sprite1)
    
# Create target sprite (Red)
sprite2 = Sprite(pygame.Color('red'), 20, 30)
sprite2.rect.x = random.randint(0, SCREEN_WIDTH - sprite2.rect.width)
sprite2.rect.y = random.randint(0, SCREEN_HEIGHT - sprite2.rect.height)
all_sprites.add(sprite2)

# Game loop control variables
running, won = True, False
clock = pygame.time.Clock()

# Main game loop
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_x):
            running = False

    if not won:
        # Smooth keyboard input reading
        keys = pygame.key.get_pressed()
        x_change = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * MOVEMENT_SPEED
        y_change = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * MOVEMENT_SPEED
        sprite1.move(x_change, y_change)

        # Collision detection checks if player touches target
        if sprite1.rect.colliderect(sprite2.rect):
            all_sprites.remove(sprite2)
            won = True

    # Drawing frame steps
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)

    # Display win message overlay
    if won:
        win_text = font.render("You win!", True, pygame.Color('black'))
        screen.blit(win_text, ((SCREEN_WIDTH - win_text.get_width()) // 2,
                               (SCREEN_HEIGHT - win_text.get_height()) // 2))

    pygame.display.flip()
    clock.tick(90)  # Locked to 90 FPS for consistent gameplay speed

pygame.quit()
