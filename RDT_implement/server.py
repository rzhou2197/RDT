from socket import socket, AF_INET, SOCK_DGRAM
from sys import argv, stdout
from checksum import ip_checksum
import time
from numpy import *

def corrupt(pkt):
    rand = random.randint(1, 20)
    if rand >= 1 and rand <= 5:
        print "bit error"
    	index = random.randint(0, len(pkt)-1)
    	pkt = pkt[:index] + str(unichr(random.randint(0, 95))) + pkt[index+1:]
    	return pkt
    else:
	return pkt
'''

def delay():
    rand = random.randint(1, 20)
    if rand >= 1 and rand <= 3:
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
    
    sock.bind(together)
    num=0

    filename='file_received'+str(num)+'.py'
    fp=open(filename,'w')
    num=1
    expecting_seq = 0
    
    while True:
        message, address = sock.recvfrom(1024)
	if message=='over':
		fp.close()
		filename='file_received'+str(num)+'.py'
		expecting_seq=0
		num=num+1
    		fp=open(filename,'w')
		continue		
        #delay()
        checksum = message[:2]
        seq = message[2]
        message=corrupt(message)
        content = message[3:]
        if ip_checksum(content) == checksum:
            if seq == str(expecting_seq):
		print "package",seq, "received successfully"
                send("ACK" + seq, address)
		fp.write(content)
                expecting_seq = 1 - expecting_seq
        else:
            negative_seq = str(1 - expecting_seq)
	    print "package",seq,"receive failed"
            send("ACK" + negative_seq, address)
    fp.close()
    sock.close()
