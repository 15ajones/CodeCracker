import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as font
import subprocess
import threading
import socket
import sys
from turtle import screensize

# root window
root = tk.Tk()
root.geometry('720x480')
root.title('InfoProc')

# create a tab
tab = ttk.Notebook(root)
tab.pack(pady=10, expand=True)

# create frames
gameSelection = ttk.Frame(tab, width=720, height=480)
settings = ttk.Frame(tab, width=720, height=480)

gameSelection.pack(fill='both', expand=True)
settings.pack(fill='both', expand=True)

# add frames to tabs
tab.add(gameSelection, text='Game Selection')
tab.add(settings, text='Settings')

# create game buttons
buttonFont = font.Font(family='Arial', weight="bold", size=8)

homescreen = True  #are we in the homescreen
Mastermind = False #are we playing mastermind

# number checking
def only_numbers(char):
    if char.isdigit():
        return True
    elif char == ".":
        return True
    else:
        return False


validation = settings.register(only_numbers)


def start_game1() : 
    global DataLabel
    global game1
    7
    game1 = tk.Tk()
    game1.geometry('720x480')
    game1.title('Master Mind')

    DataLabel = Label(game1, text="Waiting for incoming data...")
    DataLabel.place(x=20.0, y=80.0)
    game1.update()

    threading.Thread(target=mainloop(), daemon=True)

def mm_game() :
    mm = tk.Tk()
    mm.geometry('720x480')
    mm.title('Master Mind')

    userlabel = Label(game1, text="[USER]")
    userlabel.place(x=20.0, y=80.0)
    mm.update()

def mainloop() :
    
    while True :
        x = input("Waiting for input")
        x_array = x.split()

        if homescreen :
            if x_array[0] == "play" :
                match x_array[1] :
                    case "mastermind" :
                        threading.Thread(target=mm_game(), daemon=True)
                        homescreen = 0
                        Mastermind = 1
                    


        elif Mastermind :
            if x_array[0] == "turn"
                turn = x_array[1]


        
        #DataLabel.config(text=x)

        game1.update()






#Button(gameSelection, text="MasterMind", command=start_game1(), height="32", width="32", bg='red', fg='black', font=buttonFont).pack(padx=5, pady=15, side=tk.LEFT)

threading.Thread(target=mainloop(), daemon=True)



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
