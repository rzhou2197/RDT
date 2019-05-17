Implemented in ubuntu16.04

UDP transfer file: 
                   Simulate UDP file transfer by adding bit errors and packet loss randomly.
                   UDP has the basic checksum function.
                   
                   use gcc -o server server.c -lpthread to compile the server.c 
                   use gcc -o client client.c to compile the client.c
                   run ./server and the run ./client(the order can't be changed)
                   
Implement RDT protocol(Stop and wait ARQ):
                   When packet is received by receiver in order and no bit error is found, send ACK to sender and the sender will 
                   transmit next packet. Otherwise, the sender will retransmit the packet.
                   
                   use gcc -o server server.c -lpthread to compile the server.c 
                   use gcc -o client client.c to compile the client.c
                   run ./server and the run ./client(the order can't be changed)
            
Go-Back_N protocol:
                   The sending process continues to send a number of frames specified by a window size even without 
                   receiving an acknowledgement (ACK) packet from the receiver.The sender will detect that all of the frames 
                   since the first lost frame are outstanding, and will go back to the sequence number of the last ACK 
                   it received from the receiver process and fill its window starting with that frame and continue the
                   process over again.
                   
                   use gcc -o server server.c -lpthread to compile the server.c 
                   use gcc -o client client.c to compile the client.c
                   run ./server and the run ./client(the order can't be changed)
