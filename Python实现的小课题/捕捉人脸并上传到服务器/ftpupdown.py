from FTPTest import SSHConnection


# 上传到服务器
ssh = SSHConnection()
ssh.connect()
reuslt = ssh.cmd('ls /')
ssh.upload('./capture.png', '/root/capture.png')
ssh.download('/root/file', './file')
print("All Done!")
