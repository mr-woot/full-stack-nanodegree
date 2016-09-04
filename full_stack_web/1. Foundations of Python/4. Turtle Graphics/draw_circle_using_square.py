import turtle
import time

def initialize():
    return turtle.Turtle()

def screen():
    return turtle.Screen()

def draw_sq(turtle_object):
    for i in range(1, 5):
        turtle_object.forward(100)
        turtle_object.right(90)

def draw():
    win = screen()
    win.bgcolor("black")

    tushar = initialize()
    tushar.color("yellow")
    tushar.speed(30)

    for i in range(1, 37):
        draw_sq(tushar)
        tushar.right(10)
    win.exitonclick()

draw()
