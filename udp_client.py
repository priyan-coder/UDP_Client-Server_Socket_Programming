import socket
from sys import argv
from os import stat
from struct import *
from time import time_ns
from math import ceil
from hashlib import sha256

PORT, MAX_FILE_SIZE, ACK_SIZE = 4950, 60000, 4
# run in cmd like this: udp_client.py localhost myfile.txt 500 (eg. if packet size is 500)
try:
    HOST = argv[1]
except IndexError:
    HOST = input("Enter host: ")

try:
    FILE = argv[2]
except IndexError:
    FILE = input("Enter filename: ")

size = stat(FILE).st_size
if size > MAX_FILE_SIZE:
    raise ValueError(f"File size exceeds limit of {MAX_FILE_SIZE} B")

try:
    DATA_UNIT_SIZE = int(argv[3])
except IndexError:
    DATA_UNIT_SIZE = int(input("Enter packet size (B): "))

num_packs = ceil(size/DATA_UNIT_SIZE)
printf(f"Expected total data units for transfer : {num_packs}\n")


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s, open(FILE, "rb") as f:        
    packet = pack("!II", DATA_UNIT_SIZE, size)
    s.sendto(packet, (HOST,PORT))
    full_msg = bytearray()
    start = time_ns()
    count = 0
    sent = 0
    j = 1
    while(sent < size):
        if(j > 3):
            j = 1
        msg = f.read(j*DATA_UNIT_SIZE)
        full_msg.extend(msg)
        msg_size = len(msg)
        packet = pack(f"{msg_size}s", msg)
        s.sendto(packet, (HOST,PORT))
        if(ack = unpack(f"!I", s.recvfrom(ACK_SIZE))[0]):
            count += j
            print(f"Received ACK{ack}\nTransferred {msg_size} Bytes\n")
            continue
        j+=1
        sent+=msg_size

transfer_time = time_ns() - start
print(f"Transferred {count} data units \n")
print(f"Transferred {size} Bytes in {transfer_time} ns \n")
# try:
#     data_rate = (size/1024) / (rtt/(10**9))
#     print(f"Data rate: {data_rate} KB/s")
# except ZeroDivisionError:
#     pass
# print(f"SHA256 checksum of sent data: {sha256(full_msg).hexdigest()}")