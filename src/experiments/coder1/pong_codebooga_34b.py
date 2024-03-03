#!/usr/bin/python3
import turtle
import random
import time

# Setup the screen
screen = turtle.Screen()
screen.title("Pong")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

# Score
score_1 = 0
score_2 = 0

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B
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
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 2
ball.dy = -2

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Player A: 0 Player B: 0", align="center", font=("Courier", 24, "normal"))

# Function to move the paddle up
def paddle_a_up():
    """Function to move Paddle A up"""
    y = paddle_a.ycor()
    y += 20
    paddle_a.sety(y)

# Function to move the paddle down
def paddle_a_down():
    """Function to move Paddle A down"""
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)

# Function to move the ball
def move_ball():
    """Function to move the ball"""
    global score_1, score_2
    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border checking
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_1 += 1
        pen.clear()
        pen.write("Player A: {} Player B: {}".format(score_1, score_2), align="center", font=("Courier", 24, "normal"))

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_2 += 1
        pen.clear()
        pen.write("Player A: {} Player B: {}".format(score_1, score_2), align="center", font=("Courier", 24, "normal"))

    # Paddle and ball collisions
    if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < paddle_b.ycor() + 50 and ball.ycor() > paddle_b.ycor() - 50):
        ball.setx(340)
        ball.dx *= -1
    if (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < paddle_a.ycor() + 50 and ball.ycor() > paddle_a.ycor() - 50):
        ball.setx(-340)
        ball.dx *= -1

# Keyboard bindings
screen.listen()
screen.onkeypress(paddle_a_up, "Up")
screen.onkeypress(paddle_a_down, "Down")

# Main game loop
while True:
    screen.update()
    move_ball()

    # CPU control for Paddle A
    if paddle_a.ycor() < ball.ycor() - 30 and ball.xcor() > -400:
        paddle_a_down()
    elif paddle_a.ycor() > ball.ycor() + 30 and ball.xcor() > -400:
        paddle_a_up()
