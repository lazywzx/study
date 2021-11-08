from socket import *
from time import ctime

host = ''

port = 33333
buffsize = 1024
ADDR = (host,port)

tctime = socket(AF_INET,SOCK_STREAM)
tctime.bind(ADDR)
tctime.listen(3)

while True:
    print('Wait for connection ...')
    tctimeClient,addr = tctime.accept()
    print("Connection from :",addr)

    while True:
        data = tctimeClient.recv(buffsize)
        print(data)
        if not data:
            break
        tctimeClient.send(('[%s] %s' % (ctime(),data)).encode())
    tctimeClient.close()
tctimeClient.close()
