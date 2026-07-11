import tkinter

# Get the name from the console first
name = input("What's your name? ") 

# Create the main window instance using the Tk class
window = tkinter.Tk() 

# Set the window title
window.title("My first GUI") 

# Create the display area FIRST so the hello function can find it
display_area = tkinter.Label(window, text="") 
display_area.pack() # This places text area on window 

# Button click function
def hello():
    print("Hello world!") 
    # Change display area to show its text with the variable concatenated
    display_area.config(text="Hello " + name, fg="yellow", bg="black") 

# Adding a button
b1 = tkinter.Button(window, text="Click me", command=hello) 
b1.pack() # This places the button on the window 

window.mainloop()
