import pygame, sys, random

# Inicialización de Pygame y constantes globales
pygame.init()


# CONSTANTES Y CONFIGURACIONES

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 760
FPS = 60

# Tamaños de las palas
DEFAULT_PADDLE_HEIGHT = 140
ENLARGED_PADDLE_HEIGHT = 200
PADDLE_WIDTH = 10

# Colores
BG_COLOR = pygame.Color('grey12')
LIGHT_GREY = (200, 200, 200)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
STAR_COLOR = (255, 255, 255)

# Fuentes
font_large = pygame.font.Font(None, 74)
font_medium = pygame.font.Font(None, 50)

# Ventana
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong - Versión Mejorada")
clock = pygame.time.Clock()


# VARIABLES DE ESTADO DEL JUEGO

# Estados posibles: 'menu', 'select', 'game', 'game_over'
state = 'menu'
opponent_type = 'IA'  # Valor por defecto

# Botones del menú principal
btn_select = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100, 400, 80)
btn_exit = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 20, 300, 60)
# Botones de selección de oponente
btn_ia = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100, 300, 60)
btn_player = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 20, 300, 60)
# Botón en la pantalla de Game Over
btn_exit_game = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 80, 300, 60)

# Límite de puntos para finalizar la partida
POINTS_LIMIT = 100


# VARIABLES EXTRA: Fondo animado y Power-Up

# Fondo animado: generamos una lista de "estrellas" con posiciones y velocidades
NUM_STARS = 50
stars = []
for _ in range(NUM_STARS):
    x = random.randrange(0, SCREEN_WIDTH)
    y = random.randrange(0, SCREEN_HEIGHT)
    radius = random.choice([1, 2, 3])
    speed = random.uniform(0.5, 1.5)
    stars.append({'x': x, 'y': y, 'r': radius, 'speed': speed})

# Power-Up: Aparece de forma aleatoria cada 5-10 segundos y dura 5 segundos
powerup = None
powerup_active_time = 5000  # Duración en milisegundos
powerup_next_spawn = pygame.time.get_ticks() + random.randint(5000, 10000)


# VARIABLES DE ENLARGAMIENTO TEMPORAL DE PALAS

player_enlarged_until = 0
opponent_enlarged_until = 0


# FUNCIONES AUXILIARES

def draw_button(rect, text):
    # Dibuja un botón con borde redondeado y centra el texto.
    pygame.draw.rect(screen, LIGHT_GREY, rect, border_radius=5)
    text_surface = font_medium.render(text, True, BG_COLOR)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def create_ball():
    # Crea y devuelve un diccionario que representa una bola con posición y velocidad aleatoria.
    return {
        'rect': pygame.Rect(SCREEN_WIDTH / 2 - 15, SCREEN_HEIGHT / 2 - 15, 30, 30),
        'speed_x': 7 * random.choice((1, -1)),
        'speed_y': 7 * random.choice((1, -1))
    }

