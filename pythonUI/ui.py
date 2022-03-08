from ctypes import sizeof
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as font
import threading
import sys
from xml.etree.ElementPath import get_parent_map

server_name = "localhost"
server_port = 12000
message = ""

# root window
root = tk.Tk()
root.geometry('720x720')
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
        print("[INPUT]:", end=' ')
        sys.stdout.flush()
        message = sys.stdin.readline().rstrip()
        if message == "right":
            if b1['relief'] == SOLID:
                b2['relief'] = SOLID
                b1['relief'] = GROOVE
                b1['fg'] = "black"
                b2['fg'] = "red"
            elif b2['relief'] == SOLID:
                b3['relief'] = SOLID
                b2['relief'] = GROOVE
                b2['fg'] = "black"
                b3['fg'] = "red"
            else:
                print("bad move")

        if message == "left":
            if b2['relief'] == SOLID:
                b1['relief'] = SOLID
                b2['relief'] = GROOVE
                b2['fg'] = "black"
                b1['fg'] = "red"
            elif b3['relief'] == SOLID:
                b2['relief'] = SOLID
                b3['relief'] = GROOVE
                b3['fg'] = "black"
                b2['fg'] = "red"
            else:
                print("bad move")

        if message == "select":
            if b1['relief'] == SOLID:
                threadGameOne = threading.Thread(target=startGameOne, daemon=True)
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

    playerlabel = Label(game1Tab, text="[INPUT]: ")
    playerlabel.place(x=20.0, y=20.0)

    outcomelabel = Label(game1Tab, text="[OUTCOME]")
    outcomelabel.place(x=20.0, y = 40.0)
    game1Tab.update()




    while True:
        if message != "" : 
            x = message.split()
            if x[0] == "turn" :
                playerlabel['text'] = x[1]
            if x[0] == "outcome" :
                outcomelabel['text'] = x[1]
            if x[0] == "outcome" :
                colours = ['','','','','']
                for i in range(len(colours)) :
                    if x[1][i] == 'g' :
                        colours[i] = 'green'
                    if x[1][i] == 'y' :
                        colours[i] = 'yellow'
                    if x[1][i] == 'r' :
                        colours[i] = 'red'

                canvas = tk.Canvas(game1Tab, height=80, width=480)

                canvas.create_rectangle(5,5,80,80, fill=colours[0], outline=colours[0])
                canvas.create_rectangle(100,5,180,80, fill=colours[1], outline=colours[1])
                canvas.create_rectangle(200,5,280,80, fill=colours[2], outline=colours[2])
                canvas.create_rectangle(300,5,380,80, fill=colours[3], outline=colours[3])
                canvas.create_rectangle(400,5,480,80, fill=colours[4], outline=colours[4])

                canvas.pack(side='left')
        game1Tab.update()


# these buttons have been added to 'gameSelection tab'
b1 = Button(gameSelection, text="MasterMind", command=lambda: startGameOne(), height="32", width="32", fg='red', font=buttonFont, relief=SOLID)
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

# types of inputs:

# in the home screen 
# --------------------------
# play mastermind -> this is the only command we will have when at the homescreen



# in the mastermind
# ---------------------------
# turn user1 -> screen shows who's go it is (user1)

# outcome ggrgy -> show below the user's name what their guess was:

# turn user2 -> screen shows that its not user2s go 

# game over winner user 2 -> briefly show that the game has ended (show all 5 green), as well as the winner (for 5 seconds, then go back to homescreen) 

# x = input("new input please")
# x_array = x.split()
# if we're in the home screen
# if x_array[0]= play and x_array[1] = mastermind


# when in the game

# display(x_array[1])
