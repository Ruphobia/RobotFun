#!/usr/bin/python3
# Deepseek 67b, chat

# import required libraries
import pygame
import random

def init_game():
    """Initialize the game"""
    # initialize pygame
    pygame.init()
    
    # set display window size
    screen = pygame.display.set_mode((800, 600))
    
    # set caption of the display window
    pygame.display.set_caption("Pong Game")
    
    return screen

def draw_ball(screen, ball):
    """Draw ball on the screen"""
    # draw a circle for the ball
    pygame.draw.circle(screen, (255, 255, 255), ball.center, ball.radius)
    
def draw_player1(screen, player1):
    """Draw player1 on the screen"""
    # draw a rectangle for player1's paddle
    pygame.draw.rect(screen, (0, 255, 0), player1.rect)

def draw_player2(screen, player2):
    """Draw player2 on the screen"""
    # draw a rectangle for player2's paddle
    pygame.draw.rect(screen, (255, 0, 0), player2.rect)
    
def update_ball(ball, ball_speed, player1, player2):
    """Update the position of the ball"""
    # move the ball in x and y direction based on its speed
    ball.centerx += ball_speed[0]
    ball.centery += ball_speed[1]
    
    # if ball hits top or bottom wall, reverse y direction
    if ball.centery < 30 or ball.centery > 570:
        ball_speed[1] = -ball_speed[1]
        
    # if ball hits player1's paddle, reverse x direction and adjust y speed based on collision position
    if pygame.Rect.colliderect(player1.rect, ball):
        ball_speed[0] = -ball_speed[0]
        if abs(ball.centerx - player1.rect.left) < 5:
            ball_speed[1] += random.randint(-2, 2)
        else:
            ball_speed[1] -= random.randint(-2, 2)
    
    # if ball hits player2's paddle, reverse x direction and adjust y speed based on collision position
    if pygame.Rect.colliderect(player2.rect, ball):
        ball_speed[0] = -ball_speed[0]
        if abs(ball.centerx - player2.rect.left) < 5:
            ball_speed[1] += random.randint(-2, 2)
        else:
            ball_speed[1] -= random.randint(-2, 2)
        
    # if ball goes out of right side, player1 scores
    if ball.centerx > 800:
        return -1
    
    # if ball goes out of left side, player2 scores
    if ball.centerx < 0:
        return 1
        
def main():
    """Main function to run the game"""
    screen = init_game()
    
    # set up initial conditions for the ball and players
    ball = pygame.Rect(400, 300, 20, 20)
    player1 = pygame.Rect(765, 285, 20, 100)
    player2 = pygame.Rect(5, 285, 20, 100)
    ball_speed = [4, 4] # x and y speed of the ball
    
    score = [0, 0] # keep track of scores for player1 and player2
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        keys_pressed = pygame.key.get_pressed() # get the current state of keyboard buttons
        
        # move player2 up and down based on arrow key presses
        if keys_pressed[pygame.K_UP]:
            player2.move_ip(0, -5)
        elif keys_pressed[pygame.K_DOWN]:
            player2.move_ip(0, 5)
            
        # keep player2 within screen bounds
        if player2.top < 30:
            player2.top = 30
        if player2.bottom > 570:
            player2.bottom = 570
        
        draw_ball(screen, ball) # draw the ball on the screen
        draw_player1(screen, player1) # draw player1's paddle on the screen
        draw_player2(screen, player2) # draw player2's paddle on the screen
        
        update_ball(ball, ball_speed, player1, player2) # update the position of the ball
        
        if update_ball == -1: # if player1 scores
            score[0] += 1
            print("Player1 scores!")
            ball.center = (400, 300)
            
        elif update_ball == 1: # if player2 scores
            score[1] += 1
            print("Player2 scores!")
            ball.center = (400, 300)
        
        pygame.display.flip() # flip the display to show changes on screen


main()