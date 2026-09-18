import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.geometry("200x200")
scanning = tk.Label(root, text="Scanning for viruses...")

def scan():
    scanning.pack()
    root.after(3000, finish_scan)  # runs after 3000ms, without freezing the GUI

def finish_scan():
    scanning.pack_forget()
    messagebox.showwarning("Alert", "Scan complete")

button = tk.Button(root, text="Scan for Viruses", command=scan)
button.place(x=40, y=80)

root.mainloop()