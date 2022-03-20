from ctypes import sizeof
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as font
import threading
import sys
from xml.etree.ElementPath import get_parent_map
import socket
import os
from playsound import playsound

#from grpc import xds_channel_credentials
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
# server stuff
host_name = '18.132.60.200'
host_port = 12000

ui_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ui_socket.bind(('', 11090))

ping = "ui"
ui_socket.sendto(ping.encode(), (host_name, host_port))

def playMusic():
    print("Audio on")
    playsound('music.mp3')

message = ""
p1_name = "None"
p2_name = "None"
p3_name = "None"
p1_score = 0
p2_score = 0
p3_score = 0

# root window
root = tk.Tk()
root.geometry("1920x1080")
root.configure(bg = "#323232")
root.title('InfoProc')
style = ttk.Style()
style.layout('TNotebook.Tab', [])

# create a tab
tab = ttk.Notebook(root)
tab.pack(pady=10, expand=True)

# create frames
gameSelection = ttk.Frame(tab, width=1280, height=720)
gameSelection.pack(fill='both', expand=True)
game1Tab = ttk.Frame(tab, width=1280, height=720)
game1Tab.pack(fill='both', expand=True)
game2Tab = ttk.Frame(tab, width=1280, height=720)
game2Tab.pack(fill='both', expand=True)
leaderboardTab = ttk.Frame(tab, width=1280, height=720)
leaderboardTab.pack(fill='both', expand=True)

# add frames to tabs
tab.add(gameSelection, text='Game Selection')
tab.add(game1Tab, text='Game 1')
tab.add(game2Tab, text='Game 2')
tab.add(leaderboardTab, text='Leaderboard')

# create game buttons
buttonFont = font.Font(family='Arial', weight="bold", size=8)
textFont = font.Font(family='Arial', weight="bold", size=50)
mmtextFont = font.Font(family='Arial', weight="bold", size=36)

def btn_clicked():
    print("Button Clicked")

def inputListen():
    global message, p1_score, p2_score, p3_score, p1_name, p2_name, p3_name
    while True:
        #print("[INPUT]:", end=' ')
        #sys.stdout.flush()
        print("waiting for message")
        message = ui_socket.recv(1024)
        print("message received")
        message = message.decode()
        #message = sys.stdin.readline().rstrip()          #Testing without server, comment 4 line above
        print(message)
        if message != " ":
            if message == "right":
                #pyimage6 is mastermind img reference name
                if mastermind_button['image'] == "pyimage10":
                    memory_button['image'] = img1_1
                    mastermind_button['image'] = img2
                #pyimage6 is memory img reference name
                elif memory_button['image'] == "pyimage8":
                    leaderboard_button['image'] = img0_1
                    memory_button['image'] = img1
                    
                else:
                    print("bad move")

            if message == "left":
                #pyimage6 is memory img eference name
                if memory_button['image'] == "pyimage8":
                    memory_button['image'] = img1
                    mastermind_button['image'] = img2_1
                #pyimage6 is leaderboard img reference name
                elif leaderboard_button['image'] == "pyimage6":
                    leaderboard_button['image'] = img0
                    memory_button['image'] = img1_1
                else:
                    print("bad move")

            if message == "select":
                if mastermind_button['image'] == "pyimage10":
                    threadGameOne = threading.Thread(target=startGameOne, daemon=True)
                    threadGameOne.start()
                elif memory_button['image'] == "pyimage8":
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
                    p1nLabel['text'] = p1_name
                    mmp1nLabel['text'] = p1_name
                    mp1nLabel['text'] = p1_name
                    p1sLabel['text'] = str(p1_score)
                elif msg[1] == p2_name or p2_name == "None":
                    p2_name = msg[1]
                    p2_score = msg[2]
                    p2nLabel['text'] = p2_name
                    mmp2nLabel['text'] = p2_name
                    mp2nLabel['text'] = p2_name
                    p2sLabel['text'] = str(p2_score)
                elif msg[1] == p3_name or p3_name == "None":
                    p3_name = msg[1]
                    p3_score = msg[2]
                    p3nLabel['text'] = p3_name
                    mmp3nLabel['text'] = p3_name
                    mp3nLabel['text'] = p3_name
                    p3sLabel['text'] = str(p3_score)

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


    canvas = tk.Canvas(game1Tab, width=500, height=120, bg='#164181', highlightthickness=0)
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
                canvas.create_rectangle(105,5,180,80, fill=colours[1], outline=colours[1])
                canvas.create_rectangle(205,5,280,80, fill=colours[2], outline=colours[2])
                canvas.create_rectangle(305,5,380,80, fill=colours[3], outline=colours[3])
                canvas.create_rectangle(405,5,480,80, fill=colours[4], outline=colours[4])
                message = "."    # need to clear message else it loops infinitely back to outcome

                
                #print(canvas.find_all())    # prints all canvas items active
            elif x[0] == "winner" :
                playerlabel['text'] = "WINNER: " + x[1]
                playsound('winner.mp3')
        canvas.place(x=200, y=400)
        game1Tab.update()

