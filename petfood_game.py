import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pet Food Collection Game")

bg = pygame.image.load("background.jpg")
bg = pygame.transform.scale(bg, (800, 600))

pet = pygame.Rect(100, 100, 50, 50)

foods = [
    pygame.Rect(200, 150, 30, 30),
    pygame.Rect(500, 200, 30, 30),
    pygame.Rect(300, 400, 30, 30),
    pygame.Rect(650, 350, 30, 30)
]

font = pygame.font.SysFont("Arial", 48)

speed = 5
clock = pygame.time.Clock()

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        pet.x -= speed

    if keys[pygame.K_RIGHT]:
        pet.x += speed

    if keys[pygame.K_UP]:
        pet.y -= speed

    if keys[pygame.K_DOWN]:
        pet.y += speed

    for food in foods[:]:
        if pet.colliderect(food):
            foods.remove(food)

    screen.blit(bg, (0, 0))

    pygame.draw.rect(screen, (0, 0, 255), pet)

    for food in foods:
        pygame.draw.rect(screen, (255, 165, 0), food)

    if len(foods) == 0:
        message = font.render("You Collected All The Food!", True, (255, 255, 255))
        message_rect = message.get_rect(center=(400, 300))
        screen.blit(message, message_rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
