import socket
from sys import argv
from os import stat
from math import ceil
from struct import *
from time import time_ns
from hashlib import sha256

MAX_FILE_SIZE = 60000
ACK_BUFFER = 12

# exe cmd : python3.7 udp_client.py localhost <port_no> <file_name> <data_unitsize>
try:
    HOST = argv[1]
except IndexError:
    HOST = input("Enter host: ")

try:
    PORT = int(argv[2])
except (IndexError, ValueError) as e:
    PORT = int(input("Enter Port Number: "))

try:
    FILE = argv[3]
except IndexError:
    FILE = input("Enter filename: ")

size = stat(FILE).st_size
print(f"Size of file asked for transfer : {size}\n")
if size > MAX_FILE_SIZE:
    raise ValueError(f"File size exceeds limit of {MAX_FILE_SIZE} Bytes\n")

try:
    DATA_UNIT_SIZE = int(argv[4])
except IndexError:
    DATA_UNIT_SIZE = int(input("Enter packet size in Bytes: "))

num_packs = ceil(size/DATA_UNIT_SIZE)
print(f"Expected total number of data units for transfer : {num_packs}\n")


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s, open(FILE, "rb") as f:
    pkt = pack("!II", size, DATA_UNIT_SIZE)
    s.sendto(pkt, (HOST, PORT))
    batch = 1
    entire_file_message = bytearray()
    start_time = time_ns()
    sent = 0
    while sent < size:
        if(batch > 3):
            batch = 1
        current_num_of_batch = 1
        while(current_num_of_batch <= batch):
            msg = f.read(DATA_UNIT_SIZE)
            entire_file_message.extend(msg)
            s.sendto(msg, (HOST, PORT))
            current_num_of_batch += 1
        ack_data, srv_addr = s.recvfrom(ACK_BUFFER)
        sent_bytes, srv_current_batch, ack_num = unpack("!III", ack_data)
        sent = sent_bytes
        print(
            f"Ack Number : {ack_num} \nCurrenlty received total file size is {sent_bytes} bytes at server with addr : {srv_addr}\n Batch Number at server is : {srv_current_batch}")
        print(
            f"Current Client Batch Number : {batch}\n")
        batch += 1
    transfer_time = time_ns() - start_time
    print(f"Message Transfer Time: {transfer_time} nanoseconds\n")
    print(
        f"SHA256 checksum of sent data: {sha256(entire_file_message).hexdigest()}\n")
    try:
        throughput = (size/1024) / (transfer_time/(10**9))
        print(f"Throughput = {throughput} KB/s")
    except ZeroDivisionError:
        pass
    s.close()