def startGameTwo():
    tab.select(game2Tab)
    global message
    canvas = tk.Canvas(game2Tab, width=1280, height=720)

    playerlabel2['text'] = "READY"
    movelabel['text'] = ""
    remainingplayers['text'] = ""


    # while True:
    #     if message != "" : 
    #         x = message.split()

    #         if x[0] == "menu" :
    #             break
    #         if x[0] == "turn" :
    #             playerlabel2['text'] = x[1] + ", YOUR TURN"
    #         if x[0] == "move" :
    #             movelabel['text'] = "LAST MOVE: " + x[1]
    #         if x[0] == "players" :
    #             remainingplayers['text'] = ""
    #             for i in range(len(x)) :
    #                 if i != 0 :
    #                     if remainingplayers['text'] == "" :
    #                         remainingplayers['text'] = x[i]
    #                     else :
    #                         remainingplayers['text'] = remainingplayers['text'] + "\n" + x[i]
    #             message = "."
    #         if x[0] == "winner" :
    #             playerlabel2['text'] = "WINNER: " + x[1] 
    #             playsound('winner.mp3')
        
    #     game2Tab.update()
    while True:
        if message != "" :
            x = message.split()

            if x[0] == "menu":
                break
            if x[0] == "start":
                playerlabel2['text'] = "GO"
                movelabel['text'] = x[1]
            if x[0] == "winner" :
                playerlabel2['text'] = "WINNER: " + x[1]
                playsound('winner.mp3')
        game2Tab.update()


            
            
# UI STUFFFF


menu_background_img = PhotoImage(file = f"img/menu_background.png")
menu_background = Label(gameSelection, image=menu_background_img, bd=0, highlightthickness=0, relief='ridge')
menu_background.place(x=0, y=0)

mm_background_img = PhotoImage(file = f"img/mm_background.png")
mm_background = Label(game1Tab, image=mm_background_img, bd=0, highlightthickness=0, relief='ridge')
mm_background.place(x=0, y=0)

guess_background_img = PhotoImage(file = f"img/guess_background.png")
guess_background = Label(game2Tab, image=guess_background_img, bd=0, highlightthickness=0, relief='ridge')
guess_background.place(x=0, y=0)

leader_background_img = PhotoImage(file = f"img/leader_background.png")
leader_background = Label(leaderboardTab, image=leader_background_img, bd=0, highlightthickness=0, relief='ridge')
leader_background.place(x=0, y=0)

# leaderboard button
img0 = PhotoImage(file = f"img/img0.png")
img0_1 = PhotoImage(file = f"img/img0_1.png")
leaderboard_button = Button(
    gameSelection,
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command=lambda:tab.select(leaderboardTab),
    relief = "flat")

leaderboard_button.place(
    x = 361+640, y = -151+360,
    width = 216,
    height = 210)

# memory button
img1 = PhotoImage(file = f"img/img1.png")
img1_1 = PhotoImage(file = f"img/img1_1.png")
memory_button = Button(
    gameSelection,
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command=lambda: threading.Thread(target=startGameTwo, daemon=True).start(),
    relief = "flat")

memory_button.place(
    x = -108+640, y = -159+360,
    width = 412,
    height = 404)

# mastermind button
img2 = PhotoImage(file = f"img/img2.png")
img2_1 = PhotoImage(file = f"img/img2_1.png")
mastermind_button = Button(
    gameSelection,
    image = img2_1,
    borderwidth = 0,
    highlightthickness = 0,
    command=lambda: threading.Thread(target=startGameOne, daemon=True).start(),
    relief = "flat")

mastermind_button.place(
    x = -574+640, y = -163+360,
    width = 412,
    height = 404)

img3 = PhotoImage(file = f"img/img3.png")
button3 = Button(
    gameSelection,
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = root.destroy,
    relief = "flat")

button3.place(
    x = 507+640, y = 221+360,
    width = 115,
    height = 120)

img4 = PhotoImage(file = f"img/back.png")
button4 = Button(
    game1Tab,
    image = img4,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda: tab.select(gameSelection),
    relief = "flat")

button4.place(
    x = 866, y = 580,
    width = 268,
    height = 122)

