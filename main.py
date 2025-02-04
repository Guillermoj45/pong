import pygame, sys, random

# Inicialización de Pygame
pygame.init()

# Variables de la pantalla
screen_width = 1280
screen_height = 760
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()  # Define el reloj localmente

# Configuración de la fuente para el marcador
font = pygame.font.Font(None, 74)  # Fuente por defecto de tamaño 74

# Variables del juego
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)  # Pala enemiga ubicada en el lado izquierdo

bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0  # Velocidad del jugador
opponent_speed = 7

# Variables para el contador de puntuación
player_score = 0      # Puntuación del jugador (lado derecho)
opponent_score = 0    # Puntuación del oponente (lado izquierdo)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    # Movimiento de la bola y la pala del jugador
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    player.y += player_speed

    # Control de límites para la pala del jugador
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

    # Colisión de la bola con la parte superior e inferior
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    # Colisión con los bordes izquierdo y derecho
    if ball.left <= 0 or ball.right >= screen_width:
        # Actualización de la puntuación según el borde tocado:
        if ball.left <= 0:
            # La bola tocó la pared enemiga (lado izquierdo), se le otorga punto al jugador (lado derecho)
            player_score += 1
            print("La bola ha tocado la pared enemiga. Punto para el jugador.")
        if ball.right >= screen_width:
            # La bola tocó la pared del jugador, se le otorga punto al oponente (lado izquierdo)
            opponent_score += 1
            print("La bola ha tocado la pared del jugador. Punto para el oponente.")

        # Reinicia la bola en el centro y se asignan nuevas direcciones aleatorias
        ball.center = (screen_width/2, screen_height/2)
        ball_speed_y *= random.choice((1, -1))
        ball_speed_x *= random.choice((1, -1))

    # Colisiones con las palas
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

    # Movimiento de la IA del oponente
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

    # Visualización
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))

    # Renderizado y visualización del marcador
    score_text = font.render(f"{opponent_score}  -  {player_score}", True, light_grey)
    score_rect = score_text.get_rect(center=(screen_width/2, 30))
    screen.blit(score_text, score_rect)

    pygame.display.flip()
    clock.tick(60)
