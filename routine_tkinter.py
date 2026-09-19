import tkinter as tk
import tkinter as tk
from tkinter import messagebox
root=tk.Tk()
root.title("After School Routine Checker")
tasks = ["Snack", "Homework", "Chores", "Free time"]
def clicked():
    text=routine.get()
    if routine.get()=='' or routine.get() not in tasks:
        messagebox.showwarning("Alert", "Wrong task detected")
    else:
        print(text)
routine=tk.Entry(root, bg="lightblue")
routine.pack()
btn=tk.Button(root,text="Enter task and click to verify it",command=clicked)
btn.pack()
root.mainloop()