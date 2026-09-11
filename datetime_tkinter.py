from tkinter import *
from datetime import date

#Create Window
root=Tk()
root.title("Getting Started with widgets")
root.geometry("400x300")
lbl=Label(text="Hey There!", fg="white", bg="#072F5F", height=1, width=300)
name_lbl=Label(text="Full Name", bg="#389503")
name_entry=Entry()
def display():
    text_box.delete("1.0",END)
    name=name_entry.get()
    global message
    message = "Welcome to the Application! \nToday's date is "
    greet="Hello "+name+"\n"
    text_box.insert(END, greet)
    text_box.insert(END,message)
    text_box.insert(END,date.today())
    name_entry.delete(0,END)
text_box=Text(height=3)
btn=Button(text="Begin", command=display, height=1,bg="#1261a0", fg="white")
lbl.pack()
name_lbl.pack()
name_entry.pack()
btn.pack()
text_box.pack()
root.mainloop()