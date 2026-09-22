import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
root=tk.Tk()
root.title("Text Editor")
root.geometry('600x500')
root.rowconfigure(0, minsize=800, weight=1)
root.columnconfigure(1, minsize=800, weight=1)
def save_file():
    filepath=asksaveasfilename(
        filetypes=[("Text Files","*.txt"),("All Files","*.*")]
    )
    if not filepath:
        return
    
    with open(filepath,"w") as output_file:
        text=txt_edit.get(1.0,tk.END)
        output_file.write(text)
    root.title(f"My Text Editor-{filepath}")
def open_file():
	print("hello")
    filepath=askopenfilename(
        filetypes=[("Text Files","*.txt"),("All Files","*.*")]
    )
    if not filepath:
        return
    txt_edit.delete(1.0,tk.END)
    with open(filepath,"r") as input_file:
        text=input_file.read()
        txt_edit.insert(tk.END,text)
        input_file.close()
    root.title(f"My Text Editor-{filepath}")
txt_edit=tk.Text(root)
fr_buttons=tk.Frame(root,relief=tk.RAISED,bd=2)
btn_open=tk.Button(fr_buttons,text="Open",command=open_file)
btn_save=tk.Button(fr_buttons,text="Save As...", command=save_file)


btn_open.grid(row=0, column=0,sticky="ew",padx=5,pady=5)
btn_save.grid(row=1,column=0,sticky="ew",padx=5)


fr_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0,column=1,sticky="nsew")

root.mainloop()
