import turtle
sides=int(input("Enter the number of sides in your shape"))
angle=360/sides
turtle.Screen().bgcolor("white")
screen=turtle.Screen()
screen.setup(width=700,height=700)
t=turtle.Turtle()
t.shape("turtle")
t.penup()
t.goto(-100,50)
t.pendown()
for i in range(sides):
    t.forward(100)
    t.right(angle)
turtle.exitonclick()