import pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT=500, 500
display_surface=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Adding imag and background")
background_image=pygame.transform.scale(
    pygame.image.load("night.jpeg").convert(),
    (SCREEN_WIDTH, SCREEN_HEIGHT))
tiger_image=pygame.transform.scale(
    pygame.image.load("white_tiger.jpeg").convert_alpha(),(200,200))
tiger_rect=tiger_image.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2-30))
text=pygame.font.Font(None,36).render('Hello World',True, pygame.Color('black'))
text_rect=text.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2+110))
def game_loop():
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        display_surface.blit(background_image, (0, 0))
        display_surface.blit(tiger_image, tiger_rect)
        display_surface.blit(text, text_rect)

        pygame.display.flip()

        clock.tick(30)

    pygame.quit()

if __name__ == '__main__':
    game_loop()
print("Hello")