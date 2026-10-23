import turtle
hi=input("Hello")
if hi.strip().upper()=="GOOD":
    window = turtle.Screen()
    window.bgcolor("white")

# 2. Create our turtle artist and customize it
    my_turtle = turtle.Turtle()
    my_turtle.shape("classic")  # Changes the cursor icon to an actual turtle
    my_turtle.color("black")    # Changes the line and turtle color
    my_turtle.speed(2)         # Set movement speed (1 = slow, 10 = fast)

# 3. Move the turtle to draw a line
    my_turtle.forward(100)  
    my_turtle.right(90)   # Move forward by 100 pixels