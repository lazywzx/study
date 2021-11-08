#!/usr/bin/python3
import paramiko


class SSHConnection(object):

    def __init__(self, host='服务器公网IP', port=22, username='用户名', pwd='用户密码'):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.__k = None

    def connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.pwd)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def upload(self, local_path, target_path):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.put(local_path, target_path)

    def download(self, remote_path, local_path):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.get(remote_path, local_path)

    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        result = str(stdout.read(), encoding='utf-8')
        return result

"""
ssh = SSHConnection()
# 登录
ssh.connect()
# 上传
ssh.upload('./capture.png', '/root/IoT/capture.png')
# 服务器执行命令并返回结果
# print(ssh.cmd("ls"))
if ssh.cmd("ls /root/IoT/result.txt") != '':
    print("exist")
    # 下载
    ssh.download('/root/IoT/result.txt', './result.txt')
else:
    print("not exist")
# 关闭连接
ssh.close()
"""