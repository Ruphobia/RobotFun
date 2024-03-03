#!/usr/bin/python3

"""
Task: Develop a Python3 implementation of the classic Pong game. The game should feature two players: Player 1, controlled by the computer (CPU), and Player 2, controlled by a human player using the up and down arrow keys. The game will track the score of each player, and it concludes when either player reaches 10 points first.

Requirements:

1. Game Mechanics:
   - Implement basic Pong gameplay mechanics, including a moving ball that bounces off walls and paddles.
   - The ball should reset to the center after a player scores a point, with the direction of the next serve alternating between players.

2. Player Controls:
   - Player 2 (human player) must be able to control their paddle using the up and down arrow keys.
   - Player 1 (CPU) should automatically move its paddle based on the ball's position, aiming to block or hit the ball back towards Player 2.

3. Scoring System:
   - Keep track of each player's score, incrementing the score by 1 point whenever the opposing player misses the ball.
   - Display the current score on the screen in a clear and readable format.
   - The game ends when either player reaches 10 points, displaying a message to indicate the winner.

4. Comments and Documentation:
   - Use Doxygen-style comments before each function to describe its purpose, inputs, outputs, and any side effects. Include a brief description of the function, parameters (if any), return values, and any exceptions thrown.
   - Inside functions, use regular comments to explain the logic step-by-step, aiming to make the code understandable to someone without programming experience. Focus on why certain decisions were made and how specific lines of code contribute to the overall functionality.

5. Code Structure:
   - Organize the code into functions or classes as appropriate to maintain readability and modularity. Consider separating game logic, input handling, and rendering to keep the code organized.

Example Doxygen Comment for a Function:
\"\"\"
/**
 * Moves the paddle based on player input.
 *
 * This function updates the paddle's position, ensuring it remains within the game boundaries. It responds to up/down arrow keys for Player 2 and automatically for the CPU player.
 *
 * @param paddle The paddle object to move.
 * @param direction The direction of movement (up or down) for Player 2. For CPU, the direction is calculated based on the ball's position.
 * @return None.
 */
\"\"\"

Additional Notes:
- Ensure the game runs at a consistent speed across different hardware.
- Use Python's built-in libraries or simple external libraries like `pygame` for graphical rendering, event handling, and game loop management.
- Prioritize clear and concise code, with a focus on readability and maintainability.
"""

import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BALL_SPEED = 7
PADDLE_SPEED = 7
BALL_SIZE = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 32
WINNING_SCORE = 10

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pong')

# Load the font
font = pygame.font.Font(None, FONT_SIZE)

def draw_ball(ball):
    """Draws the ball on the screen."""
    pygame.draw.ellipse(screen, WHITE, ball)

def draw_paddle(paddle):
    """Draws the paddle on the screen."""
    pygame.draw.rect(screen, WHITE, paddle)

def move_ball(ball, ball_speed_x, ball_speed_y):
    """Moves the ball and checks for collisions with walls."""
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    return ball

def check_collision(ball, paddle1, paddle2):
    """Checks for collisions between the ball and paddles or walls."""
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        return 'wall'
    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        return 'paddle'
    return 'none'

def restart_ball():
    """Resets the ball to the center of the screen."""
    return pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE), BALL_SPEED if ball_speed_x < 0 else -BALL_SPEED, BALL_SPEED

def display_score(score1, score2):
    """Displays the current score of each player."""
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20))

def move_cpu_paddle(paddle, ball):
    """Automatically moves the CPU paddle based on the ball's position."""
    if paddle.centery < ball.centery:
        paddle.y += min(PADDLE_SPEED, ball.centery - paddle.centery)
    else:
        paddle.y -= min(PADDLE_SPEED, paddle.centery - ball.centery)
    return paddle

def game_loop():
    """Main game loop."""
    ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
    paddle1 = pygame.Rect(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle2 = pygame.Rect(SCREEN_WIDTH - 30 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    ball_speed_x, ball_speed_y = BALL_SPEED, BALL_SPEED
    score1, score2 = 0, 0
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and paddle2.top > 0:
            paddle2.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and paddle2.bottom < SCREEN_HEIGHT:
            paddle2.y += PADDLE_SPEED

        ball = move_ball(ball, ball_speed_x, ball_speed_y)
        collision = check_collision(ball, paddle1, paddle2)
        if collision == 'wall':
            ball_speed_y = -ball_speed_y
        elif collision == 'paddle':
            ball_speed_x = -ball_speed_x

        if ball.left <= 0:
            score2 += 1
            ball, ball_speed_x, ball_speed_y = restart_ball()
        if ball.right >= SCREEN_WIDTH:
            score1 += 1
            ball, ball_speed_x, ball_speed_y = restart_ball()

        paddle1 = move_cpu_paddle(paddle1, ball)

        screen.fill(BLACK)
        draw_ball(ball)
        draw_paddle(paddle1)
        draw_paddle(paddle2)
        display_score(score1, score2)

        pygame.display.flip()
        clock.tick(60)

        if score1 == WINNING_SCORE or score2 == WINNING_SCORE:
            print(f"{'Player 1' if score1 == WINNING_SCORE else 'Player 2'} wins!")
            break

if __name__ == "__main__":
    game_loop()
