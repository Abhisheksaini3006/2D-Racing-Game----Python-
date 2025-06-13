import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.acceleration = 0.12
        self.max_speed = 4
        self.turn_speed = 4.5
        self.width = 50  # Increased size
        self.height = 25

    def move(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y -= math.sin(math.radians(self.angle)) * self.speed
        self.x = max(0, min(self.x, WINDOW_WIDTH - self.width))
        self.y = max(0, min(self.y, WINDOW_HEIGHT - self.height))

    def draw(self, screen):
        car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.polygon(car_surface, RED, [(0, 0), (self.width, self.height//2), (0, self.height)])  # fun shape
        rotated_car = pygame.transform.rotate(car_surface, self.angle)
        new_rect = rotated_car.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(rotated_car, new_rect.topleft)

class Track:
    def __init__(self):
        self.outer_points = []
        self.inner_points = []
        self.generate_track()

    def generate_track(self):
        center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
        outer_radius = 220
        inner_radius = 150

        for angle in range(0, 360, 5):
            rad = math.radians(angle)
            variation = 20 * math.sin(rad * 3)
            x_outer = center_x + (outer_radius + variation) * math.cos(rad)
            y_outer = center_y + (outer_radius + variation) * math.sin(rad)
            self.outer_points.append((x_outer, y_outer))
            x_inner = center_x + (inner_radius + variation) * math.cos(rad)
            y_inner = center_y + (inner_radius + variation) * math.sin(rad)
            self.inner_points.append((x_inner, y_inner))

    def draw(self, screen):
        pygame.draw.polygon(screen, GREEN, self.outer_points, 2)
        pygame.draw.polygon(screen, GREEN, self.inner_points, 2)


def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("2D Racing Game")
    clock = pygame.time.Clock()

    track = Track()
    car = Car(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            car.speed = min(car.speed + car.acceleration, car.max_speed)
        elif keys[pygame.K_DOWN]:
            car.speed = max(car.speed - car.acceleration, -car.max_speed / 2)
        else:
            car.speed *= 0.96

        if keys[pygame.K_LEFT]:
            car.angle += car.turn_speed * (car.speed / car.max_speed)
        if keys[pygame.K_RIGHT]:
            car.angle -= car.turn_speed * (car.speed / car.max_speed)

        car.move()

        screen.fill(BLACK)
        track.draw(screen)
        car.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
