import socket
# https://docs.python.org/3/library/socket.html
from sys import argv
# https://www.geeksforgeeks.org/python-os-stat-method/
from os import stat
# https://stackoverflow.com/questions/14215715/reading-a-binary-file-into-a-struct
from struct import *
# https://docs.python.org/3/library/struct.html#struct.pack
from time import time_ns
# https://www.geeksforgeeks.org/python-time-time_ns-method/

# specify the PORT_NUM, MAXIMUM_SIZE_OF_FILE_TO_TRANSFER, HEADER_SIZE, ACK_SIZE
PORT, MAXSIZE, HEADER, ACK_SIZE = 4950, 30000, 4, 1
# run the program in cmd like this: tcp_client2.py localhost myfile.txt
try:
    HOST = argv[1]
except IndexError:
    HOST = input("Enter host: ")

try:
    FILE = argv[2]
except IndexError:
    FILE = input("Enter filename: ")

# get the size of the file to be transferred in bytes 
size = stat(FILE).st_size
if size > MAXSIZE:
    raise ValueError(f"File size exceeds limit of {MAXSIZE} B")

# Opens the file as read-only in binary format and starts reading from the beginning of the file. 
with open(FILE, "rb") as f:
    # msg is a binary array 
    msg = f.read()

# Packet in the format : Network order i.e. Big Endian ==> Unsigned int, string of char[size]
# sending the size of the file and its binary byte stream
packet = pack(f"!I{size}s", size, msg)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:        
    s.connect((HOST, PORT))
    # start timer in nano sec 
    start = time_ns()  
    # sending all packet until data sent, returns NONE, when all data sent or error
    s.sendall(packet)
    # unpack in the format : Network Order ==> unsigned char of 1 byte 
    # ack accesses the unpacked acknowledgement from server which is the first element of the tuple 
    ack = unpack(f"!{ACK_SIZE}B", s.recv(ACK_SIZE))[0]

# stop timer when received ack 
rtt = time_ns() - start
size += HEADER
print(f"Received ACK{ack}\nTransferred {size} B in {rtt} ns")

# calculation of data rate 
try:
    data_rate = (size/1024) / (rtt/(10**9))
    print(f"Data rate: {data_rate} KB/s")
except ZeroDivisionError:
    pass

# checkin congruecny between sent and received 
with open("myfile.txt", newline="") as f1, open("received.txt", newline="") as f2:
    txt1, txt2 = f1.read(), f2.read()
if txt2 == txt1:
    print("Received message is identical to original")
else:
    print("Received message is different from original")