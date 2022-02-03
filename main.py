import pygame
import sys
import time
import math

# Game Vars
SCREEN_RES_X = 1000
SCREEN_RES_Y = 1000
GRAVITY = 9.8
TICKER_SPEED = 0.01
game_objects = []
ticker = 0

# PyGame Init
pygame.init()
screen = pygame.display.set_mode([SCREEN_RES_X, SCREEN_RES_Y])

def update_objects():
    for obj in game_objects:
        obj.update()

# Object classes
class ball(object):
    def __init__(self, init_x, init_y, speed, mass=1, stationary=False):
        self.x          = init_x
        self.y          = init_y
        self.init_y     = init_y
        self.speed      = speed
        self.mass       = mass
        self.time_alive = 0
        self.stationary = stationary

        game_objects.append(self)

    def draw(self, x, y):
        pygame.draw.circle(screen, (0, 0, 255), (x, y), 10)        

    def update(self):
        self.time_alive = self.time_alive + TICKER_SPEED
        # vf = g * t
        if not self.stationary:
            self.y = self.y + self.get_velocity()
            print(self.get_velocity())
        self.draw(self.x, self.y)

    def get_velocity(self):
        for obj in game_objects:
            dist = math.dist((self.x, self.y), (obj.x, obj.y))
            if dist > 0:
                force = GRAVITY*((self.mass*obj.mass)/dist**2)
                acc = force / self.mass
                return acc


# initialise objects
ball_0 = ball(500, 0, 1)
ball_1 = ball(SCREEN_RES_Y/2, SCREEN_RES_X/2, 0, 1000, True)

while True:
    # Game loop tick 60Hz
    ticker = ticker + 1
    time.sleep(TICKER_SPEED)

    # Exit on close button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((255, 255, 255))

    # Update all game objects
    update_objects()

    pygame.display.flip()