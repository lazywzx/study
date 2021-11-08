from socket import *
from time import ctime
host = "lazywzx.info"
port = 33333
bufsize = 1024
addr = (host, port)
tcpClient = socket(AF_INET,SOCK_STREAM)
tcpClient.connect(addr)
while True:
    data = input(">")
    if not data:
        break
    sendData = bytes(data, encoding="utf8")
    tcpClient.send(sendData)
    data = tcpClient.recv(bufsize).decode()
    if not data:
        break
    print(data)
tcpClient.close()
