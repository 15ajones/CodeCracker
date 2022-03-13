from ctypes import sizeof
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as font
import threading
import sys
from xml.etree.ElementPath import get_parent_map
import socket

# server stuff
host_name = '35.176.178.191'
host_port = 12000

ui_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ui_socket.bind(('', 11000))

ping = "hello server"
ui_socket.sendto(ping.encode(), (host_name, host_port))

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
textFont = font.Font(family='Arial', weight="bold", size=16)

def inputListen():
    global message
    while True:
        #print("[INPUT]:", end=' ')
        #sys.stdout.flush()
        print("waiting for message")
        message = ui_socket.recv(1024)
        print("message received")
        message = message.decode()
        print(message)
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
        if message == "exit" :
            exit()


def startGameOne():
    tab.select(game1Tab)
    global message

    playerlabel = Label(game1Tab, text="READY", fg='black', font=textFont)
    playerlabel.place(x=320.0, y=20.0, anchor="center")

    canvas = tk.Canvas(game1Tab, height=80, width=480)
    colours = ['white','white','white','white','white']

    while True:
        if message != "" : 
            x = message.split()

            if x[0] == "menu" :
                canvas.delete('all')
                playerlabel['text'] = ""

            elif x[0] == "turn" :
                playerlabel['text'] = ""
                playerlabel['text'] = x[1]
            #if x[0] == "outcome" :
                #outcomelabel['text'] = x[1]
            elif x[0] == "outcome" :
                #colours = ['','','','','']
                for i in range(len(colours)) :
                    if x[1][i] == 'g' :
                        colours[i] = 'green'
                    elif x[1][i] == 'y' :
                        colours[i] = 'yellow'
                    elif x[1][i] == 'r' :
                        colours[i] = 'red'
                canvas.create_rectangle(5,5,80,80, fill=colours[0], outline=colours[0])
                canvas.create_rectangle(100,5,180,80, fill=colours[1], outline=colours[1])
                canvas.create_rectangle(200,5,280,80, fill=colours[2], outline=colours[2])
                canvas.create_rectangle(300,5,380,80, fill=colours[3], outline=colours[3])
                canvas.create_rectangle(400,5,480,80, fill=colours[4], outline=colours[4])
                message = ""    # need to clear message else it loops infinitely back to outcome

                canvas.pack(side='bottom')
                #print(canvas.find_all())    # prints all canvas items active
            elif x[0] == "game" :
                playerlabel['text'] = "The winner is: " + x[3]
        game1Tab.update()


# these buttons have been added to 'gameSelection tab'
b1 = Button(gameSelection, text="MasterMind", command=lambda: startGameOne(), height="32", width="32", fg='red', font=buttonFont, relief=SOLID)
b1.pack(padx=5, pady=15, side=tk.LEFT)
b2 = Button(gameSelection, text="Game 2", height="32", width="32", fg='black', font=buttonFont, relief=GROOVE)
b2.pack(padx=5, pady=15, side=tk.LEFT)
b3 = Button(gameSelection, text="Game 3", height="32", width="32", fg='black', font=buttonFont, relief=GROOVE)
b3.pack(padx=5, pady=15, side=tk.LEFT)

Button(game1Tab, text="Return to Menu", font=buttonFont, command=lambda: tab.select(gameSelection)).place(x=600.0, y=450.0)
# use ipAddressEntry.get() & portEntry.get() to get TCP things

listener = threading.Thread(target=inputListen)
listener.start()
root.mainloop()

# types of inputs:

# in the home screen 
# --------------------------
# left -> select box to the left of current selection
# right -> select box to the right of current selection
# select -> start currently selected game



# in the mastermind
# ---------------------------
# turn user1 -> screen shows who's go it is (user1)

# outcome ggrgy -> displays the colour mapping for the users guess

# turn user2 -> screen shows that its now user2s go 

# game over winner user2 -> display that the winner is user2

# menu -> back to game selection menu



