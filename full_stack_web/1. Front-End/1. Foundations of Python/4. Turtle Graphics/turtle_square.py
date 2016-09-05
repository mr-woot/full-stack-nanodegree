import turtle
import time

def draw():
    win = turtle.Screen()
    win.bgcolor("green")

    tushar = turtle.Turtle()
    tushar.forward(150)
    #time.sleep(1)
    tushar.left(100)
    tushar.forward(100)
    #time.sleep(1)
    tushar.left(80)
    tushar.forward(150)
    #time.sleep(1)
    tushar.left(100)
    tushar.forward(100)
    win.exitonclick()

draw()
