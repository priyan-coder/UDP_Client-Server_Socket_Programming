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
PORT = 4950    # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    header, cli_addr = s.recvfrom(8)
    file_size, data_unit_size = unpack("!II", header)

    print(
        f"Connected by {cli_addr}\n, File size for transfer from client : {file_size}\n")
    # data_unit_size = int(s.recvfrom(4)[0].decode('utf8'))
    while True:
        # file_size, cli_addr = s.recvfrom(4)
        # file_size = int(file_size.decode('utf8'))

        batch = 1
        pkt_count = 0
        message = bytearray()
        while len(message) < file_size:
            if (batch > 3):
                batch = 1
            data = s.recvfrom(batch * data_unit_size)[0]
            message.extend(data)
            s.sendto(
                bytes(str(len(message))+"\0", encoding='utf8'), cli_addr)
            print(
                f"Currently Received {len(message)} Bytes of data since beginning of transfer\n")
            pkt_count += batch
            batch += 1
