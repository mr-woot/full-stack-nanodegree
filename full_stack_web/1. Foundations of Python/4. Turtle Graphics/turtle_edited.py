import turtle
import time

def initialize():
    return turtle.Turtle()

def draw_sqparallel():
    tushar = initialize()
    i=1
    while i<=4:        
        tushar.forward(100)
        time.sleep(1)
        tushar.left(90)
        i = i + 1

def draw_circle():
    tushar = initialize()
    tushar.shape()
    tushar.color("red")
    tushar.circle(100)

def play():
    win = turtle.Screen()
    win.bgcolor("green")

    draw_sqparallel()
    draw_circle()

    win.exitonclick()

play()
