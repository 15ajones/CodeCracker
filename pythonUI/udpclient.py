from ctypes import sizeof
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as font
import threading
import sys
from xml.etree.ElementPath import get_parent_map
import socket

host_name = '35.176.178.191'
host_port = 12000

ui_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ui_socket.bind(('', 11000))

ping = "hello server"

ui_socket.sendto(ping.encode(), (host_name, host_port))
print("waiting for message")
message = ui_socket.recv(1024)
print("message received")
message = message.decode()
print(message)