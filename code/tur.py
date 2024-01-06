import turtle

screen = turtle.Screen()
t = turtle.Turtle()

t.color('red','red')
t.begin_fill()
def curve():
    for i in range(200):
        t.right(1)
        t.forward(1)


def heart():
    t.left(140)
    t.forward(123)
  
    curve()
    t.left(120)
  
    curve()
    t.forward(122)

heart()

t.end_fill()
t.hideturtle()

turtle.done()