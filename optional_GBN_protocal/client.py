from socket import socket, AF_INET, SOCK_DGRAM, timeout
from sys import argv
from checksum import ip_checksum
import time,timeit
from numpy import *

window_size=5


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
	add=1
	ack_seqq=-1
	packet_list=[]
        ack_list=[0]*5
    	offset = 0
        count=0
	extra=0
    	seq = 0
        position=0
        t0=timeit.default_timer()
	while ((offset <len(content))or(offset >=len(content)and (not success))):
    		while (offset < len(content)and position<5 and add==1):
        		if offset + SEGMENT_SIZE > len(content):
            			segment = content[offset:]
                        	packet_list.append(segment)
                        	position=position+1
                        	break
        		else:
            			segment = content[offset:offset + SEGMENT_SIZE]
                        	packet_list.append(segment)
                        	position=position+1

        		offset += SEGMENT_SIZE
        	sock.settimeout(1.0)
		i=0
                
                ack_list=[0]*position
        	while(i<position):
                	sock.sendto(ip_checksum(packet_list[i]) + str(seq) + packet_list[i], dest)
                        print seq
                	seq=(seq+1)%5
                        i=i+1            
		all_ack_received = False
        	while not all_ack_received:
            		try:
               	 		message, address = sock.recvfrom(1024)
            		except timeout:
                		print "Timeout"
                                all_ack_received=True
                	else:   
                		checksum = message[:2]
                		ack_seq = message[5]
                		if ip_checksum(message[2:]) == checksum: #and ack_seq == str(seq):
                    			ack_list[(int(ack_seq)+extra)%5]=1;
                			print "ACK package",ack_seq
					ack_seqq=ack_seq
                                        ok=1
                                        i=0
					while(i<position):
                                        	if ack_list[i]==0:
                                                	ok=0
						i=i+1
                                        if ok==1:
                                        	all_ack_received=True
                #sock.sendto(again, dest)
      		print ack_list
        	if ack_list==[1]*position:
                   if position<5:
                        break
		   else:
                	position=0
			packet_list=[]
			seq=(int(ack_seqq)+1)%5
			extra=5-seq
                        success=1
		else:
			success=0
			for i in range(position):
				if ack_list[i]==0:
                        		for k in range(int(i)):
                                                print "packet_list",k,"will be deleted"
                                		del packet_list[0]
					if position==5:
						position=position-i
						
					else:
						position=position-i						
						add=0
					
					seq=(int(ack_seqq)+1)%5
					extra=5-seq
					break
		
                                                                   
        print "total delay is ", timeit.default_timer()-t0
	sock.sendto('over',dest) 
	break
        #x=int(input("File transfer successfully finished, do you want to transfer again? Reply by 1(Yes) or 0(NO)"))
        #if x==0:
		
    sock.close()




'''


 if(count==0):
                                print "first transmit package", seq
           			sock.sendto(ip_checksum(segment) + str(seq) + segment, dest)
                                count=count+1
                        elif(count<5):
				print "retransmit package ", seq, "for" ,count, "times"
				sock.sendto(ip_checksum(segment) + str(seq) + segment, dest)
                                count=count+1
                        else:
                                print"I have retransmitted 5 times and I will close"
                                sock.close()


    while offset < len(content):
        if offset + SEGMENT_SIZE > len(content):
            	segment = content[offset:]
        else:
            	segment = content[offset:offset + SEGMENT_SIZE]
        offset += SEGMENT_SIZE

	ack_received = False
       	while not ack_received:
           	sock.sendto(ip_checksum(segment) + str(seq) + segment, dest)

            	try:
               	 	message, address = sock.recvfrom(1024)
            	except timeout:
                	print "Timeout"
                else:
                	checksum = message[:2]
                	ack_seq = message[5]
                	if ip_checksum(message[2:]) == checksum and ack_seq == str(seq):
                    		ack_received = True
                		print "ACK",ack_seq

        seq = 1 - seq'''
