import pygame
from typing import Tuple, Union
from random import randint

# Khởi tạo instance
pygame.init()

# Tạo window
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Detect game còn chạy hay không
running = True


# Tạo FPS
clock = pygame.time.Clock() 
FPS = 60

# Colors
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)

# TUBE Value
TUBE_WIDTH = 50
TUBE_HEIGHT_MIN = 100
TUBE_HEIGHT_MAX = 400
TUBE_SPACE_VERTICAL = 150
TUBE_SPACE_HORIZONTAL = 150
TUBE_VELOCITY = 3

# TUBE Coordinate
class Tube:
    def __init__(self, tube_x: int, tube_y: int, tube_height: int | None = None):
        self.tube_x = tube_x
        self.tube_height = randint(TUBE_HEIGHT_MIN, TUBE_HEIGHT_MAX) if tube_height is None else tube_height
        self.tube_y = tube_y if tube_y >= 0 else SCREEN_HEIGHT - self.tube_height
    
    def getRect(self) -> Tuple[Union[float, int], Union[float, int], Union[float, int], Union[float, int]]:
        return (self.tube_x, self.tube_y, TUBE_WIDTH, self.tube_height)
    
    def calcVelocity(self) -> None:
        self.tube_x -= TUBE_VELOCITY

# Tạo Tubes
tube_1_top = Tube(200, 0)
tube_2_top = Tube(TUBE_WIDTH + TUBE_SPACE_HORIZONTAL + tube_1_top.tube_x, 0)
tube_3_top = Tube(TUBE_WIDTH + TUBE_SPACE_HORIZONTAL + tube_2_top.tube_x, 0)

tube_1_bot = Tube(200, -1, SCREEN_HEIGHT - TUBE_SPACE_VERTICAL - tube_1_top.tube_height)
tube_2_bot = Tube(TUBE_WIDTH + TUBE_SPACE_HORIZONTAL + tube_1_bot.tube_x, -1, SCREEN_HEIGHT - TUBE_SPACE_VERTICAL - tube_2_top.tube_height)
tube_3_bot = Tube(TUBE_WIDTH + TUBE_SPACE_HORIZONTAL + tube_2_bot.tube_x, -1, SCREEN_HEIGHT - TUBE_SPACE_VERTICAL - tube_3_top.tube_height)

while running:
    clock.tick(FPS) # Draw 60 frame trên 1 giây
    screen.fill(GREEN)
    
    pygame.draw.rect(screen, BLUE, tube_1_top.getRect())
    pygame.draw.rect(screen, BLUE, tube_2_top.getRect())
    pygame.draw.rect(screen, BLUE, tube_3_top.getRect())
    
    pygame.draw.rect(screen, BLUE, tube_1_bot.getRect())
    pygame.draw.rect(screen, BLUE, tube_2_bot.getRect())
    pygame.draw.rect(screen, BLUE, tube_3_bot.getRect())
    
    tube_1_top.calcVelocity()
    tube_2_top.calcVelocity()
    tube_3_top.calcVelocity()
    
    tube_1_bot.calcVelocity()
    tube_2_bot.calcVelocity()
    tube_3_bot.calcVelocity()
    
    if tube_1_top.tube_x <= -TUBE_WIDTH:
        tube_1_top.tube_x = TUBE_WIDTH + TUBE_SPACE_HORIZONTAL + tube_3_top.tube_x
        tube_1_top.tube_height = randint(TUBE_HEIGHT_MIN, TUBE_HEIGHT_MAX)
    
    if tube_2_top.tube_x <= -TUBE_WIDTH:
        tube_2_top.tube_x = TUBE_WIDTH + TUBE_SPACE_HORIZONTAL + tube_1_top.tube_x
        tube_2_top.tube_height = randint(TUBE_HEIGHT_MIN, TUBE_HEIGHT_MAX)
    
    if tube_3_top.tube_x <= -TUBE_WIDTH:
        tube_3_top.tube_x = TUBE_WIDTH + TUBE_SPACE_HORIZONTAL + tube_2_top.tube_x
        tube_3_top.tube_height = randint(TUBE_HEIGHT_MIN, TUBE_HEIGHT_MAX)
    
    if tube_1_bot.tube_x <= -TUBE_WIDTH:
        tube_1_bot.tube_x = TUBE_WIDTH + TUBE_SPACE_HORIZONTAL + tube_3_bot.tube_x
        tube_1_bot.tube_height = SCREEN_HEIGHT - TUBE_SPACE_VERTICAL - tube_1_top.tube_height
        tube_1_bot.tube_y = SCREEN_HEIGHT - tube_1_bot.tube_height
        
    if tube_2_bot.tube_x <= -TUBE_WIDTH:
        tube_2_bot.tube_x = TUBE_WIDTH + TUBE_SPACE_HORIZONTAL + tube_1_bot.tube_x
        tube_2_bot.tube_height = SCREEN_HEIGHT - TUBE_SPACE_VERTICAL - tube_2_top.tube_height
        tube_2_bot.tube_y = SCREEN_HEIGHT - tube_2_bot.tube_height
        
    if tube_3_bot.tube_x <= -TUBE_WIDTH:
        tube_3_bot.tube_x = TUBE_WIDTH + TUBE_SPACE_HORIZONTAL + tube_2_bot.tube_x
        tube_3_bot.tube_height = SCREEN_HEIGHT - TUBE_SPACE_VERTICAL - tube_3_top.tube_height
        tube_3_bot.tube_y = SCREEN_HEIGHT - tube_3_bot.tube_height
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Cập nhật draw
    pygame.display.flip()
    
pygame.quit()