from tkinter import *
from tkinter import Toplevel

root = Tk()
root.title("Main")
root.geometry("300x300")

def open_window():

    top = Toplevel()
    top.geometry("500x500")
    top.title("Reading Schedule Calculator")

    lbl1 = Label(top, text="Enter total pages in book")
    lbl1.grid(row=0, column=0, padx=10, pady=10)

    ent1 = Entry(top,bg="lightblue")
    ent1.grid(row=0, column=1)

    lbl2 = Label(top, text="Enter pages u read per day")
    lbl2.grid(row=1, column=0, padx=10, pady=10)

    ent2 = Entry(top,bg="lightblue")
    ent2.grid(row=1, column=1)

    days_text = Label(top, text="Days needed to complete book:",bg="navyblue",fg="white")
    days_text.grid(row=3, column=0)

    days_value = Label(top, text="")
    days_value.grid(row=3, column=1)

    remain_text = Label(top, text="Pages remaining:",bg="navyblue",fg="white")
    remain_text.grid(row=4, column=0)

    remain_value = Label(top, text="")
    remain_value.grid(row=4, column=1)

    def calculate():
        try:
            tp = int(ent1.get())
            pdp = int(ent2.get())

            days = tp // pdp
            remain = tp % pdp

            days_value.config(text=days)
            remain_value.config(text=remain)

        except:
            days_value.config(text="Invalid")
            remain_value.config(text="Input")

    cal = Button(top, text="Calculate", command=calculate)
    cal.grid(row=2, column=0, columnspan=2, pady=10)

Btn1 = Button(root, text="Open Calculator", command=open_window)
Btn1.pack()

root.mainloop()