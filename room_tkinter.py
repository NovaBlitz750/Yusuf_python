import tkinter as tk

root = tk.Tk()
root.geometry("400x300")

current_room = None
player_name = ""   # store the captured value separately from the widget

def goto_room(build_room):
    global current_room
    if current_room:
        current_room.destroy()
    current_room = build_room()
    current_room.pack(fill="both", expand=True)

def start_game():
    global player_name
    player_name = inpi.get()   # grab the text WHILE inpi still exists
    goto_room(game_room)

def menu_room():
    frame = tk.Frame(root)
    tk.Label(frame, fg="white", text="Enter ur name", bg="navy").pack(pady=20)
    global inpi
    inpi = tk.Entry(frame, fg="blue", bg="yellow")
    inpi.pack(pady=10)

    tk.Button(frame, text="Start", command=start_game).pack()
    return frame

def game_room():
    frame = tk.Frame(root)
    tk.Label(frame, text="Playing...").pack(pady=20)
    tk.Button(frame, text="Back to Menu", command=lambda: goto_room(menu_room)).pack()
    tk.Label(frame, fg="white", text="Hey there " + player_name + "! this is the second room", bg="navy").pack(pady=10)
    return frame

goto_room(menu_room)
root.mainloop()