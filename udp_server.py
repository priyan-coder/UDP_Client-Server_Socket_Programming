# import socket
# from struct import *
# from hashlib import sha256
# import sys

# HOST, PORT, HEADER = "", 4950, 8

# with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
#     s.bind((HOST, PORT))
#     while True:
#             msg = bytearray()
#             count = 0
#             received_stream, addr = s.recvfrom(HEADER)
#             print(f"Connected by : {addr}")
#             print(f"size of object received : {sys.getsizeof(received_stream)}")
#             DATA_UNIT_SIZE, TOTAL_FILE_SIZE = unpack("!II", received_stream)
#             j = 1
#             while len(msg) < TOTAL_FILE_SIZE:
#                 if(j > 3):
#                     j = 1
#                 msg.extend(s.recvfrom(j*DATA_UNIT_SIZE)[0])
#                 count += j
#                 ack = pack(f"!I", count)
#                 s.sendto(ack, (HOST, PORT))
#                 j += 1
#         # print(f"Received {count} data units\n")
#         # print(f"Received {len(msg) + HEADER} B packets")
#         # print(f"SHA256 checksum of received data: {sha256(msg).hexdigest()}")


import socket
from struct import *

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 6000  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    header, cli_addr = s.recvfrom(8)
    file_size, data_unit_size = unpack("!II", header)
    print(
        f"Connected by {cli_addr}\n, File size for transfer from client : {file_size}\n")
    while True:
        batch = 1
        pkt_count = 0
        message = bytearray()
        while len(message) < file_size:
            if (batch > 3):
                batch = 1
            data = s.recvfrom(batch * data_unit_size)[0]
            message.extend(data)
            length_pkt = pack("!II", len(message), batch)
            s.sendto(length_pkt, cli_addr)
            pkt_count += batch
            print(
                f"Currently Received {len(message)} Bytes of data since beginning of transfer\n Total Pkts Received so far = {pkt_count}\n")
            batch += 1
