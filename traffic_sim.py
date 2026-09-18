import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Traffic Signal Simulator")

clock = pygame.time.Clock()

ROAD_Y = HEIGHT // 2
ROAD_HEIGHT = 80

CAR_EVENT = pygame.USEREVENT + 1

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, color):
        super().__init__()
        self.color = color
        self.speed = speed
        self.image = pygame.Surface((80, 40))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.x += self.speed
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            pygame.event.post(pygame.event.Event(CAR_EVENT, {"car": self}))

class TrafficSignal:
    def __init__(self, x, y):
        self.state = "GREEN"
        self.red_color = (200, 40, 40)
        self.green_color = (40, 200, 40)
        self.base_color = (50, 50, 50)
        self.rect = pygame.Rect(x, y, 40, 100)

    def toggle(self):
        if self.state == "GREEN":
            self.state = "RED"
        else:
            self.state = "GREEN"

    def draw(self, surface):
        pygame.draw.rect(surface, self.base_color, self.rect)
        red_circle_center = (self.rect.centerx, self.rect.top + 25)
        green_circle_center = (self.rect.centerx, self.rect.bottom - 25)
        if self.state == "RED":
            pygame.draw.circle(surface, self.red_color, red_circle_center, 12)
            pygame.draw.circle(surface, (80, 80, 80), green_circle_center, 12)
        else:
            pygame.draw.circle(surface, (80, 80, 80), red_circle_center, 12)
            pygame.draw.circle(surface, self.green_color, green_circle_center, 12)

car_group = pygame.sprite.Group()
car = Car(100, ROAD_Y + ROAD_HEIGHT // 2 - 20, 4, (0, 0, 255))
car_group.add(car)

signal = TrafficSignal(WIDTH - 80, ROAD_Y - 120)

bg_color = (220, 220, 220)
road_color = (60, 60, 60)
line_color = (240, 240, 240)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == CAR_EVENT:
            c = event.car
            if signal.state == "GREEN":
                signal.toggle()
                c.color = (255, 0, 0)
                c.image.fill(c.color)
                c.speed = -abs(c.speed)
            else:
                signal.toggle()
                c.color = (0, 255, 0)
                c.image.fill(c.color)
                c.speed = abs(c.speed)

    car_group.update()

    screen.fill(bg_color)

    pygame.draw.rect(screen, road_color, (0, ROAD_Y, WIDTH, ROAD_HEIGHT))
    pygame.draw.line(
        screen,
        line_color,
        (0, ROAD_Y + ROAD_HEIGHT // 2),
        (WIDTH, ROAD_Y + ROAD_HEIGHT // 2),
        2,
    )

    signal.draw(screen)
    car_group.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
