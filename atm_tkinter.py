import tkinter as tk

root = tk.Tk()
root.geometry("400x500")
root.title("ATM PIN Project")

details = tk.Frame(root, bd=2, relief="raised")
details.pack(side="top", fill="x", padx=10, pady=10)

tk.Label(details, text="Name:").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(details)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(details, text="Account Number:").grid(row=1, column=0, padx=5, pady=5)
acc_entry = tk.Entry(details)
acc_entry.grid(row=1, column=1, padx=5, pady=5)

pin_frame = tk.Frame(root)
pin_frame.pack(pady=10)

tk.Label(pin_frame, text="Enter PIN:").pack()
pin_entry = tk.Entry(pin_frame, show="*", width=20)
pin_entry.pack()

keypad = tk.Frame(root, bd=2, relief="sunken")
keypad.pack(side="top", fill="both", expand=True, padx=10, pady=10)

rows = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    ["0", "Clear", "Enter"]
]

def submit():
    summary.delete("1.0", tk.END)
    summary.insert("1.0",
                   f"Name: {name_entry.get()}\n"
                   f"Account Number: {acc_entry.get()}\n"
                   f"PIN Entered: {pin_entry.get()}\n")

def add_digit(d):
    if d == "Clear":
        pin_entry.delete(0, tk.END)
    elif d == "Enter":
        submit()
    else:
        current = pin_entry.get()
        pin_entry.delete(0, tk.END)
        pin_entry.insert(0, current + d)

for r, row in enumerate(rows):
    for c, label in enumerate(row):
        btn = tk.Button(keypad, text=label, width=7, height=2,
                        command=lambda d=label: add_digit(d))
        btn.grid(row=r, column=c, padx=5, pady=5)

summary = tk.Text(root, height=6, width=40)
summary.pack(pady=10)

root.mainloop()
