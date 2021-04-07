# https://docs.python.org/3/library/socket.html
import socket
# https://docs.python.org/3/library/struct.html
from struct import *


HOST, PORT, HEADER, ACK_SIZE, ack_num = "", 4950, 4, 1, 1
# The HEADER is 4 bytes in which the size of the msg to be 
# received from client upon unpacking is specified
# This is because size of integer is 4 bytes

# creation of socket s and binding it to the host and port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            # unpack to convert byte stream received in network order i.e. big endian ==> unsigned integers
            # size contains the size of msg to be received 
            size = unpack("!I", conn.recv(HEADER))[0]
            # msg is a bytes stream or bytes object 
            msg = conn.recv(size)
            # acks is a bytes oject that contains acknowledgement num formatted into a 1 byte unsigned char
            ack = pack(f"!{ACK_SIZE}B", ack_num)
            conn.sendall(ack)
        with open("received.txt", "wb") as f:
            f.write(msg)
        print(f"Sent ACK{ack_num}")
        ack_num += 1
        # print(msg)


# https://stackoverflow.com/questions/27893804/udp-client-server-socket-in-python
