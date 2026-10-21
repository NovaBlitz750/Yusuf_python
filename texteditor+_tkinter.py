import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

APP_NAME = "Letter Writer"

root = tk.Tk()
root.title(APP_NAME)
root.geometry("700x500")
root.rowconfigure(0, minsize=400, weight=1)
root.columnconfigure(1, minsize=500, weight=1)


def new_letter():
    """Clear the editor and start a fresh letter with a simple skeleton."""
    txt_edit.delete(1.0, tk.END)
    txt_edit.insert(tk.END, "Dear ,\n\n\n\nYours sincerely,\n")
    root.title(f"{APP_NAME} - New letter")


def open_file():
    """Open an old letter and show it in the editor so it can be edited."""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete(1.0, tk.END)
    with open(filepath, "r", encoding="utf-8") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    root.title(f"{APP_NAME} - {filepath}")


def save_file():
    """Save the letter under a name the user picks (new or existing)."""
    filepath = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, "w", encoding="utf-8") as output_file:
        text = txt_edit.get(1.0, tk.END)
        output_file.write(text)
    root.title(f"{APP_NAME} - {filepath}")


# Widgets
txt_edit = tk.Text(root, wrap=tk.WORD, font=("Georgia", 12))
fr_buttons = tk.Frame(root, relief=tk.RAISED, bd=2)
btn_new = tk.Button(fr_buttons, text="New Letter", command=new_letter)
btn_open = tk.Button(fr_buttons, text="Open Letter", command=open_file)
btn_save = tk.Button(fr_buttons, text="Save As...", command=save_file)

# Layout
btn_new.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_open.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

new_letter()  # start with a fresh letter instead of an empty box

root.mainloop()