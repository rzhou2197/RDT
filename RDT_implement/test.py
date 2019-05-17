from sys import argv, stdout
from checksum import ip_checksum
import time
from numpy import *

def corrupt(pkt):
    rand = random.randint(1, 20)
    if rand >= 1 and rand <= 5:
    	index = random.randint(0, len(pkt)-1)
    	pkt = pkt[:index] + str(unichr(random.randint(0, 95))) + pkt[index+1:]
    	return pkt
    else:
	return pkt

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

    filename='file_received'+str(num)+'.txt'
    fp=open(filename,'w')
    num=1
    while True:
	
        message, address = sock.recvfrom(1024)
	
        if message=='over':
		fp.close()
		filename='file_received'+str(num)+'.txt'
		num=num+1
    		fp=open(filename,'w')
		continue		
        checksum = message[:2]
