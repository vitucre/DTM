import socket
import sys
import time


#生成器，每次迭代获取文件的最后一行，用于监控日志
def tail_file(myfile):
    with open(myfile, 'r', encoding='utf-8') as f:
        f.seek(0, 2)
        while True:
            content = f.read()
            if content:
                yield content
            time.sleep(30)


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 9998
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #监控指定文件
    t = tail_file('{}/test.txt'.format(sys.path[0]))
    while True:
        content = next(t) + '@@@@@@@@@@{}'.format('test.txt')
        clientsocket.sendto(content.encode('utf-8'), (host, port))
