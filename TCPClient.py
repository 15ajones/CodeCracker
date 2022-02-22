import subprocess
import time
import socket
import sys, platform
import ctypes, ctypes.util
import os.path

class intel_jtag_uart:
    
    # The error strings below were copied from following MIT-licensed file:
    # https://github.com/thotypous/alterajtaguart/blob/master/software/jtag_atlantic.h
    ERROR_MSGS = [
        "No error",
        "Unable to connect to local JTAG server",
        "More than one cable available, provide more specific cable name",
        "Cable not available",
        "Selected cable is not plugged",
        "JTAG not connected to board, or board powered down",
        "Another program is already using the UART",
        "More than one UART available, specify device/instance",
        "No UART matching the specified device/instance",
        "Selected UART is not compatible with this version of the library"
    ]

    function_table = {
        'jtagatlantic_open'             : { 
            'Linux'         : '_Z17jtagatlantic_openPKciiS0_',
            'Windows'       : '?jtagatlantic_open@@YAPEAUJTAGATLANTIC@@PEBDHH0@Z',
            'argtypes'      : [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p],
            'restype'       : ctypes.c_void_p,
        },
        'jtagatlantic_read'             : { 
            'Linux'         : '_Z17jtagatlantic_readP12JTAGATLANTICPcj',
            'Windows'       : '?jtagatlantic_read@@YAHPEAUJTAGATLANTIC@@PEADI@Z',
            'argtypes'      : [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint],
            'restype'       : ctypes.c_int
        },
        'jtagatlantic_close'            : { 
            'Linux'         : '_Z18jtagatlantic_closeP12JTAGATLANTIC',
            'Windows'       : '?jtagatlantic_close@@YAXPEAUJTAGATLANTIC@@@Z',
            'argtypes'      :  [ctypes.c_void_p],
            'restype'       :  None
        },
        'jtagatlantic_flush'            : { 
            'Linux'         : '_Z18jtagatlantic_flushP12JTAGATLANTIC',
            'Windows'       : '?jtagatlantic_flush@@YAHPEAUJTAGATLANTIC@@@Z',
            'argtypes'      : [ctypes.c_void_p],
            'restype'       :  None
        },
        'jtagatlantic_write'            : { 
            'Linux'         : '_Z18jtagatlantic_writeP12JTAGATLANTICPKcj',
            'Windows'       : '?jtagatlantic_write@@YAHPEAUJTAGATLANTIC@@PEBDI@Z',
            'argtypes'      : [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint],
            'restype'       : ctypes.c_int
        },
        'jtagatlantic_get_info'         : { 
            'Linux'         : '_Z21jtagatlantic_get_infoP12JTAGATLANTICPPKcPiS4_',
            'Windows'       : '?jtagatlantic_get_info@@YAXPEAUJTAGATLANTIC@@PEAPEBDPEAH2@Z',
            'argtypes'      : [ ctypes.c_void_p, POINTER(ctypes.c_char_p), POINTER(ctypes.c_int), POINTER(ctypes.c_int) ],
            'restype'       : None,
        },
        'jtagatlantic_get_error'        : { 
            'Linux'         : '_Z22jtagatlantic_get_errorPPKc',
            'Windows'       : '?jtagatlantic_get_error@@YA?AW4JATL_ERROR@@PEAPEBD@Z',
            'argtypes'      : [POINTER(ctypes.c_char_p)], 
            'restype'       : ctypes.c_int,
        },
        'jtagatlantic_wait_open'        : { 
            'Linux'         : '_Z22jtagatlantic_wait_openP12JTAGATLANTIC',
            'Windows'       : '?jtagatlantic_wait_open@@YAHPEAUJTAGATLANTIC@@@Z',
            'argtypes'      : [ctypes.c_void_p],
            'restype'       : ctypes.c_int,
        },
        'jtagatlantic_scan_thread'      : { 
            'Linux'         : '_Z24jtagatlantic_scan_threadP12JTAGATLANTIC',
            'Windows'       : '?jtagatlantic_scan_thread@@YAXPEAUJTAGATLANTIC@@@Z',
            'argtypes'      : [ctypes.c_void_p],
            'restype'       : ctypes.c_int,
        },
        'jtagatlantic_cable_warning'    : { 
            'Linux'         : '_Z26jtagatlantic_cable_warningP12JTAGATLANTIC',
            'Windows'       : '?jtagatlantic_cable_warning@@YAHPEAUJTAGATLANTIC@@@Z',
            'argtypes'      : [ctypes.c_void_p],
            'restype'       : ctypes.c_int,
        },
        'jtagatlantic_is_setup_done'    : { 
            'Linux'         : '_Z26jtagatlantic_is_setup_doneP12JTAGATLANTIC',
            'Windows'       : '?jtagatlantic_is_setup_done@@YA_NPEAUJTAGATLANTIC@@@Z',
            'argtypes'      : [ctypes.c_void_p],
            'restype'       : ctypes.c_int,
        },
        'jtagatlantic_bytes_available'  : { 
            'Linux'         : '_Z28jtagatlantic_bytes_availableP12JTAGATLANTIC',
            'Windows'       : '?jtagatlantic_bytes_available@@YAHPEAUJTAGATLANTIC@@@Z',
            'argtypes'      : [ctypes.c_void_p],
            'restype'       : ctypes.c_int,
        },
    }
    
    @classmethod
    def read(self):
            """Read from the JTAG UART.
            Returns a bytes object.
            Raises an exception when the connection with the JTAG UART is broken.
            """
            buf_len     = self.bytes_available()
            buf         = bytes(buf_len)

            bytes_read = intel_jtag_uart.function_table['jtagatlantic_read']['ptr'](
                                self.handle,
                                ctypes.c_char_p(buf),
                                ctypes.c_uint(buf_len)
                            )

            if bytes_read == -1:
                raise Exception("Connection broken")

            return buf



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



#end jtag part
client_socket.close()

