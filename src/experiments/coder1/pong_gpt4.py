#!/usr/bin/python3
# Generate with GPT4
import turtle

# Initialize the window
win = turtle.Screen()
win.title("Pong")
win.bgcolor("black")
win.setup(width=800, height=600)
win.tracer(0)  # Stops the window from updating automatically

# Paddle A (CPU)
paddle_a = turtle.Turtle()
paddle_a.speed(0)  # Animation speed
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=6, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)

# Paddle B (Player)
paddle_b = turtle.Turtle()
paddle_b.speed(0)  # Animation speed
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=6, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Ball
# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.8  # Increase the x movement speed to make the ball go faster
ball.dy = -0.8  # Increase the y movement speed to make the ball go faster


# Function to move paddle A up
def paddle_a_up():
    """Move paddle A up"""
    y = paddle_a.ycor()
    if y < 250:
        y += 20
    paddle_a.sety(y)

# Function to move paddle A down
def paddle_a_down():
    """Move paddle A down"""
    y = paddle_a.ycor()
    if y > -240:
        y -= 20
    paddle_a.sety(y)

# Function to move paddle B up
def paddle_b_up():
    """Move paddle B up"""
    y = paddle_b.ycor()
    if y < 250:
        y += 20
    paddle_b.sety(y)

# Function to move paddle B down
def paddle_b_down():
    """Move paddle B down"""
    y = paddle_b.ycor()
    if y > -240:
        y -= 20
    paddle_b.sety(y)

# Keyboard bindings
win.listen()
win.onkeypress(paddle_b_up, "Up")
win.onkeypress(paddle_b_down, "Down")

def main():
    """Main game loop"""
    update_speed = 0
    while True:

        # make the ball go faster over time
        update_speed += 1
        if (update_speed > 10):
            update_speed = 0
            ball.dx += 0.01
            ball.dy -= 0.01

        win.update()  # Update the screen
        
        # Move the ball
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)
        
        # Border checking for ball
        if ball.ycor() > 290 or ball.ycor() < -290:
            ball.dy *= -1
        
        if ball.xcor() > 390:  # Player B misses
            ball.goto(0, 0)
            ball.dx *= -1
        
        if ball.xcor() < -390:  # Player A misses
            ball.goto(0, 0)
            ball.dx *= -1
        
        # Paddle and ball collisions
        if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < paddle_b.ycor() + 50 and ball.ycor() > paddle_b.ycor() - 50):
            ball.setx(340)
            ball.dx *= -1
        
        if (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < paddle_a.ycor() + 50 and ball.ycor() > paddle_a.ycor() - 50):
            ball.setx(-340)
            ball.dx *= -1

        # Simple CPU for Player A
        if paddle_a.ycor() < ball.ycor() and abs(paddle_a.ycor() - ball.ycor()) > 10:
            paddle_a_up()
        elif paddle_a.ycor() > ball.ycor() and abs(paddle_a.ycor() - ball.ycor()) > 10:
            paddle_a_down()

if __name__ == "__main__":
    main()
