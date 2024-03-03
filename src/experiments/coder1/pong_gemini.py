#!/usr/bin/python3
# generated with gemini
import turtle
import time
import random

# Window setup
wn = turtle.Screen()
wn.title("Pong by Your Name")  # Replace 'Your Name' with your name
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Score
score_a = 0
score_b = 0

# Paddle A (CPU)
paddle_a = turtle.Turtle()
paddle_a.speed(0)  # Maximum animation speed
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B (Player)
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.2  # Ball's movement speed in the x direction
ball.dy = 0.2

# Pen for score
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

# --- Functions ---

##  /**
##  * Moves paddle A (CPU) based on ball position
##  */
def move_paddle_a():
    y = ball.ycor()
    y += random.randint(-20, 20)  # Add randomness to CPU movement
    if y > 250:
        y = 250
    if y < -250:
        y = -250
    paddle_a.sety(y)


##  /**
##  * Moves paddle B upwards
##  */
def move_paddle_b_up():
    y = paddle_b.ycor()
    y += 30
    if y > 250:
        y = 250
    paddle_b.sety(y)


##  /**
##  * Moves paddle B downwards
##  */
def move_paddle_b_down():
    y = paddle_b.ycor()
    y -= 30
    if y < -250:
        y = -250
    paddle_b.sety(y)


# --- Keyboard bindings ---
wn.listen()
wn.onkeypress(move_paddle_b_up, "Up")
wn.onkeypress(move_paddle_b_down, "Down")

# --- Main game loop ---
def main():
    while True:
        wn.update()  # Update the game screen

        # Move the ball
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Border collision checking
        # Top and bottom
        if ball.ycor() > 290 or ball.ycor() < -290:
            ball.dy *= -1

        # Right and left
        if ball.xcor() > 390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_a += 1
            pen.clear() 
            pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))

        if ball.xcor() < -390:
            ball.goto(0, 0)
            ball.dx *= -1
            score_b += 1
            pen.clear()
            pen.write("Player A: {}  Player B: {}".format(score_a, score_b), align="center", font=("Courier", 24, "normal"))

        # Paddle and ball collisions
        # ... (implementation in next step) 
        
        move_paddle_a()  # CPU paddle movement

# ... (add paddle collision logic in the next step)
main()  # Start the game
