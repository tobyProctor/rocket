import math
import turtle
import time
import pygame
import sys

# Global defs
pygame.init()
TICKER_SPEED = 0.02
SCREEN_RES_X = 1400
SCREEN_RES_Y = 900

# Solar System Bodies
class SolarSystemBody(turtle.Turtle):
    min_display_size = 20
    display_log_base = 1.1

    def __init__(
            self,
            solar_system,
            mass,
            position=(0, 0),
            velocity=(0, 0),
    ):
        super().__init__()
        self.mass = mass
        self.setposition(position)
        self.velocity = velocity
        self.display_size = max(
            math.log(self.mass, self.display_log_base),
            self.min_display_size,
        )
        solar_system.add_body(self)

    def clear(self):
        pygame.display.update()
        

    def draw(self, screen):
        self.clear()
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (0, 0, 255), (self.xcor(), self.ycor()), 10)

    def move(self):
        self.setx(self.xcor() + self.velocity[0])
        self.sety(self.ycor() + self.velocity[1])


class Sun(SolarSystemBody):
    def __init__(
            self,
            solar_system,
            mass,
            position=(0, 0),
            velocity=(0, 0),
    ):
        super().__init__(solar_system, mass, position, velocity)


class Planet(SolarSystemBody):

    def __init__(
            self,
            solar_system,
            mass,
            position=(0, 0),
            velocity=(0, 0),
    ):
        super().__init__(solar_system, mass, position, velocity)


# Solar System
class SolarSystem:
    def __init__(self, width, height):
        self.solar_system = turtle.Screen()
        self.solar_system.setup(1, 1)

        self.screen = pygame.display.set_mode([width, height])
        self.screen.fill((0, 0, 0))

        self.bodies = []

    def add_body(self, body):
        self.bodies.append(body)

    def remove_body(self, body):
        body.clear()
        self.bodies.remove(body)

    def update_all(self):
        for body in self.bodies:
            body.move()
            body.draw(self.screen)            

    @staticmethod
    def accelerate_due_to_gravity(
            first: SolarSystemBody,
            second: SolarSystemBody,
    ):
        force = first.mass * second.mass / first.distance(second) ** 2
        angle = first.towards(second)
        reverse = 1
        for body in first, second:
            acceleration = force / body.mass
            acc_x = acceleration * math.cos(math.radians(angle))
            acc_y = acceleration * math.sin(math.radians(angle))
            body.velocity = (
                body.velocity[0] + (reverse * acc_x),
                body.velocity[1] + (reverse * acc_y),
            )
            reverse = -1

    def check_collision(self, first, second):
        if isinstance(first, Planet) and isinstance(second, Planet):
            return
        if first.distance(second) < first.display_size/2 + second.display_size/2:
            for body in first, second:
                if isinstance(body, Planet):
                    self.remove_body(body)

    def calculate_all_body_interactions(self):
        bodies_copy = self.bodies.copy()
        for idx, first in enumerate(bodies_copy):
            for second in bodies_copy[idx + 1:]:
                self.accelerate_due_to_gravity(first, second)
                self.check_collision(first, second)


def main():
    solar_system = SolarSystem(width=SCREEN_RES_X, height=SCREEN_RES_Y)

    sun = Sun(solar_system, mass=10_000, position=(SCREEN_RES_X/2, SCREEN_RES_Y/2))
    planets = (
        Planet(
            solar_system,
            mass=1,
            position=(350, 450),
            velocity=(0, 5),
        ),
        Planet(
            solar_system,
            mass=2,
            position=(430, 450),
            velocity=(0, 7),
        ),
    )

    while True:
        # Game loop tick 60Hz
        time.sleep(TICKER_SPEED)

        # Exit on close button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        solar_system.calculate_all_body_interactions()
        solar_system.update_all()

if __name__ == "__main__":
    main()