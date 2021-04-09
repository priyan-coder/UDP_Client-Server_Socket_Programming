import socket
from struct import *
from hashlib import sha256

HOST, PORT, HEADER = "", 4950, 8

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    while True:
            msg = bytearray()
            count = 0
            DATA_UNIT_SIZE, TOTAL_FILE_SIZE = unpack("!II", s.recvfrom(HEADER))
            j = 1
            while len(msg) < TOTAL_FILE_SIZE:
                if(j > 3):
                    j = 1
                msg.extend(s.recvfrom(j*DATA_UNIT_SIZE))
                count +=j
                ack = pack(f"!I",count)
                s.sendto(ack, (HOST, PORT))
                j+=1
        print(f"Received {len(msg) + HEADER} B packets")
        # print(f"SHA256 checksum of received data: {sha256(msg).hexdigest()}")