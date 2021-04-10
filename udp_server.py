import socket
from struct import *
from hashlib import sha256

HOST = 'localhost'  # Standard loopback interface address (localhost)
# Port to listen on (non-privileged ports are > 1023)
HEADER_SIZE = 8
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, 0))
        print(f"UDP Server running on PORT: {s.getsockname()[1]}\n")
        header, cli_addr = s.recvfrom(HEADER_SIZE)
        file_size, data_unit_size = unpack("!II", header)
        print(
            f"Connected by Client : {cli_addr}\n, File size for transfer from client : {file_size}\n")

        batch = 1
        pkt_count = 0
        message = bytearray()
        while len(message) < file_size:
            if (batch > 3):
                batch = 1
            current_num_of_batch = 1
            while current_num_of_batch <= batch:
                data = s.recvfrom(data_unit_size)[0]
                message.extend(data)
                current_num_of_batch += 1
            pkt_count += batch
            length_pkt = pack("!III", len(message), batch, pkt_count)
            s.sendto(length_pkt, cli_addr)
            print(
                f"Currently Received {len(message)} Bytes of data since beginning of transfer\n Total Pkts Received so far = {pkt_count}\n")
            batch += 1
        print(
            f"SHA256 checksum of received data: {sha256(message).hexdigest()}\n")
        s.close()
