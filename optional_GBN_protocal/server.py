from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv, stdout
from checksum import ip_checksum
import time
from numpy import *

window_size=5

def corrupt(pkt):
    rand = random.randint(1, 20)
    if rand >= 1 and rand <= 3:
        print "bit error"
    	index = random.randint(0, len(pkt)-1)
    	pkt = pkt[:index] + str(unichr(random.randint(0, 95))) + pkt[index+1:]
    	return pkt
    else:
	return pkt
'''
def delay():
    rand = random.randint(1, 20)
    if rand >= 1 and rand <= 7:
    	print "transmission delay"
        time.sleep(1)
'''
     

def send(content, to):
    checksum = ip_checksum(content)
    sock.sendto(checksum + content, to)

if __name__ == "__main__":
    addr = argv[1]
    port = int(argv[2])
    together = (addr, port)
    
    sock = socket(AF_INET, SOCK_DGRAM)
    expected_seq=0
    sock.bind(together)
    num=0

    filename='file_received'+str(num)+'.py'
    fp=open(filename,'w')
    num=1
    while True:
        message, address = sock.recvfrom(1024)
	if message=='over':
		fp.close()
		filename='file_received'+str(num)+'.py'
		num=num+1
		expected_seq=0
    		fp=open(filename,'w')
		continue		
        checksum = message[:2]
        seq = message[2]
	seq1=int(seq)
	
        message=corrupt(message)
        content = message[3:]
        if (ip_checksum(content) == checksum and seq1==expected_seq):
                send("ACK" + seq, address)
		fp.write(content)
		expected_seq=(expected_seq+1)%5
        elif ip_checksum(content) == checksum:
		print "Out of order, discard!"
		
	else:
		print "package biterror"
		
           # negative_seq = str(1 - expecting_seq)
            #send("ACK" + negative_seq, address)
    fp.close()
    sock.close()
