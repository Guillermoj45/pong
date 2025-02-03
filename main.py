import pygame, sys
from pygame.examples.go_over_there import screen, clock

# Initialize Pygame

screen_width = 1280
screen_height = 860
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")

# Game Variables

ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
# ball2 = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(10, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)

bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #Visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    # pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))

    pygame.display.flip()
    clock.tick(60)

