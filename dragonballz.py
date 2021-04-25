import pygame

pygame.font.init()


class GameAttributes:
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


class CharacterControl:
    def __init__(self):
        super().__init__()
        self.attributes = GameAttributes()

    def goku_keypad(self, goku, key_pressed):
        if key_pressed[pygame.K_a] and goku.x - self.attributes.VEL > 0:
            goku.x -= self.attributes.VEL
        if key_pressed[pygame.K_d] and goku.x + self.attributes.VEL + goku.width < self.attributes.BORDER.x - 10:
            goku.x += self.attributes.VEL
        if key_pressed[pygame.K_s] and goku.y + self.attributes.VEL + goku.height < self.attributes.HEIGHT:
            goku.y += self.attributes.VEL
        if key_pressed[pygame.K_w] and goku.y - self.attributes.VEL > 0:
            goku.y -= self.attributes.VEL

    def handle_power(self, goku_power, jiren_power, goku, jiren):
        for bullet in goku_power:
            bullet.x += self.attributes.BULLET_VEL
            if jiren.colliderect(bullet):
                pygame.event.post(pygame.event.Event(self.attributes.GOKU_HIT))
                goku_power.remove(bullet)
            elif bullet.x > self.attributes.WIDTH:
                goku_power.remove(bullet)
        for bullet in jiren_power:
            bullet.x -= self.attributes.BULLET_VEL
            if goku.colliderect(bullet):
                pygame.event.post(pygame.event.Event(self.attributes.JIREN_HIT))
                jiren_power.remove(bullet)
            elif bullet.x < 0:
                jiren_power.remove(bullet)

    def jiren_keypad(self, jiren, key_pressed):
        if key_pressed[pygame.K_LEFT] and jiren.x - self.attributes.VEL > self.attributes.BORDER.x + 10:
            jiren.x -= self.attributes.VEL
        if key_pressed[pygame.K_RIGHT] and jiren.x + self.attributes.VEL + jiren.width < self.attributes.WIDTH:
            jiren.x += self.attributes.VEL
        if key_pressed[pygame.K_DOWN] and jiren.y + self.attributes.VEL + jiren.height < self.attributes.HEIGHT:
            jiren.y += self.attributes.VEL
        if key_pressed[pygame.K_UP] and jiren.y - self.attributes.VEL > 0:
            jiren.y -= self.attributes.VEL


class Window:
    def __init__(self) -> None:
        super().__init__()
        self.attributes = GameAttributes()

    def draw_winner(self, text):
        draw_text = self.attributes.WINNER_FONT.render(text, True, self.attributes.WHITE)
        self.attributes.WIN.blit(draw_text, (self.attributes.WIDTH // 2 - draw_text.get_width() // 2,
                                             self.attributes.HEIGHT // 2 - draw_text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(5000)

    def draw_window(self, goku, jiren, goku_power, jiren_power, goku_health, jiren_health):
        pygame.draw.rect(self.attributes.WIN, self.attributes.BLACK, self.attributes.BORDER)
        self.attributes.WIN.blit(self.attributes.TOURNAMENT, (0, 0))
        goku_health_text = self.attributes.HEALTH_FONT.render("HEALTH :" + str(goku_health), True,
                                                              self.attributes.WHITE)
        jiren_health_text = self.attributes.HEALTH_FONT.render("HEALTH :" + str(jiren_health), True,
                                                               self.attributes.WHITE)
        self.attributes.WIN.blit(jiren_health_text, (self.attributes.WIDTH - jiren_health_text.get_width() - 10, 10))
        self.attributes.WIN.blit(goku_health_text, (10, 10))
        self.attributes.WIN.blit(self.attributes.GOKU, (goku.x, goku.y))
        self.attributes.WIN.blit(self.attributes.JIREN, (jiren.x, jiren.y))
        for bullet in goku_power:
            pygame.draw.rect(self.attributes.WIN, self.attributes.GOKU_POWER_COLOR, bullet)
        for bullet in jiren_power:
            pygame.draw.rect(self.attributes.WIN, self.attributes.JIREN_POWER_COLOR, bullet)
        pygame.display.update()


class GameLogic:
    def __init__(self):
        super().__init__()
        self.attributes = GameAttributes()
        self.control = CharacterControl()
        self.window = Window()

    def main(self):
        run = True
        goku = pygame.Rect(100, 300, self.attributes.CHARACTER_HEIGHT,
                           self.attributes.CHARACTER_WIDTH)
        jiren = pygame.Rect(700, 300, self.attributes.CHARACTER_HEIGHT,
                            self.attributes.CHARACTER_WIDTH)
        clock = pygame.time.Clock()
        goku_power = []
        jiren_power = []
        goku_health = 100
        jiren_health = 100
        while run:
            clock.tick(self.attributes.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL and len(goku_power) < self.attributes.MAX_BULLETS:
                        bullet = pygame.Rect(goku.x + goku.width, goku.y + goku.height // 2 - 2, 20, 10)
                        goku_power.append(bullet)
                    if event.key == pygame.K_RCTRL and len(jiren_power) < self.attributes.MAX_BULLETS:
                        bullet = pygame.Rect(jiren.x, jiren.y + jiren.height // 2 - 2, 20, 10)
                        jiren_power.append(bullet)
                if event.type == self.attributes.GOKU_HIT:
                    jiren_health -= 10
                if event.type == self.attributes.JIREN_HIT:
                    goku_health -= 10

            winner_text = ""
            if goku_health <= 0:
                winner_text = "JIREN WON!!"
            if jiren_health <= 0:
                winner_text = "GOKU WON!!"
            if winner_text != "":
                self.window.draw_winner(winner_text)
                break

            key_pressed = pygame.key.get_pressed()
            self.control.goku_keypad(goku, key_pressed)
            self.control.jiren_keypad(jiren, key_pressed)
            self.control.handle_power(goku_power, jiren_power, goku, jiren)
            self.window.draw_window(goku, jiren, goku_power, jiren_power, goku_health, jiren_health)

        pygame.quit()


if __name__ == "__main__":
    game = GameLogic()
    game.main()
