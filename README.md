# EE4204_UDP
UDP-based client-server socket program for transferring a large message.
Here, the message transmitted from the client to server is read from a large file. 

The message is split into short data-units (DUs) which are sent and acknowledged in batches of size 1, 2, and 3 DUs. 

The sender sends one DU, waits for an acknowledgment (ACK); sends two DUs, waits for an ACK; sends three DUs, waits for an ACK; 
and repeats the above procedure until the entire file is sent. 

The receiver sends an ACK after receiving a DU; sends next ACK after receiving two DUs; sends next ACK after receiving three DUs; 
and repeats the above procedure.