def spawn_powerup():
    # Genera un power-up en una posición aleatoria.
    size = 20
    x = random.randint(SCREEN_WIDTH // 4, SCREEN_WIDTH * 3 // 4)
    y = random.randint(50, SCREEN_HEIGHT - 50)
    # El power-up se representa con un rectángulo (se dibujará como círculo)
    return {
        'rect': pygame.Rect(x, y, size, size),
        'spawn_time': pygame.time.get_ticks()  # Momento en el que aparece
    }

def update_stars():
    # Actualiza la posición de las estrellas para crear un efecto de fondo en movimiento.
    for star in stars:
        star['y'] += star['speed']
        if star['y'] > SCREEN_HEIGHT:
            star['y'] = 0
            star['x'] = random.randrange(0, SCREEN_WIDTH)

def draw_stars():
    # Dibuja las estrellas en el fondo.
    for star in stars:
        pygame.draw.circle(screen, STAR_COLOR, (int(star['x']), int(star['y'])), star['r'])

def reset_paddle_size(paddle, original_height=DEFAULT_PADDLE_HEIGHT):
    # Reinicia el tamaño de la pala manteniendo su centro.
    center = paddle.centery
    paddle.height = original_height
    paddle.centery = center


# INICIALIZACIÓN DEL JUEGO

def init_game():
    # Inicializa o reinicia los elementos del juego.
    global balls, player, opponent, player_speed, opponent_speed, player_score, opponent_score
    global player_enlarged_until, opponent_enlarged_until, powerup, powerup_next_spawn
    balls = [create_ball()]  # Se inicia con una bola
    # Se crean las palas con altura por defecto
    player = pygame.Rect(SCREEN_WIDTH - 20, SCREEN_HEIGHT / 2 - DEFAULT_PADDLE_HEIGHT // 2, PADDLE_WIDTH, DEFAULT_PADDLE_HEIGHT)
    opponent = pygame.Rect(10, SCREEN_HEIGHT / 2 - DEFAULT_PADDLE_HEIGHT // 2, PADDLE_WIDTH, DEFAULT_PADDLE_HEIGHT)
    player_speed = 0  # Velocidad de la pala del jugador
    opponent_speed = 7  # Velocidad inicial de la IA (oponente)
    player_score = 0
    opponent_score = 0
    # Reiniciar power-up y timers de ampliación
    player_enlarged_until = 0
    opponent_enlarged_until = 0
    powerup = None
    powerup_next_spawn = pygame.time.get_ticks() + random.randint(5000, 10000)

# Inicialización de la partida
init_game()


# BUCLE PRINCIPAL DEL JUEGO

while True:
    current_time = pygame.time.get_ticks()  # Tiempo actual para gestionar eventos temporales

    # Captura y gestión de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # MENÚ PRINCIPAL
        if state == 'menu':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_select.collidepoint(event.pos):
                    state = 'select'
                elif btn_exit.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        # SELECCIÓN DE OPONENTE
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
        # PARTIDA EN JUEGO
        elif state == 'game':
            if event.type == pygame.KEYDOWN:
                # Controles para la pala del jugador (lado derecho)
                if event.key == pygame.K_DOWN:
                    player_speed += 7
                if event.key == pygame.K_UP:
                    player_speed -= 7
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_speed -= 7
                if event.key == pygame.K_UP:
                    player_speed += 7
        # PANTALLA DE GAME OVER
        elif state == 'game_over':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_exit_game.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


    # ACTUALIZACIONES SEGÚN EL ESTADO

    # Actualizar fondo animado (estrellas)
    update_stars()

    if state == 'menu':
        screen.fill(BG_COLOR)
        draw_stars()  # Fondo animado
        title_surface = font_large.render("PONG", True, LIGHT_GREY)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_surface, title_rect)
        draw_button(btn_select, "Seleccionar Oponente")
        draw_button(btn_exit, "Salir")

    elif state == 'select':
        screen.fill(BG_COLOR)
        draw_stars()
        title_surface = font_large.render("Elige el oponente", True, LIGHT_GREY)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_surface, title_rect)
        draw_button(btn_ia, "IA")
        draw_button(btn_player, "Jugador")

    elif state == 'game':

        # GESTIÓN DE POWER-UP

        if powerup is None and current_time >= powerup_next_spawn:
            powerup = spawn_powerup()
        # Si el powerup ha estado en pantalla más de 5 segundos sin ser recogido, desaparece
        if powerup is not None and current_time - powerup['spawn_time'] > powerup_active_time:
            powerup = None
            powerup_next_spawn = current_time + random.randint(5000, 10000)


        # ACTUALIZACIÓN DE BOLAS Y COLISIONES

        for ball in balls:
            ball['rect'].x += ball['speed_x']
            ball['rect'].y += ball['speed_y']

            # Rebote en techo y suelo
            if ball['rect'].top <= 0 or ball['rect'].bottom >= SCREEN_HEIGHT:
                ball['speed_y'] *= -1

            # Colisión con los laterales: Se actualiza la puntuación y se reinicia la bola
            if ball['rect'].left <= 0 or ball['rect'].right >= SCREEN_WIDTH:
                if ball['rect'].left <= 0:
                    # Punto para el jugador (lado derecho)
                    player_score += 1
                    if opponent_type == 'IA':
                        opponent_speed += 0.5  # Incrementa dificultad
                if ball['rect'].right >= SCREEN_WIDTH:
                    # Punto para el oponente (lado izquierdo)
                    opponent_score += 1
                    if opponent_type == 'IA':
                        opponent_speed += 0.5

                # Reiniciar la bola en el centro con dirección aleatoria
                ball['rect'].center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                ball['speed_x'] = 7 * random.choice((1, -1))
                ball['speed_y'] = 7 * random.choice((1, -1))

            # Colisiones con palas: se garantiza el rebote en la dirección correcta
            if ball['rect'].colliderect(player):
                ball['speed_x'] = -abs(ball['speed_x'])
            if ball['rect'].colliderect(opponent):
                ball['speed_x'] = abs(ball['speed_x'])


            # COLISIÓN CON POWER-UP (la bola no lo recoge, sino que la pala sí)

            if powerup is not None:
                if ball['rect'].colliderect(powerup['rect']):
                    # Si la bola toca el powerup, se asigna el efecto según la dirección de la bola
                    if ball['speed_x'] > 0:
                        # La bola se dirige a la pala del jugador (derecha)
                        player_enlarged_until = current_time + 5000  # 5 segundos de efecto
                        center = player.centery
                        player.height = ENLARGED_PADDLE_HEIGHT
                        player.centery = center
                    else:
                        # La bola se dirige al oponente (izquierda)
                        opponent_enlarged_until = current_time + 5000
                        center = opponent.centery
                        opponent.height = ENLARGED_PADDLE_HEIGHT
                        opponent.centery = center
                    # Se elimina el powerup y se programa la siguiente aparición
                    powerup = None
                    powerup_next_spawn = current_time + random.randint(5000, 10000)


        # ACTUALIZACIÓN DE PALAS

        player.y += player_speed
        if player.top < 0:
            player.top = 0
        if player.bottom > SCREEN_HEIGHT:
            player.bottom = SCREEN_HEIGHT

        # Movimiento del oponente según el tipo seleccionado
        if opponent_type == 'IA':
            if opponent.centery < balls[0]['rect'].centery:
                opponent.y += opponent_speed
            if opponent.centery > balls[0]['rect'].centery:
                opponent.y -= opponent_speed
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                opponent.y -= opponent_speed
            if keys[pygame.K_s]:
                opponent.y += opponent_speed

        if opponent.top < 0:
            opponent.top = 0
        if opponent.bottom > SCREEN_HEIGHT:
            opponent.bottom = SCREEN_HEIGHT


        # GESTIÓN DE MULTIBOLAS

        total_points = player_score + opponent_score
        if total_points // 10 + 1 > len(balls):
            balls.append(create_ball())


        # REINICIAR EL TAMAÑO DE PALAS SI SE ACABA EL POWER-UP

        if current_time > player_enlarged_until and player.height != DEFAULT_PADDLE_HEIGHT:
            reset_paddle_size(player)
        if current_time > opponent_enlarged_until and opponent.height != DEFAULT_PADDLE_HEIGHT:
            reset_paddle_size(opponent)


        # DIBUJO DE ELEMENTOS EN PANTALLA

        screen.fill(BG_COLOR)
        draw_stars()
        pygame.draw.rect(screen, RED, player)
        pygame.draw.rect(screen, RED, opponent)
        for ball in balls:
            pygame.draw.ellipse(screen, YELLOW, ball['rect'])
        pygame.draw.aaline(screen, LIGHT_GREY, (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))
        score_text = font_medium.render(f"{opponent_score}  -  {player_score}", True, LIGHT_GREY)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        screen.blit(score_text, score_rect)
        # Dibujar power-up como círculo
        if powerup is not None:
            pygame.draw.ellipse(screen, GREEN, powerup['rect'])

        if player_score >= POINTS_LIMIT or opponent_score >= POINTS_LIMIT:
            state = 'game_over'

    elif state == 'game_over':
        screen.fill(BG_COLOR)
        draw_stars()
        if player_score > opponent_score:
            result_text = "Ganó el Jugador"
        elif opponent_score > player_score:
            result_text = "Ganó el Oponente"
        else:
            result_text = "Empate"
        result_surface = font_large.render(result_text, True, LIGHT_GREY)
        result_rect = result_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(result_surface, result_rect)
        score_surface = font_medium.render(f"{opponent_score}  -  {player_score}", True, LIGHT_GREY)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 60))
        screen.blit(score_surface, score_rect)
        draw_button(btn_exit_game, "Salir")

    pygame.display.flip()
    clock.tick(FPS)
