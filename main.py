import pygame, sys, random

# Inicialización de Pygame
pygame.init()

# Variables de la pantalla
screen_width = 1280
screen_height = 760
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# Colores y fuentes
bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)
font_large = pygame.font.Font(None, 74)
font_medium = pygame.font.Font(None, 50)

# Estados del juego
# 'menu': menú principal, 'select': selección del tipo de oponente, 'game': partida en juego
state = 'menu'
opponent_type = 'IA'  # Valor por defecto

# Botones en el menú principal
# Se definen rectángulos para detectar los clics
btn_select = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 100, 300, 60)
btn_exit = pygame.Rect(screen_width // 2 - 150, screen_height // 2 + 20, 300, 60)

# Botones en la pantalla de selección de oponente
btn_ia = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 100, 300, 60)
btn_player = pygame.Rect(screen_width // 2 - 150, screen_height // 2 + 20, 300, 60)


# Función para dibujar un botón
def draw_button(rect, text):
    pygame.draw.rect(screen, light_grey, rect, border_radius=5)
    text_surface = font_medium.render(text, True, bg_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


# Variables del juego (se inicializan cuando se empieza la partida)
def init_game():
    global ball, player, opponent, ball_speed_x, ball_speed_y, player_speed, opponent_speed, player_score, opponent_score
    ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
    player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
    opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)  # Pala del oponente
    ball_speed_x = 7 * random.choice((1, -1))
    ball_speed_y = 7 * random.choice((1, -1))
    player_speed = 0  # Velocidad del jugador (lado derecho)
    opponent_speed = 7
    player_score = 0  # Puntuación del jugador (lado derecho)
    opponent_score = 0  # Puntuación del oponente (lado izquierdo)
    return player_score, opponent_score


# Variables de puntuación (inicializadas al comenzar la partida)
player_score, opponent_score = 0, 0

# Bucle principal del programa
while True:
    # Captura de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Procesamiento de eventos según el estado actual
        if state == 'menu':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_select.collidepoint(event.pos):
                    state = 'select'
                elif btn_exit.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        elif state == 'select':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_ia.collidepoint(event.pos):
                    opponent_type = 'IA'
                    # Se inicializan las variables del juego y se cambia al estado 'game'
                    player_score, opponent_score = init_game()
                    state = 'game'
                elif btn_player.collidepoint(event.pos):
                    opponent_type = 'player'
                    player_score, opponent_score = init_game()
                    state = 'game'
        elif state == 'game':
            # Eventos de teclado para controlar la pala del jugador (lado derecho)
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

    # Lógica y visualización según el estado
    if state == 'menu':
        # Menú principal
        screen.fill(bg_color)
        title_surface = font_large.render("PONG", True, light_grey)
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 4))
        screen.blit(title_surface, title_rect)

        # Botón para seleccionar el tipo de oponente (se ubica en la parte superior, según se indica)
        draw_button(btn_select, "Seleccionar Oponente")
        # Botón para salir de la aplicación
        draw_button(btn_exit, "Salir")

    elif state == 'select':
        # Pantalla para seleccionar el tipo de oponente
        screen.fill(bg_color)
        title_surface = font_large.render("Elige el oponente", True, light_grey)
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 4))
        screen.blit(title_surface, title_rect)

        draw_button(btn_ia, "IA")
        draw_button(btn_player, "Jugador")

    elif state == 'game':
        # Actualización de la lógica del juego Pong
        ball.x += ball_speed_x
        ball.y += ball_speed_y
        player.y += player_speed

        # Movimiento de la pala del oponente según el tipo seleccionado
        if opponent_type == 'IA':
            if opponent.top < ball.y:
                opponent.top += opponent_speed
            if opponent.bottom > ball.y:
                opponent.bottom -= opponent_speed
        else:  # Control manual para el jugador oponente
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                opponent.y -= opponent_speed
            if keys[pygame.K_s]:
                opponent.y += opponent_speed

        # Límites para la pala del jugador (lado derecho)
        if player.top <= 0:
            player.top = 0
        if player.bottom >= screen_height:
            player.bottom = screen_height

        # Límites para la pala del oponente
        if opponent.top <= 0:
            opponent.top = 0
        if opponent.bottom >= screen_height:
            opponent.bottom = screen_height

        # Colisión de la bola con la parte superior e inferior
        if ball.top <= 0 or ball.bottom >= screen_height:
            ball_speed_y *= -1

        # Colisión con los bordes izquierdo y derecho
        if ball.left <= 0 or ball.right >= screen_width:
            # Actualización de la puntuación según el borde tocado:
            if ball.left <= 0:
                # La bola tocó la pared enemiga (lado izquierdo), se otorga punto al jugador (lado derecho)
                player_score += 1
                print("La bola ha tocado la pared enemiga. Punto para el jugador.")
            if ball.right >= screen_width:
                # La bola tocó la pared del jugador, se otorga punto al oponente (lado izquierdo)
                opponent_score += 1
                print("La bola ha tocado la pared del jugador. Punto para el oponente.")

            # Reiniciar la bola en el centro y asignar nuevas direcciones aleatorias
            ball.center = (screen_width / 2, screen_height / 2)
            ball_speed_y *= random.choice((1, -1))
            ball_speed_x *= random.choice((1, -1))

        # Colisión de la bola con las palas
        if ball.colliderect(player) or ball.colliderect(opponent):
            ball_speed_x *= -1

        # Visualización de la partida
        screen.fill(bg_color)
        pygame.draw.rect(screen, light_grey, player)
        pygame.draw.rect(screen, light_grey, opponent)
        pygame.draw.ellipse(screen, light_grey, ball)
        pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

        # Visualización del marcador
        score_text = font_medium.render(f"{opponent_score}  -  {player_score}", True, light_grey)
        score_rect = score_text.get_rect(center=(screen_width / 2, 30))
        screen.blit(score_text, score_rect)

    pygame.display.flip()
    clock.tick(60)
