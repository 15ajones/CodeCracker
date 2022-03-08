import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as font
import threading


server_name = "localhost"
server_port = 12000
message = ""

# root window
root = tk.Tk()
root.geometry('720x480')
root.title('InfoProc')
style = ttk.Style()
style.layout('TNotebook.Tab', [])

# create a tab
tab = ttk.Notebook(root)
tab.pack(pady=10, expand=True)

# create frames
gameSelection = ttk.Frame(tab, width=720, height=480)
gameSelection.pack(fill='both', expand=True)
game1Tab = ttk.Frame(tab, width=720, height=480)
game1Tab.pack(fill='both', expand=True)

# add frames to tabs
tab.add(gameSelection, text='Game Selection')
tab.add(game1Tab, text='Game 1')
# create game buttons
buttonFont = font.Font(family='Arial', weight="bold", size=8)

def inputListen():
    global message
    while True:
        message = input("[INPUT]: ")

        if message == "right":
            if b1['relief'] == SOLID:
                b2['relief'] = SOLID
                b1['relief'] = GROOVE
            elif b2['relief'] == SOLID:
                b3['relief'] = SOLID
                b2['relief'] = GROOVE
            else:
                print("bad move")

        if message == "left":
            if b2['relief'] == SOLID:
                b1['relief'] = SOLID
                b2['relief'] = GROOVE
            elif b3['relief'] == SOLID:
                b2['relief'] = SOLID
                b3['relief'] = GROOVE
            else:
                print("bad move")

        if message == "select":
            if b1['relief'] == SOLID:
                threadGameOne = threading.Thread(target=startGameOne)
                threadGameOne.start()
            elif b2['relief'] == SOLID:
                print("start game 2")
            else:
                print("start game 3")

        if message == "menu":
            tab.select(gameSelection)






def startGameOne():
    tab.select(game1Tab)
    global message

    DataLabel = Label(game1Tab, text="[INPUT]: ")
    DataLabel.place(x=20.0, y=20.0)
    game1Tab.update()

    while True:
        DataLabel['text'] = "[INPUT]: " + message
        game1Tab.update()


# these buttons have been added to 'gameSelection tab'
b1 = Button(gameSelection, text="MasterMind", command=lambda: startGameOne(), height="32", width="32", fg='black', font=buttonFont, relief=SOLID)
b1.pack(padx=5, pady=15, side=tk.LEFT)
b2 = Button(gameSelection, text="Game 2", height="32", width="32", fg='black', font=buttonFont, relief=GROOVE)
b2.pack(padx=5, pady=15, side=tk.LEFT)
b3 = Button(gameSelection, text="Game 3", height="32", width="32", fg='black', font=buttonFont, relief=GROOVE)
b3.pack(padx=5, pady=15, side=tk.LEFT)

Button(game1Tab, text="Return to Menu", font=buttonFont, command=lambda: tab.select(gameSelection)).place(x=600.0, y=400.0)
# use ipAddressEntry.get() & portEntry.get() to get TCP things

listener = threading.Thread(target=inputListen)
listener.start()
root.mainloop()
