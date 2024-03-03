#!/usr/bin/python3
# miqu_120b

import random
import time
import sys

import pygame

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 20
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 75
PADDLE_MARGIN = 20
SPEED_FACTOR = 3
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize Pygame and create the game window
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Classic Pong")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Function to draw the ball and paddles on the screen
def draw_objects():
    # Draw the ball
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)

    # Draw Player 1's paddle
    pygame.draw.rect(screen, RED, (paddle1_x, SCREEN_HEIGHT // 2 - PADDLE_MARGIN, PADDLE_WIDTH, PADDLE_MARGIN * 2))

    # Draw Player 2's paddle
    pygame.draw.rect(screen, GREEN, (paddle2_x, SCREEN_HEIGHT // 2 - PADDLE_MARGIN, PADDLE_WIDTH, PADDLE_MARGIN * 2))

    # Draw the score text
    score1_text = font.render(str(score1), True, WHITE)
    score2_text = font.render(str(score2), True, WHITE)
    screen.blit(score1_text, (SCREEN_WIDTH // 4 - len(str(score1)) * 10 // 2, 30))
    screen.blit(score2_text, (SCREEN_WIDTH // 4 + len(str(score2)) * 10 // 2, 30))

# Function to handle the ball's movement and collision detection
def update():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, score1, score2

    # Update the ball's position based on its speed
    ball_x += ball_speed_x * dt
    ball_y += ball_speed_y * dt

    # Check for collisions with the top and bottom walls
    if ball_y < 0 or ball_y > SCREEN_HEIGHT - BALL_RADIUS:
        ball_speed_y *= -1

    # Check for collisions with the paddles
    if (ball_x >= paddle1_x and ball_x <= paddle1_x + PADDLE_WIDTH) and (ball_y >= SCREEN_HEIGHT // 2 - BALL_RADIUS and ball_y <= SCREEN_HEIGHT // 2 + BALL_RADIUS):
        ball_speed_x *= -1
        ball_speed_y += random.uniform(-PADDLE_SPEED, PADDLE_SPEED)
    elif (ball_x >= SCREEN_WIDTH - paddle2_width - BALL_RADIUS and ball_x <= SCREEN_WIDTH - BALL_RADIUS) and (ball_y >= SCREEN_HEIGHT // 2 - BALL_RADIUS and ball_y <= SCREEN_HEIGHT // 2 + BALL_RADIUS):
        ball_speed_x *= -1
        ball_speed_y += random.uniform(-PADDLE_SPEED, PADDLE_SPEED)

    # Check for collisions with the left and right walls
    if ball_x < 0:
        ball_speed_x *= -1
        score2 += 1
        reset_ball()
    elif ball_x > SCREEN_WIDTH:
        ball_speed_x *= -1
        score1 += 1
        reset_ball()

# Function to draw the game objects on the screen
def draw():
    global ball_x, ball_y, paddle1_y, paddle2_y, score1, score2

    # Clear the screen
    screen.fill(BACKGROUND)

    # Draw the ball
    pygame.draw.circle(screen, BALL_COLOR, (ball_x, ball_y), BALL_RADIUS)

    # Draw the paddles
    pygame.draw.rect(screen, PADDLE1_COLOR, (0, paddle1_y, PADDLE1_WIDTH, PADDLE1_HEIGHT))
    pygame.draw.rect(screen, PADDLE2_COLOR, (SCREEN_WIDTH - PADDLE2_WIDTH, paddle2_y, PADDLE2_WIDTH, PADDLE2_HEIGHT))

    # Draw the scores
    font = pygame.font.SysFont("Arial", 36)
    score1_text = font.render(str(score1), True, (0, 0, 0))
    score2_text = font.render(str(score2), True, (0, 0, 0))
    screen.blit(score1_text, (SCREEN_WIDTH // 2 - score1_text.get_width() // 2, 50))
    screen.blit(score2_text, (SCREEN_WIDTH // 2 + score2_text.get_width() // 2, 50))

    # Update the display
    pygame.display.flip()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Move the ball and check for collisions
    move_ball(ball_x, ball_y)
    check_collisions()

    # Update the paddle positions
    update_paddles(paddle1_y, paddle2_y)
