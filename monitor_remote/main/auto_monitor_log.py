import socket
import sys
import os
import json
sys.path.append('{}/..'.format(sys.path[0]))
from mas_monitor import SolveFile

if __name__ == '__main__':
    #从xml中获取本地绑定的ip:port,返回格式为['ip',port]
    local_ip_port = SolveFile.get_local_ip('{}/../conf/monitor.xml'.format(
        sys.path[0]))
    host = local_ip_port[0]
    port = local_ip_port[1]
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((host, port))
    serversocket.listen(20)
    while True:
        s, addr = serversocket.accept()
        #获取被监控主机传来的数据，格式为[['内容'],['日志别名']]
        data = s.recv(512000)
        data_list = json.loads(data.decode('utf-8'))
        content = data_list[0]
        aliasname = data_list[1]
        #创建logs目录下对应的被监控主机目录
        if not os.access('{}/../logs/{}'.format(sys.path[0], addr[0]),
                         os.F_OK):
            os.mkdir('{}/../logs/{}'.format(sys.path[0], addr[0]))
        #将被监控文件数据写入到本地日志中最后一行
        with open('{}/../logs/{}/{}'.format(sys.path[0], addr[0], aliasname),
                  'a',
                  encoding='utf-8') as f:
            f.write(content)
