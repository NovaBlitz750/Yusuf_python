import pygame
def main():
    pygame.init()
    sc_width, sc_height= 500,500
    screen=pygame.display.set_mode((sc_width, sc_height))
    pygame.display.set_caption("Color changing sprite")
    colors={
        'red':pygame.Color('red'),
        'green':pygame.Color('green'),
        'blue':pygame.Color('blue'),
        'yellow':pygame.Color('yellow'),
        'white':pygame.Color('white')
    }
    current_color=colors['white']
    x,y=30,30
    spwidth, spheight=60, 60
    clock=pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pressed=pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
             x-=3
        if pressed[pygame.K_RIGHT]:
             x+=3
        if pressed[pygame.K_UP]:
            y-=3    
        if pressed[pygame.K_DOWN]:
             y+=3
        x=min(max(0,x),sc_width-spwidth)
        y=min(max(0,y),sc_height-spheight)
        if x==0: current_color=colors['blue']
        elif x==sc_width-spwidth:current_color=colors['yellow']
        elif y==0: current_color=colors["red"]
        elif y==sc_height-spheight:current_color=colors['green']
        else:
             current_color=colors['white']
        screen.fill((0,0,0))
        pygame.draw.rect(screen, current_color,
                         (x,y, spwidth, spheight))
        pygame.display.flip()
    
        clock.tick(90)
    
    pygame.quit()
if __name__=="__main__":
    main()