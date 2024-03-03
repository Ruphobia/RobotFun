#!/usr/bin/python3
# phind-coder 34B
import pygame
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 640, 480
PAD_WIDTH, PAD_HEIGHT = 15, 60
BALL_SIZE = 20

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

# Initialize the paddles and ball
paddle1 = pygame.Rect(10, HEIGHT // 2 - PAD_HEIGHT // 2, PAD_WIDTH, PAD_HEIGHT)
paddle2 = pygame.Rect(WIDTH - 20, HEIGHT // 2 - PAD_HEIGHT // 2, PAD_WIDTH, PAD_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Define the velocity of the ball
velocity = [random.choice([-1, 1]), random.choice([-1, 1])]

def draw_objects():
    # Draw the paddles and the ball
    pygame.draw.rect(screen, WHITE, paddle1)
    pygame.draw.rect(screen, WHITE, paddle2)
    pygame.draw.ellipse(screen, WHITE, ball)
    # Update the display
    pygame.display.flip()

def update_paddles():
    keys = pygame.key.get_pressed()
    
    # Move player 1's paddle
    if keys[pygame.K_UP] and paddle1.top > 0:
        paddle1.y -= 5
    if keys[pygame.K_DOWN] and paddle1.bottom < HEIGHT:
        paddle1.y += 5
    
    # Move player 2's paddle
    cpu_paddle()

def cpu_paddle():
    # CPU paddle follows the ball
    if paddle2.top < ball.y:
        paddle2.y -= 5
    if paddle2.bottom > ball.y:
        paddle2.y += 5
    

def update_ball():
    global velocity
    
    # Update the ball's position
    ball.x += velocity[0]
    ball.y += velocity[1]
    
    # Check for collisions with top and bottom walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        velocity[1] = -velocity[1]
    
    # Check for collisions with paddles
    if pygame.Rect.colliderect(ball, paddle1) or pygame.Rect.colliderect(ball, paddle2):
        velocity[0] = -velocity[0]
        
    # Check for out of bounds
    if ball.left <= 0 or ball.right >= WIDTH:
        reset_ball()
    
def reset_ball():
    global velocity
    # Reset the ball's position and reverse its direction
    ball.x = WIDTH // 2 - BALL_SIZE // 2
    ball.y = HEIGHT // 2 - BALL_SIZE // 2
    velocity[0] = -velocity[0]

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        update_paddles()
        update_ball()
        screen.fill(BLACK)  # Draw the background
        draw_objects()  # Draw the paddles and ball
    pygame.quit()

if __name__ == '__main__':
    main()