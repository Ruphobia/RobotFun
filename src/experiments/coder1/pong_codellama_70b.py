#!/usr/bin/python3
# generated using codellama 70b

from turtle import *
from freegames import vector
import random


player1xy = vector(-100, 0)
player2xy = vector(100, 0)
playersize = 50
ballxy = vector(0, 0)
ballspeed = vector(random.randint(-9, -6), random.randint(5, 7))

def pongstart():
    "Starts the game of Pong"
    global ballx, bally
    ballxy = vector(0, 0)
    ballspeed = vector(10, random.randrange(-6, 6))
    ht()
    up()

def pongmove():
    "Moves the ball and players"
    global ballx, bally
    window.clear()
    player1xy.y += (random.randint(10, 20) * random.choice([-1, 1])) #Causes CPU Player to jump around randomly
    
    if inside(ballxy):
        ballx += ballspeed.x
        bally += ballspeed.y
    elif (ballxy.y < -200) or (ballxy.y > 200):
        ballspeed.y *= -1
    
    if (ballxy-player1xy).mag() < playersize:
        ballspeed.x = abs(ballspeed.x)
        
    elif (ballxy-player2xy).mag() < playersize:
            ballspeed.x = -abs(ballspeed.x)
    
    ballxy.move(ballspeed)
    player1xy.draw()
    player2xy.draw()
    window.update()

def pongcheck():
    "Checks to see if the game ends"
    if not inside(ballxy):
        return True
    else:
        return False

def pongscore(p1, p2):
    "Determines which player won and ends the game"
    global window
    window.clear()
    
    if (ballxy-player1xy).mag() < playersize:
        window.bgcolor('red')
        
    elif (ballxy-player2xy).mag() < playersize:
            window.bgcolor('blue')
            
    up()
    goto(0, 50)
    color('white')
    
    if p1 > p2:
        write("Player 1 Wins", font=("Arial", 36))
        
    elif p2 > p1:
            write("Player 2 Wins", font=("Arial", 36))
            
    else:
            write("It's a tie!", font=("Arial", 36))
    
    down()
    goto(0, -50)
    
    if p1 != 7 and p2 != 7:
        color('white')
        write("Press Enter to play again or press Esc to quit.", font=("Arial", 18))
            
    update()
        
def main():
    "Main function that runs game"
    
    global window
    window = Screen()
    window.tracer(False)
    pongstart()
    player2xy.draw()
    player1xy.draw()
    ballxy.draw()
    
    #Game Loop
    while True:
        pongmove()
        
        if pongcheck():
            pongscore()
            
main()