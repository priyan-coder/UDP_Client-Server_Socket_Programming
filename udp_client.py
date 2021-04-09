import socket
from sys import argv
from os import stat
from math import ceil
from struct import *

PORT = 4950
MAX_FILE_SIZE = 60000
ACK_BUFFER = 8

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
print(f"Size of file asked for transfer : {size}\n")
if size > MAX_FILE_SIZE:
    raise ValueError(f"File size exceeds limit of {MAX_FILE_SIZE} Bytes\n")

try:
    DATA_UNIT_SIZE = int(argv[3])
except IndexError:
    DATA_UNIT_SIZE = int(input("Enter packet size in Bytes: "))

num_packs = ceil(size/DATA_UNIT_SIZE)
print(f"Expected total number of data units for transfer : {num_packs}\n")


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s, open(FILE, "rb") as f:
    pkt = pack("!II", size, DATA_UNIT_SIZE)
    s.sendto(pkt, (HOST, PORT))
    sent = 0
    batch = 1
    while sent < size:
        if(batch > 3):
            batch = 1
        msg = f.read(batch*DATA_UNIT_SIZE)
        s.sendto(msg, (HOST, PORT))
        ack_data, srv_addr = s.recvfrom(ACK_BUFFER)
        ack, srv_current_batch = unpack("!II", ack_data)
        print(
            f"Currenlty received total file size is {ack} bytes at server with addr : {srv_addr}\n Batch Number at server is : {srv_current_batch}")
        sent += batch * DATA_UNIT_SIZE
        print(
            f"Sent by Client : {sent} Bytes\n Current Client Batch Number : {batch}\n")
        batch += 1


# import socket
# from sys import argv
# from os import stat
# from struct import *
# # from time import time_ns
# from math import ceil
# from hashlib import sha256
# import sys

# PORT, MAX_FILE_SIZE, ACK_SIZE = 4950, 60000, 4
# # run in cmd like this: udp_client.py localhost myfile.txt 500 (eg. if packet size is 500)
# try:
#     HOST = argv[1]
# except IndexError:
#     HOST = input("Enter host: ")

# try:
#     FILE = argv[2]
# except IndexError:
#     FILE = input("Enter filename: ")

# size = stat(FILE).st_size
# if size > MAX_FILE_SIZE:
#     raise ValueError(f"File size exceeds limit of {MAX_FILE_SIZE} B")

# try:
#     DATA_UNIT_SIZE = int(argv[3])
# except IndexError:
#     DATA_UNIT_SIZE = int(input("Enter packet size (B): "))

# num_packs = ceil(size/DATA_UNIT_SIZE)
# print(f"Expected total data units for transfer : {num_packs}\n")


# # with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s, open(FILE, "rb") as f:
# #     fmt = calcsize("!II")
# #     print(f"size of format sent : {fmt}")
# #     pkt = pack("!II", DATA_UNIT_SIZE, size)
# #     print(f"Sending {sys.getsizeof(pkt)} bytes packet\n")
# #     s.sendto(pkt, (HOST,PORT))
# #     full_msg = bytearray()
# #     # start = time_ns()
# #     count = 0
# #     sent = 0
# #     j = 1
# #     while(sent < size):
# #         if(j > 3):
# #             j = 1
# #         msg = f.read(j*DATA_UNIT_SIZE)
# #         full_msg.extend(msg)
# #         msg_size = len(msg)
# #         packet = pack(f"{msg_size}s", msg)
# #         s.sendto(packet, (HOST,PORT))
# #         count += j
# #         if(count == unpack(f"!I", s.recvfrom(ACK_SIZE))[0]):
# #             print(f"Received ACK{count}\nTransferred {msg_size} Bytes\n")
# #             continue
# #         j+=1
# #         sent+=msg_size

# # # transfer_time = time_ns() - start
# # print(f"Transferred {count} data units \n")
# # # print(f"Transferred {size} Bytes in {transfer_time} ns \n")
# # # try:
# # #     data_rate = (size/1024) / (rtt/(10**9))
# # #     print(f"Data rate: {data_rate} KB/s")
# # # except ZeroDivisionError:
# # #     pass
# # # print(f"SHA256 checksum of sent data: {sha256(full_msg).hexdigest()}")
