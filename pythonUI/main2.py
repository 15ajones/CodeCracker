import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as font
import subprocess
import threading
import socket
import sys
#from tkinter.tix import InputOnly

server_name = "localhost"
server_port = 12000

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


# number checking
def only_numbers(char):
    if char.isdigit():
        return True
    elif char == ".":
        return True
    else:
        return False


validation = settings.register(only_numbers)

def changeText():
    global server_name, server_port
    TCPValues.config(text="TCP Set: " + ipAddressEntry.get() + ":" + portEntry.get())
    server_name = ipAddressEntry.get()
    server_port = int(portEntry.get())

def setLocalHost():
    global chkValue
    global server_name
    if chkValue == 0:
        ipVar.set("localhost")
        server_name = "localhost"
        chkValue = 1
    else:
        chkValue = 0
        ipVar.set("")

def startTCP():

    game1 = tk.Tk()
    game1.geometry('720x480')
    game1.title('Master Mind')

    TCPDataLabel = Label(game1, text="Waiting for incoming data...")
    TCPDataLabel.place(x=20.0, y=80.0)
    game1.update()
    
    threading.Thread(target = maincycle, daemon=True)

    #threading.Thread(target=masterMind).start()

def maincycle() : 
    global TCPDataLabel
    global game1
    
    while True:
        x = input("waiting for input label")

        TCPDataLabel.config(text=x)
        
        game1.update()

    


chkValue = tk.BooleanVar()
chkValue = False

TCPTitle = Label(settings, text="Enter IP & Port")
TCPTitle.place(x=20.0, y=10.0)

ipVar = tk.StringVar()
ipName = Label(settings, text="IP")
ipName.place(x=20.0, y=40.0)
ipAddressEntry = Entry(settings, textvariable=ipVar, validate="key", validatecommand=(validation, '%S'))
ipAddressEntry.place(x=80.0, y=40.0)

localhost = Checkbutton(settings, text = "localhost", command=setLocalHost, var=chkValue)
localhost.place(x=280.0, y=40.0)

portVar = tk.StringVar()
portName = Label(settings, text="Port")
portName.place(x=20.0, y=80.0)
portEntry = Entry(settings, textvariable=portVar, validate="key", validatecommand=(validation, '%S'))
portEntry.place(x=80.0, y=80.0)

TCPValues = Label(settings, text="TCP Set: 0.0.0.0: 00000")
TCPValues.place(x=20.0, y=170.0)

saveButton = Button(settings, text="Save", command=changeText, height="1", width="25")
saveButton.place(x=20.0, y=120.0)

#connectTCP = threading.Thread(target=startTCP)
# these buttons have been added to 'gameSelection tab'
Button(gameSelection, text="MasterMind", command=startTCP, height="32", width="32", bg='red', fg='black', font=buttonFont).pack(padx=5, pady=15, side=tk.LEFT)
Button(gameSelection, text="Game 2", height="32", width="32", bg='green', fg='black', font=buttonFont).pack(padx=5, pady=15, side=tk.LEFT)
Button(gameSelection, text="Game 3", height="32", width="32", bg='blue', fg='black', font=buttonFont).pack(padx=5, pady=15, side=tk.LEFT)


# use ipAddressEntry.get() & portEntry.get() to get TCP things
root.mainloop()
