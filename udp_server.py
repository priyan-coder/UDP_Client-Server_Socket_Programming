import socket
from struct import *
from hashlib import sha256

HOST, PORT, HEADER = "", 4950, 8

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    while True:
            msg = bytearray()
            pack_size, total_size = unpack("!II", s.recvfrom(HEADER))
            j = 1
            while len(msg) < total_size:
                if(j > 3):
                    j = 1
                msg.extend(s.recvfrom(j*pack_size))
                ack = pack(f"!I",j*pack_size)
                s.sendto(ack, (HOST, PORT))
                j+=1
        print(f"Received {len(msg) + HEADER} B packets")
        # print(f"SHA256 checksum of received data: {sha256(msg).hexdigest()}")