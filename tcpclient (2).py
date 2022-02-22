import socket
import subprocess
import time
import socket
import sys, platform
import ctypes, ctypes.util
import os.path


def send_on_jtag(cmd):  # sends y or n to jtag (sent to board)
    
    assert cmd == 'y' or cmd == 'n', "Please make the cmd a single character"    # check if atleast one character is being sent down
    # inputCmd = "nios2-terminal {}".format(cmd);                 # call nios2-terminal and insert characters using <<<
    # subprocess allows python to run a bash command
    output = subprocess.Popen('C:\\intelFPGA_lite\\18.0\\quartus\\bin64\\nios2-terminal.exe', shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    strthing = cmd + '\n'
    output.stdin.write(bytes(strthing,'utf-8'))
    output.stdin.flush()
    line = output.stdout.readlines()
    print(line)


def perform_computation(): # checks whether inpoutted code is equal to passcode from ec2 server
    #need to read jtag-uart port for board_code
    board_code = intel_jtag_uart.read()

    if (board_code == passcode_ec2):
        var = 'y'
        res = send_on_jtag(var)                                   # example of how to use send_on_jtag function
        print(res)
        #time.sleep(1000)

    else:
        var = 'n'
        res = send_on_jtag(var)                                   # example of how to use send_on_jtag function
        print(res)



#TCP Client:



print("We're in tcp client...");

#the server name and port client wishes to access
server_name = '35.176.178.191'   # change to ec2 public IPv4
server_port = 12000
#create a TCP client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Set up a TCP connection
#connection_socket will be assigned to this client on the server side
client_socket.connect((server_name, server_port))

#some work
msg = input("Enter a string to test if it is alphanumeric: ");

#send the message  to the udp server
client_socket.send(msg.encode())

#return values from the server
passcode_ec2 = client_socket.recv(1024)
# print(passcode_ec2.decode())
pacccode_ec2 = passcode_ec2.decode
#start jtag part



def main():
    perform_computation()
   
if __name__ == '__main__':
    main()

print("We're in tcp client...");

#the server name and port client wishes to access
server_name = '35.176.178.191'  #ipv4 of ec2
server_port = 12000
#create a TCP client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Set up a TCP connection
#connection_socket will be assigned to this client on the server side
client_socket.connect((server_name, server_port))
#some work
msg = input("Enter a string to test if it is alphanumeric: ");

#send the message  to the udp server
client_socket.send(msg.encode())

#return values from the server
msg = client_socket.recv(1024)
print(msg.decode())
client_socket.close()




