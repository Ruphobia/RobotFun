#!/usr/bin/python3
import os
import time
import random

# Function to print the menu
def print_menu():
    print("""
    Up Arrow: Player 2 moves up
    Down Arrow: Player 2 moves down
    """)

# Function for CPU to play against user
def cpu_play(player1, player2):
    # CPU goes first
    while True:
        if player1.score > player2.score:
            print("CPU wins!")
            return
        elif player2.score > player1.score:
            print("Player 2 wins!")
            return

        # CPU's move
        cpu_move = random.choice([True, False])
        if cpu_move:
            player1.move(0, 1)
            time.sleep(1)

        # Player 2's move
        player2_move = input("Player 2, do you want to move up or down? (Up/Down Arrow): ")
        if player2_move.lower() == 'up':
            player2.move(0, -1)
        elif player2_move.lower() == 'down':
            player2.move(0, 1)
            
        # Printing the current state of the game
        print("CPU: ", player1.position)
        print("Player 2: ", player2.position)

# Function to play the game
def play_game():
    global player1, player2
    
    # Initializing positions for both players
    player1.position = [0, 0]
    player2.position = [0, 0]
    
    # Playing the game
    while True:
        print_menu()
        cpu_play(player1, player2)
        
# Main Function
def main():
    global player1, player2
    player1 = Paddle(1, 1)
    player2 = Paddle(0, 0)
    
    play_game()

# Defining the Paddle class
class Paddle:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        
    # Method to move the paddle up or down
    def move(self, dx, dy):
        self.x_pos += dx
        self.y_pos += dy

if __name__ == "__main__":
    main()
