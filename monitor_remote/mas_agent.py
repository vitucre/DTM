import socket
import psutil
import json
import sys


#监听并返回相关信息
def put_info(local_ip, local_prot):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((local_ip, local_prot))
    serversocket.listen(5)
    while True:
        s, addr = serversocket.accept()
        message = s.recv(1024).decode('utf-8')
        #返回操作系统信息
        if message == 'get_platform':
            s.send(sys.platform.encode('utf-8'))
        #返回打开文件信息
        if message == 'get_openfiles':
            openfiles_info = [
                p.info for p in psutil.process_iter(['pid', 'open_files'])
            ]
            openfiles_info_json = json.dumps(openfiles_info)
            s.send(openfiles_info_json.encode('utf-8'))
        #返回进程信息
        if message == 'get_process':
            process_info = [
                p.info
                for p in psutil.process_iter(['pid', 'username', 'name'])
            ]
            process_info_json = json.dumps(process_info)
            s.send(process_info_json.encode('utf-8'))
        #返回内存信息
        if message == 'get_memory':
            mem_list = [[], []]
            for x in psutil.virtual_memory():
                mem_list[0].append(x)
            for y in psutil.swap_memory():
                mem_list[1].append(y)
            mem_json = json.dumps(mem_list)
            s.send(mem_json.encode('utf-8'))
        #返回cpu信息
        if message == 'get_cpu':
            cpu_list = [[], [], []]
            for x in psutil.cpu_times_percent(interval=1, percpu=False):
                cpu_list[0].append(x)
            cpu_list[1].append(psutil.cpu_count(logical=True))
            for y in psutil.getloadavg():
                cpu_list[2].append(y)
            cpu_json = json.dumps(cpu_list)
            s.send(cpu_json.encode('utf-8'))


if __name__ == '__main__':
    local_ip = '127.0.0.1'
    local_port = 11111
    #开启监听
    put_info(local_ip, local_port)
