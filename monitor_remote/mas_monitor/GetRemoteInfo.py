# 此模块用来获取被监控主机信息
import socket
import json


# 获取可用状态值
def get_situation():
    situation = [
        'get_process', 'get_platform', 'get_openfiles', 'get_memory', 'get_cpu'
    ]
    return situation


# 获取被监控主机的状态信息
# 返回信息转列表类型
def get_remote_situation_list(remote_ip, remote_port, message):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((remote_ip, remote_port))
    clientsocket.send(message.encode('utf-8'))
    result_message_json = json.loads(
        clientsocket.recv(2048000).decode('utf-8'))
    return result_message_json


# 返回信息为字符串类型
def get_remote_situation_str(remote_ip, remote_port, message):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((remote_ip, remote_port))
    clientsocket.send(message.encode('utf-8'))
    result_message_str = clientsocket.recv(2048000).decode('utf-8')
    return result_message_str


# 判断被监控主机操作系统类型
def judge_remote_platform(remote_ip, remote_port):
    remote_situation_platform = get_remote_situation_str(
        remote_ip, remote_port, 'get_platform')
    if 'linux' in remote_situation_platform:
        remote_platform = 'linux'
    elif 'win' in remote_situation_platform:
        remote_platform = 'windows'
    return remote_platform
