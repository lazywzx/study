class Client:
    def __init__(self, IP, port=9999):
        self.serverIP = IP;
        self.port = 9999;
        self.isconnect = False;
        self.message = [];
        self.STRING_SENDIMAGE = "**transport png**"
        
        
    def connectServer(self):
        import _thread
        from socket import socket, AF_INET, SOCK_STREAM
        self.client = socket(AF_INET, SOCK_STREAM)
        try:
            self.client.connect((self.serverIP, self.port))
            self.isconnect = True
            _thread.start_new_thread(self.readMessage, (None,))
            
            
            self.server = socket()
            self.server.bind((self.client.getsockname()[0], 9898))
            self.server.listen(1)
        except Exception as e:
            self.isconnect = False
            #             当连接错误时，可以在这里修改你想输出的信息
            print('连接错误')
            print(e)

    #     这个函数是开发人员使用的
    def getClient(self):
        return self.client

    #     目前只支持整型，浮点和字符串
    def send(self, msg):
        if self.isconnect == False:
            print('请先连接服务器')
            return
        if isinstance(msg, int):
            msg = str(msg)
        elif isinstance(msg, float):
            msg = str(msg)
        elif isinstance(msg, str):
            pass
        else:
            print('不支持该类型字符')
            return;
        msg = msg + '+'
        self.client.send(msg.encode())

    def readMessage(self, mm):
        import _thread
        try:
            msg = self.client.recv(2048).decode()
            if msg == '':
                self.isconnect = False
                print('与服务器失去连接')
                msg = None
            else:
                _thread.start_new_thread(self.readMessage, (None,))
            #                 print('读取成功')
                self.message.append(msg)
        except Exception as e:
            self.isconnect = False
            print(e)

    def read(self):
        if self.isconnect == False:
            print('请先连接服务器')
            return
        if len(self.message) == 0:
            return None
        return self.message.pop(0)

    def isConnected(self):
        return self.isconnect

    def close(self):
        self.client.close()

    def sendImage(self, path):
        import socket
        import os
        import time
       # server = socket.socket()
        #server.bind((self.client.getsockname()[0], 9898))
       # server.listen(1)
        # 设置accept的超时时间
        self.server.settimeout(5)
        self.send(self.STRING_SENDIMAGE)
        try:
            conn, adrr = self.server.accept()
            file_size = os.stat(path).st_size
            f = open(path, 'rb')
            has_sent = 0
            while has_sent != file_size:
                data = f.read(1024)
                conn.sendall(data)  # 发送真实数据
                has_sent += len(data)
            f.close()
            conn.close()
            print('上传成功')
        except Exception as e:
            print('上传失败')
        finally:
            #server.close()
            print('关闭成功')
    def clearMessage(self):
        self.message = []
