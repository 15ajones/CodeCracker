from ctypes import sizeof
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as font
import threading
import sys
from xml.etree.ElementPath import get_parent_map
import socket

from grpc import xds_channel_credentials

# server stuff
host_name = 'localhost'
host_port = 12000

ui_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ui_socket.bind(('', 11000))

ping = "hello server"
ui_socket.sendto(ping.encode(), (host_name, host_port))

message = ""
p1_name = "None"
p2_name = "None"
p3_name = "None"
p1_score = 0
p2_score = 0
p3_score = 0

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
game2Tab = ttk.Frame(tab, width=720, height=480)
game2Tab.pack(fill='both', expand=True)
leaderboardTab = ttk.Frame(tab, width=720, height=480)
leaderboardTab.pack(fill='both', expand=True)

# add frames to tabs
tab.add(gameSelection, text='Game Selection')
tab.add(game1Tab, text='Game 1')
tab.add(game2Tab, text='Game 2')
tab.add(leaderboardTab, text='Leaderboard')

# create game buttons
buttonFont = font.Font(family='Arial', weight="bold", size=8)
textFont = font.Font(family='Arial', weight="bold", size=16)

def inputListen():
    global message, p1_score, p2_score, p3_score, p1_name, p2_name, p3_name
    while True:
        print("[INPUT]:", end=' ')
        sys.stdout.flush()
        # print("waiting for message")
        # message = ui_socket.recv(1024)
        # print("message received")
        # message = message.decode()
        message = sys.stdin.readline().rstrip()          #Testing without server, comment 4 line above
        print(message)
        if message != "":
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
                    threadGameTwo = threading.Thread(target=startGameTwo, daemon=True)
                    threadGameTwo.start()
                else:
                    tab.select(leaderboardTab)

            if message.split()[0] == "leaderboard":
                print("Updating Scores")
                msg = message.split()
                if msg[1] == p1_name or p1_name == "None":
                    p1_name = msg[1]
                    p1_score = msg[2]
                    p1Label['text'] = p1_name + "\t\t" + str(p1_score)
                elif msg[1] == p2_name or p2_name == "None":
                    p2_name = msg[1]
                    p2_score = msg[2]
                    p2Label['text'] = p2_name + "\t\t" + str(p2_score)
                elif msg[1] == p3_name or p3_name == "None":
                    p3_name = msg[1]
                    p3_score = msg[2]
                    p3Label['text'] = p3_name + "\t\t" + str(p3_score)

            if message == "scores":
                print(p1_score, p2_score, p3_score)
            if message == "menu":
                tab.select(gameSelection)
                message = "."
            if message == "exit" :
                break


def startGameOne():
    tab.select(game1Tab)
    global message

    playerlabel['text'] = "READY"


    canvas = tk.Canvas(game1Tab, height=80, width=480)
    colours = ['white','white','white','white','white']


    while True:
        if message != "" : 
            x = message.split()

            if x[0] == "menu" :
                canvas.destroy()
                playerlabel['text'] = "READY"
                break

            elif x[0] == "turn" :
                playerlabel['text'] = x[1] + ", YOUR TURN"
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
                message = "."    # need to clear message else it loops infinitely back to outcome

                
                #print(canvas.find_all())    # prints all canvas items active
            elif x[0] == "winner" :
                playerlabel['text'] = "WINNER: " + x[1]
        canvas.pack(pady=100, anchor="center")
        game1Tab.update()

def startGameTwo():
    tab.select(game2Tab)
    global message

    playerlabel2['text'] = "READY"
    movelabel['text'] = "LAST MOVE:"
    remainingplayers['text'] = ""


    while True:
        if message != "" : 
            x = message.split()

            if x[0] == "menu" :
                break
            if x[0] == "turn" :
                playerlabel2['text'] = x[1] + ", YOUR TURN"
            if x[0] == "move" :
                movelabel['text'] = "LAST MOVE: " + x[1]
            if x[0] == "players" :
                remainingplayers['text'] = ""
                for i in range(len(x)) :
                    if i != 0 :
                        if remainingplayers['text'] == "" :
                            remainingplayers['text'] = x[i]
                        else :
                            remainingplayers['text'] = remainingplayers['text'] + "\t" + x[i]
                message = "."
            if x[0] == "winner" :
                playerlabel2['text'] = "WINNER: " + x[1] 
        
        game2Tab.update()

            
            




# these buttons have been added to 'gameSelection tab'
b1 = Button(gameSelection, text="MasterMind", command=lambda: threading.Thread(target=startGameOne, daemon=True).start(), height="32", width="32", fg='red', font=buttonFont, relief=SOLID)
b1.pack(padx=5, pady=15, side=tk.LEFT)
b2 = Button(gameSelection, text="Game 2", command=lambda: threading.Thread(target=startGameTwo, daemon=True).start(), height="32", width="32", fg='black', font=buttonFont, relief=GROOVE)
b2.pack(padx=5, pady=15, side=tk.LEFT)
b3 = Button(gameSelection, text="Leaderboard", command=lambda:tab.select(leaderboardTab), height="32", width="32", fg='black', font=buttonFont, relief=GROOVE)
b3.pack(padx=5, pady=15, side=tk.LEFT)

Button(game1Tab, text="Return to Menu", font=buttonFont, command=lambda: tab.select(gameSelection)).place(x=600.0, y=450.0)
Button(leaderboardTab, text="Return to Menu", font=buttonFont, command=lambda: tab.select(gameSelection)).place(x=600.0, y=450.0)

playerlabel = Label(game1Tab, text="READY", fg='black', font=textFont)
playerlabel.pack(pady = 50, anchor="center")

playerlabel2 = Label(game2Tab, text="READY", fg='black', font=textFont)
playerlabel2.pack(pady = 50, anchor="center")

movelabel = Label(game2Tab, text="LAST MOVE:", fg='black', font=textFont)
movelabel.pack(pady=50, anchor="center")

remaining = Label(game2Tab, text="REMAINING PLAYERS", fg='black', font=textFont)
remaining.pack(pady=30, anchor="center")

remainingplayers = Label(game2Tab, text="PLAYER_1\tPLAYER_2\tPLAYER_3", fg='black', font=textFont)
remainingplayers.pack(pady=10, anchor="center")

titleLabel = Label(leaderboardTab, text="LEADERBOARD", fg='black', font=textFont)
titleLabel.pack(pady = 50, anchor="center")
scoresLabel = Label(leaderboardTab, text="PLAYER\t\tSCORE", fg='black', font=textFont)
scoresLabel.pack(pady = 40, anchor="center")
p1Label = Label(leaderboardTab, text="None\t\t0", fg='black', font=textFont)
p1Label.pack(pady = 20, anchor="center")
p2Label = Label(leaderboardTab, text="None\t\t0", fg='black', font=textFont)
p2Label.pack(pady = 20, anchor="center")
p3Label = Label(leaderboardTab, text="None\t\t0", fg='black', font=textFont)
p3Label.pack(pady = 20, anchor="center")
# use ipAddressEntry.get() & portEntry.get() to get TCP things

listener = threading.Thread(target=inputListen)
listener.start()
root.mainloop()
exit()

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



