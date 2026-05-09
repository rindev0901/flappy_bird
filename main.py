import pygame
from random import randint

pygame.init()
pygame.mixer.init()

jump_sound = pygame.mixer.Sound("jump.mp3")
score_sound = pygame.mixer.Sound("score.mp3")
hit_sound = pygame.mixer.Sound("hit.mp3")

# SCREEN
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
icon = pygame.image.load("bird.png")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
pygame.display.set_icon(icon)

# FPS
clock = pygame.time.Clock()
FPS = 60

# COLORS
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)

# TUBE
TUBE_WIDTH = 50
TUBE_HEIGHT_MIN = 100
TUBE_HEIGHT_MAX = 400
TUBE_SPACE_VERTICAL = 150
TUBE_VELOCITY = 3

# BIRD
GRAVITY = 0.5
JUMP_STRENGTH = -8
BIRD_WIDTH = 30
BIRD_HEIGHT = 30

font = pygame.font.SysFont(None, 50)
score = 0

# ===================== TUBE =====================
class Tube:
    def __init__(self, x: int):
        self.x = x
        self.passed = False  # 👈 thêm cái này
        self.reset()

    def reset(self):
        self.top_height = randint(TUBE_HEIGHT_MIN, TUBE_HEIGHT_MAX)
        self.bottom_y = self.top_height + TUBE_SPACE_VERTICAL
        self.bottom_height = SCREEN_HEIGHT - self.bottom_y
        self.passed = False   # 👈 reset lại

    def update(self):
        self.x -= TUBE_VELOCITY

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x, 0, TUBE_WIDTH, self.top_height))
        pygame.draw.rect(screen, BLUE, (self.x, self.bottom_y, TUBE_WIDTH, self.bottom_height))

    def collide(self, rect):
        top = pygame.Rect(self.x, 0, TUBE_WIDTH, self.top_height)
        bottom = pygame.Rect(self.x, self.bottom_y, TUBE_WIDTH, self.bottom_height)
        return rect.colliderect(top) or rect.colliderect(bottom)


# ===================== BIRD =====================
class Bird:
    def __init__(self):
        self.x = 100
        self.y = 300
        self.velocity = 0

        self.image = pygame.image.load("bird.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (BIRD_WIDTH, BIRD_HEIGHT))

    def getRect(self):
        return pygame.Rect(self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT)

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def draw(self, screen):
        angle = max(-45, min(25, -self.velocity * 3))

        rotated = pygame.transform.rotate(self.image, angle)
        rect = rotated.get_rect(center=(self.x + BIRD_WIDTH // 2, self.y + BIRD_HEIGHT // 2))

        screen.blit(rotated, rect)


# ===================== GAME RESET =====================
def reset_game():
    bird = Bird()
    tubes = [
        Tube(200),
        Tube(350),
        Tube(500)
    ]
    return bird, tubes


bird, tubes = reset_game()
is_game_over = False


# ===================== GAME LOOP =====================
running = True
while running:
    clock.tick(FPS)
    screen.fill(GREEN)

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_game_over:
                bird.jump()
                jump_sound.play()

            if event.key == pygame.K_r and is_game_over:
                bird, tubes = reset_game()
                is_game_over = False
                score = 0
    
    # UPDATE
    if not is_game_over:
        bird.update()

        for tube in tubes:
            tube.update()
            if not tube.passed and tube.x + TUBE_WIDTH < bird.x:
                score += 1
                tube.passed = True
                score_sound.play()

            if tube.x < -TUBE_WIDTH:
                tube.x = max(t.x for t in tubes) + 150
                tube.reset()

            if tube.collide(bird.getRect()):
                hit_sound.play()
                is_game_over = True
    
    # DRAW TUBES
    for tube in tubes:
        tube.draw(screen)

    # DRAW BIRD
    bird.draw(screen)
    
    score_text = font.render(str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # GAME OVER UI
    if is_game_over:
        text = font.render("GAME OVER - R to restart", True, (255, 255, 255))
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, rect)

    pygame.display.flip()

pygame.quit()