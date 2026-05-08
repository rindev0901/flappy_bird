import pygame
from typing import Tuple, Union
from random import randint

# Khởi tạo instance
pygame.init()

# Tạo window
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Flappy Bird")

# Detect game còn chạy hay không
running = True

# Colors
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)

# TUBE Value
TUBE_WIDTH = 50
TUBE_HEIGHT_MIN = 100
TUBE_HEIGHT_MAX = 400
TUBE_SPACING = 150
TUBE_VELOCITY = 3

# TUBE Coordinate
class Tube:
    def __init__(self, tube_x: int, tube_y: int):
        self.tube_x = tube_x
        self.tube_y = tube_y
        self.tube_height = randint(TUBE_HEIGHT_MIN, TUBE_HEIGHT_MAX)
    
    def getRect(self) -> Tuple[Union[float, int], Union[float, int], Union[float, int], Union[float, int]]:
        return (self.tube_x, self.tube_y, TUBE_WIDTH, self.tube_height)
    
    def calcVelocity(self) -> None:
        self.tube_x -= TUBE_VELOCITY

# Tạo FPS
clock = pygame.time.Clock() 
FPS = 60

# Tạo Tubes
tube_1_top = Tube(200, 0)
tube_2_top = Tube(TUBE_WIDTH + TUBE_SPACING + tube_1_top.tube_x, 0)
tube_3_top = Tube(TUBE_WIDTH + TUBE_SPACING + tube_2_top.tube_x, 0)

tube_1_bot = Tube(200, screen.get_height())

while running:
    clock.tick(FPS) # Draw 60 frame trên 1 giây
    screen.fill(GREEN)
    
    pygame.draw.rect(screen, BLUE, tube_1_top.getRect())
    pygame.draw.rect(screen, BLUE, tube_2_top.getRect())
    pygame.draw.rect(screen, BLUE, tube_3_top.getRect())
    
    pygame.draw.rect(screen, BLUE, tube_1_bot.getRect())
    
    tube_1_top.calcVelocity()
    tube_2_top.calcVelocity()
    tube_3_top.calcVelocity()
    
    if tube_1_top.tube_x <= -TUBE_WIDTH:
        tube_1_top.tube_x = TUBE_WIDTH + TUBE_SPACING + tube_3_top.tube_x
        tube_1_top.tube_height = randint(TUBE_HEIGHT_MIN, TUBE_HEIGHT_MAX)
    if tube_2_top.tube_x <= -TUBE_WIDTH:
        tube_2_top.tube_x = TUBE_WIDTH + TUBE_SPACING + tube_1_top.tube_x
        tube_2_top.tube_height = randint(TUBE_HEIGHT_MIN, TUBE_HEIGHT_MAX)
    if tube_3_top.tube_x <= -TUBE_WIDTH:
        tube_3_top.tube_x = TUBE_WIDTH + TUBE_SPACING + tube_2_top.tube_x
        tube_3_top.tube_height = randint(TUBE_HEIGHT_MIN, TUBE_HEIGHT_MAX)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Cập nhật draw
    pygame.display.flip()
    
pygame.quit()