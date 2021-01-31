import FormatPrint
import sys
import SolveFile
import threading
import telnetlib


def run(remote_ip, remote_port, situation_value):
    #探测端口是否连通
    try:
        telnetlib.Telnet(remote_ip, remote_port)
    except ConnectionRefusedError:
        print('cant connect to {}:{}'.format(remote_ip, remote_port))
        return
    else:
        print(
            '--------------------------------{}:{}--------------------------------'
            .format(remote_ip, remote_port))
        #获取并输出对端主机状态信息
        FormatPrint.do_situation_value(situation_value, remote_ip, remote_port)


if __name__ == '__main__':
    situation_value = sys.argv[1]
    remote_ip_port = SolveFile.get_info_from_xml()
    for x in remote_ip_port:
        threading.Thread(target=run,
                         args=(x[0], x[1], situation_value)).start()
