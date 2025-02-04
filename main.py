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

# Estados del juego:
# 'menu': menú principal,
# 'select': selección del tipo de oponente,
# 'game': partida en juego,
# 'game_over': tiempo terminado y resultado mostrado
state = 'menu'
opponent_type = 'IA'  # Valor por defecto

# Botones en el menú principal
btn_select = pygame.Rect(screen_width // 2 - 200, screen_height // 2 - 100, 400, 80)
btn_exit = pygame.Rect(screen_width // 2 - 150, screen_height // 2 + 20, 300, 60)

# Botones en la pantalla de selección de oponente
btn_ia = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 100, 300, 60)
btn_player = pygame.Rect(screen_width // 2 - 150, screen_height // 2 + 20, 300, 60)

# Botón para salir en la pantalla de Game Over
btn_exit_game = pygame.Rect(screen_width // 2 - 150, screen_height // 2 + 80, 300, 60)

# Variable para almacenar el tiempo de inicio de la partida (en milisegundos)
game_start_time = None
# Duración de la partida: 5 minutos = 300000 ms
game_duration = 300000

# Función para dibujar un botón
def draw_button(rect, text):
    pygame.draw.rect(screen, light_grey, rect, border_radius=5)
    text_surface = font_medium.render(text, True, bg_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Función para crear una nueva bola
def create_ball():
    return {
        'rect': pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30),
        'speed_x': 7 * random.choice((1, -1)),
        'speed_y': 7 * random.choice((1, -1))
    }

# Función de inicialización del juego
def init_game():
    global balls, player, opponent, player_speed, opponent_speed, player_score, opponent_score, game_start_time
    balls = [create_ball()]  # Se inicia con una bola
    player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
    opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)  # Pala del oponente
    player_speed = 0  # Velocidad del jugador (lado derecho)
    opponent_speed = 7
    player_score = 0  # Puntuación del jugador (lado derecho)
    opponent_score = 0  # Puntuación del oponente (lado izquierdo)
    # Se marca el tiempo de inicio de la partida
    game_start_time = pygame.time.get_ticks()

# Inicialización de variables de juego
init_game()

# Bucle principal del programa
while True:
    # Captura de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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
                    init_game()
                    state = 'game'
                elif btn_player.collidepoint(event.pos):
                    opponent_type = 'player'
                    init_game()
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
        elif state == 'game_over':
            # En la pantalla final se espera la pulsación en el botón de salir
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_exit_game.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

    # Lógica y visualización según el estado
    if state == 'menu':
        # Menú principal
        screen.fill(bg_color)
        title_surface = font_large.render("PONG", True, light_grey)
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 4))
        screen.blit(title_surface, title_rect)

        draw_button(btn_select, "Seleccionar Oponente")
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
        # Verificar si el tiempo de partida ha finalizado
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - game_start_time
        if elapsed_time >= game_duration:
            state = 'game_over'
        else:
            # Actualización de la lógica del juego Pong para cada bola
            for ball in balls:
                ball['rect'].x += ball['speed_x']
                ball['rect'].y += ball['speed_y']

                # Colisión con la parte superior e inferior
                if ball['rect'].top <= 0 or ball['rect'].bottom >= screen_height:
                    ball['speed_y'] *= -1

                # Colisión con los bordes izquierdo y derecho y actualización de puntuación
                if ball['rect'].left <= 0 or ball['rect'].right >= screen_width:
                    if ball['rect'].left <= 0:
                        # La bola tocó la pared enemiga (lado izquierdo): punto para el jugador (lado derecho)
                        player_score += 1
                    if ball['rect'].right >= screen_width:
                        # La bola tocó la pared del jugador: punto para el oponente (lado izquierdo)
                        opponent_score += 1

                    # Reiniciar la bola en el centro con nuevas direcciones aleatorias
                    ball['rect'].center = (screen_width / 2, screen_height / 2)
                    ball['speed_x'] = 7 * random.choice((1, -1))
                    ball['speed_y'] = 7 * random.choice((1, -1))

                # Colisiones con las palas:
                # Si la bola colisiona con la pala del jugador (lado derecho), se asegura que se mueva hacia la izquierda.
                if ball['rect'].colliderect(player):
                    ball['speed_x'] = -abs(ball['speed_x'])
                # Si la bola colisiona con la pala del oponente (lado izquierdo), se asegura que se mueva hacia la derecha.
                if ball['rect'].colliderect(opponent):
                    ball['speed_x'] = abs(ball['speed_x'])

            # Actualización del jugador y del oponente
            player.y += player_speed
            if player.top < 0:
                player.top = 0
            if player.bottom > screen_height:
                player.bottom = screen_height

            # Movimiento del oponente según el tipo seleccionado
            if opponent_type == 'IA':
                if opponent.top < balls[0]['rect'].y:
                    opponent.top += opponent_speed
                if opponent.bottom > balls[0]['rect'].y:
                    opponent.bottom -= opponent_speed
            else:  # Control manual para el jugador oponente
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    opponent.y -= opponent_speed
                if keys[pygame.K_s]:
                    opponent.y += opponent_speed
            if opponent.top < 0:
                opponent.top = 0
            if opponent.bottom > screen_height:
                opponent.bottom = screen_height

            # Comprobación para añadir una bola extra cada 10 puntos totales
            total_points = player_score + opponent_score
            if total_points // 10 + 1 > len(balls):
                balls.append(create_ball())

            # Dibujo de elementos en pantalla
            screen.fill(bg_color)
            pygame.draw.rect(screen, light_grey, player)
            pygame.draw.rect(screen, light_grey, opponent)
            for ball in balls:
                pygame.draw.ellipse(screen, light_grey, ball['rect'])
            pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))
            score_text = font_medium.render(f"{opponent_score}  -  {player_score}", True, light_grey)
            score_rect = score_text.get_rect(center=(screen_width / 2, 30))
            screen.blit(score_text, score_rect)

            # Se muestra el tiempo restante en la esquina superior derecha
            remaining_time = max(0, game_duration - elapsed_time)
            minutes = remaining_time // 60000
            seconds = (remaining_time % 60000) // 1000
            timer_text = font_medium.render(f"{minutes:02}:{seconds:02}", True, light_grey)
            timer_rect = timer_text.get_rect(topright=(screen_width - 20, 20))
            screen.blit(timer_text, timer_rect)

    elif state == 'game_over':
        # Pantalla final: se muestra el resultado y un botón de salida
        screen.fill(bg_color)
        # Determinar el resultado de la partida
        if player_score > opponent_score:
            result_text = "Ganó el Jugador"
        elif opponent_score > player_score:
            result_text = "Ganó el Oponente"
        else:
            result_text = "Empate"
        result_surface = font_large.render(result_text, True, light_grey)
        result_rect = result_surface.get_rect(center=(screen_width // 2, screen_height // 3))
        screen.blit(result_surface, result_rect)
        # Mostrar el marcador final
        score_surface = font_medium.render(f"{opponent_score}  -  {player_score}", True, light_grey)
        score_rect = score_surface.get_rect(center=(screen_width // 2, screen_height // 3 + 60))
        screen.blit(score_surface, score_rect)
        # Dibujar el botón de salida
        draw_button(btn_exit_game, "Salir")

    pygame.display.flip()
    clock.tick(60)
