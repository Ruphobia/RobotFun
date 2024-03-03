#!/usr/bin/python3
# Wizard Coder 33B
import turtle

def paddle_a_up():
    """This function moves paddle A up."""
    y = paddle_a.ycor()  # Get the current y-coordinate
    y += 20            # Add 20 to it
    paddle_a.sety(y)     # Set the new y-coordinate

def paddle_a_down():
    """This function moves paddle A down."""
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)

def paddle_b_up():
    """This function moves paddle B up."""
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)

def paddle_b_down():
    """This function moves paddle B down."""
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)

# Create the window and set its properties
wn = turtle.Screen()
wn.title("Pong by @TokyoEdTech")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)  # Stops the window from updating automatically

# Paddle A
paddle_a = turtle.Turtle()
paddle_a.speed(0)   # Set the speed to maximum possible
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)  # Stretches the shape to make it a rectangle
paddle_a.penup()   # Lifts the pen so it doesn't draw when moving
paddle_a.goto(-350, 0)    # Set its initial position

# Paddle B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)

# Keyboard bindings
wn.listen()   # Listen for keyboard input
wn.onkeypress(paddle_a_up, "w")    # When the user presses w, call the paddle_a_up function
wn.onkeypress(paddle_a_down, "s")  # When the user presses s, call the paddle_a_down function
wn.onkeypress(paddle_b_up, "Up")     # When the user presses Up arrow, call the paddle_b_up function
wn.onkeypress(paddle_b_down, "Down")   # When the user presses Down arrow, call the paddle_b_down function

# Main game loop
while True:
    wn.update()  # Update the screen every refresh
