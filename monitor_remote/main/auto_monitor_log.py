import socket
import sys
import os
import json

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 9998
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((host, port))
    serversocket.listen(20)
    while True:
        s, addr = serversocket.accept()
        #获取监控主机传来的数据，格式为[['内容'],['日志别名']]
        data = s.recv(204800)
        data_list = json.loads(data.decode('utf-8'))
        content = data_list[0]
        aliasname = data_list[1]
        #创建logs目录下对应的对端主机目录
        if not os.access('{}/../logs/{}'.format(sys.path[0], addr[0]),
                         os.F_OK):
            os.mkdir('{}/../logs/{}'.format(sys.path[0], addr[0]))
        #将监控文件数据写入到本地日志中最后一行
        with open('{}/../logs/{}/{}'.format(sys.path[0], addr[0], aliasname),
                  'a',
                  encoding='utf-8') as f:
            f.write(content)
