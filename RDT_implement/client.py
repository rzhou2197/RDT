from socket import socket, AF_INET, SOCK_DGRAM, timeout
from sys import argv
from checksum import ip_checksum
import time,timeit

SEGMENT_SIZE = 100

if __name__ == "__main__":
    dest_addr = argv[1]
    dest_port = int(argv[2])
    dest = (dest_addr, dest_port)
    addr = argv[3]
    port = int(argv[4])
    together=(addr,port)
    filename = argv[5]

    with open(filename) as f:
        content = f.read()

    sock = socket(AF_INET, SOCK_DGRAM)

    sock.bind(together)
    while True:
    	offset = 0
        count=0
    	seq = 0
        t0=timeit.default_timer()
    	while offset < len(content):
        	if offset + SEGMENT_SIZE > len(content):
            		segment = content[offset:]
        	else:
            		segment = content[offset:offset + SEGMENT_SIZE]
        	offset += SEGMENT_SIZE

		ack_received = False
       		while not ack_received:
                        if(count==0):
                                print "first transmit package", seq
                                sock.settimeout(0.8)
           			sock.sendto(ip_checksum(segment) + str(seq) + segment, dest)
                                count=count+1
                        elif(count<5):
				print "retransmit package ", seq, "for" ,count, "times"
                                sock.settimeout(0.8)
				sock.sendto(ip_checksum(segment) + str(seq) + segment, dest)
                                count=count+1
                        else:
                                print"I have retransmitted 5 times and I will close"
                                sock.close()
                                

            		try:
               	 		message, address = sock.recvfrom(1024)
            		except timeout:
                		print "Timeout"
                	else:   
                		checksum = message[:2]
                		ack_seq = message[5]
                		if ip_checksum(message[2:]) == checksum and ack_seq == str(seq):
                    			ack_received = True
                                        count=0
                			print "ACK package",ack_seq

        	seq = 1 - seq
        print "total delay is ", timeit.default_timer()-t0
	sock.sendto('over',dest) 
        x=int(input("File transfer successfully finished, do you want to transfer again? Reply by 1(Yes) or 0(NO)"))
        if x==0:
		break;
    sock.close()





