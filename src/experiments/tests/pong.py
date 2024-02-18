#!/usr/bin/python3.8
import pygame
import sys
from pygame.locals import *
import random

# Initialization
pygame.init()

# Window dimensions
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Create the window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Paddle dimensions
paddle_width, paddle_height = 20, 100

# Ball dimensions
ball_radius = 5

# FPS
FPS = 60

# Clock
cl = pygame.time.Clock()

# Player score
player_score = 0

class Paddle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.speed = 8

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, paddle_width, paddle_height))

    def move(self, up):
        if up:
            self.y -= self.speed
        else:
            self.y += self.speed

class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = 6 * random.choice((1, -1))
        self.speed_y = 6 * random.choice((1, -1))

    def move(self):
        global player_score
        self.x += self.speed_x
        self.y += self.speed_y

        # Left wall
        if self.x <= ball_radius:
            self.speed_x = 6 * random.choice((1, -1))
            self.x = ball_radius

        # Right wall
        elif self.x >= WIDTH - ball_radius:
            self.speed_x = -6 * random.choice((1, -1))
            self.x = WIDTH - ball_radius

        # Top wall
        if self.y <= ball_radius:
            self.speed_y = 6 * random.choice((1, -1))
            self.y = ball_radius

        # Bottom wall
        elif self.y >= HEIGHT - ball_radius:
            player_score += 1
            return True

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

def main():
    run = True
    paddle1 = Paddle(WIDTH / 2 - paddle_width / 2, HEIGHT - paddle_height - 10, RED)
    paddle2 = Paddle(WIDTH / 2 - paddle_width / 2, 10, GREEN)
    ball = Ball(WIDTH / 2, HEIGHT / 2, ball_radius, WHITE)

    while run:
        cl.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            paddle1.move(True)
        elif keys[pygame.K_DOWN]:
            paddle1.move(False)

        win.fill(BLACK)

        if ball.move():
            ball = Ball(WIDTH / 2, HEIGHT / 2, ball_radius, WHITE)
            paddle1 = Paddle(WIDTH / 2 - paddle_width / 2, HEIGHT - paddle_height - 10, RED)
            paddle2 = Paddle(WIDTH / 2 - paddle_width / 2, 10, GREEN)

        paddle1.draw(win)
        paddle2.draw(win)
        ball.draw(win)

        pygame.draw.line(win, WHITE, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))

        font = pygame.font.Font(None, 50)
        text = font.render(str(player_score), True, WHITE)
        win.blit(text, (WIDTH - text.get_width() - 10, 10))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()