import tkinter as tk
root=tk.Tk()
root.title("Workshop Participation Project")
root.geometry('400x400')
lbl1=tk.Label(root, bg="navy", fg="white",text="Enter your name for the workshop")
lbl1.pack(fill='x')

#Adding user input
name_entry=tk.Entry(root, bg="lightyellow", fg="blue")
name_entry.pack()
output_text = tk.Text(root, height=5, width=40)
output_text.pack()

def check():
    name=name_entry.get()
    msg="Welcome, "+ name +"!\nWorkshop Date: 20 Sept,2026"
    output_text.delete("1.0", "end")
    output_text.insert("1.0", msg)
    output_text.config(state='disabled')
    name_entry.delete(0, "end")
checkin_btn = tk.Button(root, text="Check In", bg="steelblue", fg="white", command=check)
checkin_btn.pack()
root.mainloop()