button5 = Button(
    game1Tab,
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

button5.place(
    x = 1147, y = 582,
    width = 115,
    height = 120)

button6 = Button(
    game2Tab,
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

button6.place(
    x = 1147, y = 582,
    width = 115,
    height = 120)

button7 = Button(
    leaderboardTab,
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

button7.place(
    x = 1147, y = 582,
    width = 115,
    height = 120)

button8 = Button(
    game2Tab,
    image = img4,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda: tab.select(gameSelection),
    relief = "flat")

button8.place(
    x = 866, y = 580,
    width = 268,
    height = 122)

button9 = Button(
    leaderboardTab,
    image = img4,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda: tab.select(gameSelection),
    relief = "flat")

button9.place(
    x = 866, y = 580,
    width = 268,
    height = 122)


# these buttons have been added to 'gameSelection tab'
#b1 = Button(gameSelection, text="MasterMind", command=lambda: threading.Thread(target=startGameOne, daemon=True).start(), height="32", width="32", fg='red', font=buttonFont, relief=SOLID)
#b1.pack(padx=5, pady=15, side=tk.LEFT)
#b2 = Button(gameSelection, text="Game 2", command=lambda: threading.Thread(target=startGameTwo, daemon=True).start(), height="32", width="32", fg='black', font=buttonFont, relief=GROOVE)
#b2.pack(padx=5, pady=15, side=tk.LEFT)
#b3 = Button(gameSelection, text="Leaderboard", command=lambda:tab.select(leaderboardTab), height="32", width="32", fg='black', font=buttonFont, relief=GROOVE)
#b3.pack(padx=5, pady=15, side=tk.LEFT)

playerlabel = Label(game1Tab, text="READY", fg='white', font=mmtextFont, background="#164181")
playerlabel.place(x=200, y=260)

playerlabel2 = Label(game2Tab, text="READY", fg='white', font=mmtextFont, background="#164181")
playerlabel2.place(x=200, y=260)

movelabel = Label(game2Tab, text="LAST MOVE:", fg='white', font=mmtextFont, background="#164181")
movelabel.place(x=200, y=340)

remaining = Label(game2Tab, text="REMAINING PLAYERS: ", fg='white', font=mmtextFont, background="#164181")
remaining.place(x=200, y=450)

remainingplayers = Label(game2Tab, text="PLAYER_1\nPLAYER_2\nPLAYER_3", fg='white', font=mmtextFont, background="#164181")
remainingplayers.place(x=200, y=490)

# Leaderboard
playerLabel = Label(leaderboardTab, text="Players", fg='white', font=textFont, background="#A755A9")
playerLabel.place(x=150, y=200)
p1nLabel = Label(leaderboardTab, text="None", fg='white', font=textFont, background="#A755A9")
p1nLabel.place(x=150, y=300)
p2nLabel = Label(leaderboardTab, text="None", fg='white', font=textFont, background="#A755A9")
p2nLabel.place(x=150, y=380)
p3nLabel = Label(leaderboardTab, text="None", fg='white', font=textFont, background="#A755A9")
p3nLabel.place(x=150, y=460)

scoresLabel = Label(leaderboardTab, text="Scores", fg='white', font=textFont, background="#A755A9")
scoresLabel.place(x=600, y=200)
p1sLabel = Label(leaderboardTab, text="0", fg='white', font=textFont, background="#A755A9")
p1sLabel.place(x=600, y=300)
p2sLabel = Label(leaderboardTab, text="0", fg='white', font=textFont, background="#A755A9")
p2sLabel.place(x=600, y=380)
p3sLabel = Label(leaderboardTab, text="0", fg='white', font=textFont, background="#A755A9")
p3sLabel.place(x=600, y=460)

# Mastermind Players

mmp1nLabel = Label(game1Tab, text="None", fg='white', font=textFont, background="#A755A9")
mmp1nLabel.place(x=980, y=240)
mmp2nLabel = Label(game1Tab, text="None", fg='white', font=textFont, background="#A755A9")
mmp2nLabel.place(x=980, y=320)
mmp3nLabel = Label(game1Tab, text="None", fg='white', font=textFont, background="#A755A9")
mmp3nLabel.place(x=980, y=400)

# Memory Players
mp1nLabel = Label(game2Tab, text="None", fg='white', font=textFont, background="#A755A9")
mp1nLabel.place(x=980, y=240)
mp2nLabel = Label(game2Tab, text="None", fg='white', font=textFont, background="#A755A9")
mp2nLabel.place(x=980, y=320)
mp3nLabel = Label(game2Tab, text="None", fg='white', font=textFont, background="#A755A9")
mp3nLabel.place(x=980, y=400)

#use ipAddressEntry.get() & portEntry.get() to get TCP things

listener = threading.Thread(target=inputListen)
listener.start()
musicStart = threading.Thread(target=playMusic)
musicStart.start()
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


# game start -> display ready?
# 5 letter message -> display  
# winner name 


