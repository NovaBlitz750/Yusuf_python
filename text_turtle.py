import turtle

window = turtle.Screen()
t = turtle.Turtle()
t.hideturtle()  # Hide the cursor so we only see text

# Move the turtle to the top of the screen without drawing a line
t.penup()
t.goto(0, 100)

# Write the text instantly
# Arguments: (Text, Alignment on screen, (Font name, Font size, Font style))
t.write("Hello World!", align="center", font=("Arial", 24, "bold"))

window.exitonclick()
