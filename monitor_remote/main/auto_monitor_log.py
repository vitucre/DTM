import socket
import sys
import os

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 9998
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serversocket.bind((host, port))
    while True:
        content, addr = serversocket.recvfrom(204800)
        logname = content.decode('utf-8').split('@@@@@@@@@@')[1]
        #创建logs目录下对应的对端主机目录
        if not os.access('{}/../logs/{}'.format(sys.path[0], addr[0]),
                         os.F_OK):
            os.mkdir('{}/../logs/{}'.format(sys.path[0], addr[0]))
        #将监控文件数据写入到本地日志中最后一行
        with open('{}/../logs/{}/{}'.format(sys.path[0], addr[0], logname),
                  'a',
                  encoding='utf-8') as f:
            f.write(content.decode('utf-8').split('@@@@@@@@@@')[0])
