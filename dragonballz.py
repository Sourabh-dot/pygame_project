import pygame

pygame.font.init()

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DragonBall Z")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOKU_POWER_COLOR = (51, 255, 255)
JIREN_POWER_COLOR = (255, 69, 0)
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
FPS = 60
BULLET_VEL = 7
MAX_BULLETS = 2
VEL = 5
CHARACTER_HEIGHT, CHARACTER_WIDTH = 90, 70
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

GOKU_HIT = pygame.USEREVENT + 1
JIREN_HIT = pygame.USEREVENT + 2

GOKU_IMAGE = pygame.image.load('Assets/goku.png')
GOKU = pygame.transform.scale(GOKU_IMAGE, (CHARACTER_HEIGHT, CHARACTER_WIDTH))
JIREN_IMAGE = pygame.image.load('Assets/jiren.png')
JIREN = pygame.transform.scale(JIREN_IMAGE, (CHARACTER_HEIGHT, CHARACTER_WIDTH))
TOURNAMENT_IMAGE = pygame.image.load('Assets/tournament.png')
TOURNAMENT = pygame.transform.scale(TOURNAMENT_IMAGE, (WIDTH, HEIGHT))


def goku_keypad(goku, key_pressed):
    if key_pressed[pygame.K_a] and goku.x - VEL > 0:
        goku.x -= VEL
    if key_pressed[pygame.K_d] and goku.x + VEL + goku.width < BORDER.x - 10:
        goku.x += VEL
    if key_pressed[pygame.K_s] and goku.y + VEL + goku.height < HEIGHT:
        goku.y += VEL
    if key_pressed[pygame.K_w] and goku.y - VEL > 0:
        goku.y -= VEL


def handle_power(goku_power, jiren_power, goku, jiren):
    for bullet in goku_power:
        bullet.x += BULLET_VEL
        if jiren.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GOKU_HIT))
            goku_power.remove(bullet)
        elif bullet.x > WIDTH:
            goku_power.remove(bullet)
    for bullet in jiren_power:
        bullet.x -= BULLET_VEL
        if goku.colliderect(bullet):
            pygame.event.post(pygame.event.Event(JIREN_HIT))
            jiren_power.remove(bullet)
        elif bullet.x < 0:
            jiren_power.remove(bullet)


def jiren_keypad(jiren, key_pressed):
    if key_pressed[pygame.K_LEFT] and jiren.x - VEL > BORDER.x + 10:
        jiren.x -= VEL
    if key_pressed[pygame.K_RIGHT] and jiren.x + VEL + jiren.width < WIDTH:
        jiren.x += VEL
    if key_pressed[pygame.K_DOWN] and jiren.y + VEL + jiren.height < HEIGHT:
        jiren.y += VEL
    if key_pressed[pygame.K_UP] and jiren.y - VEL > 0:
        jiren.y -= VEL


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, True, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)


def draw_window(goku, jiren, goku_power, jiren_power, goku_health, jiren_health):
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(TOURNAMENT, (0, 0))
    goku_health_text = HEALTH_FONT.render("HEALTH :" + str(goku_health), True, WHITE)
    jiren_health_text = HEALTH_FONT.render("HEALTH :" + str(jiren_health), True, WHITE)
    WIN.blit(jiren_health_text, (WIDTH - jiren_health_text.get_width() - 10, 10))
    WIN.blit(goku_health_text, (10, 10))
    WIN.blit(GOKU, (goku.x, goku.y))
    WIN.blit(JIREN, (jiren.x, jiren.y))
    for bullet in goku_power:
        pygame.draw.rect(WIN, GOKU_POWER_COLOR, bullet)
    for bullet in jiren_power:
        pygame.draw.rect(WIN, JIREN_POWER_COLOR, bullet)
    pygame.display.update()


def main():
    run = True
    goku = pygame.Rect(100, 300, CHARACTER_HEIGHT, CHARACTER_WIDTH)
    jiren = pygame.Rect(700, 300, CHARACTER_HEIGHT, CHARACTER_WIDTH)
    clock = pygame.time.Clock()
    goku_power = []
    jiren_power = []
    goku_health = 100
    jiren_health = 100
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(goku_power) < MAX_BULLETS:
                    bullet = pygame.Rect(goku.x + goku.width, goku.y + goku.height // 2 - 2, 20, 10)
                    goku_power.append(bullet)
                if event.key == pygame.K_RCTRL and len(jiren_power) < MAX_BULLETS:
                    bullet = pygame.Rect(jiren.x, jiren.y + jiren.height // 2 - 2, 20, 10)
                    jiren_power.append(bullet)
            if event.type == GOKU_HIT:
                jiren_health -= 10
            if event.type == JIREN_HIT:
                goku_health -= 10

        winner_text = ""
        if goku_health <= 0:
            winner_text = "JIREN WON!!"
        if jiren_health <= 0:
            winner_text = "GOKU WON!!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        key_pressed = pygame.key.get_pressed()
        goku_keypad(goku, key_pressed)
        jiren_keypad(jiren, key_pressed)
        handle_power(goku_power, jiren_power, goku, jiren)
        draw_window(goku, jiren, goku_power, jiren_power, goku_health, jiren_health)

    pygame.quit()


if __name__ == "__main__":
    main()
