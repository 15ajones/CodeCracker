import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as font


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

# these buttons have been added to 'gameSelection tab'
Button(gameSelection, text="Game 1", height="32", width="32", bg='red', fg = 'white', font = buttonFont).pack(padx=5, pady=15, side=tk.LEFT)
Button(gameSelection, text="Game 2", height="32", width="32", bg='green', fg = 'white', font = buttonFont).pack(padx=5, pady=15, side=tk.LEFT)
Button(gameSelection, text="Game 3", height="32", width="32", bg='blue', fg = 'white', font = buttonFont).pack(padx=5, pady=15, side=tk.LEFT)

# settings tab
ipName = Label(settings, text="IP: ")
ipName.pack(side = LEFT)
ipAddressEntry = Entry(settings)
ipAddressEntry.pack(side = LEFT)

portName = Label(settings, text="Port: ")
portName.pack(side = LEFT)
portEntry = Entry(settings)
portEntry.pack(side = LEFT)

root.mainloop()
