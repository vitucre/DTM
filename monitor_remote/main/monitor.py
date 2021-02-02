import sys
import threading
import telnetlib
sys.path.append('{}/..'.format(sys.path[0]))
sys.path.append('{}/../mas_monitor'.format(sys.path[0]))
from mas_monitor import FormatPrint
from mas_monitor import SolveFile


def run(remote_ip, remote_port, situation_value):
    #探测端口是否连通
    try:
        telnetlib.Telnet(remote_ip, remote_port, 5)
    except:
        print('cant connect to {}:{}'.format(remote_ip, remote_port))
        return
    else:
        print(
            '--------------------------------{}:{}--------------------------------'
            .format(remote_ip, remote_port))
        #获取并输出对端主机状态信息
        FormatPrint.do_situation_value(situation_value, remote_ip, remote_port)


if __name__ == '__main__':
    # situation_value = sys.argv[1]
    situation_value = 'get_situation'
    remote_ip_port = SolveFile.get_info_from_xml(
        '{}/../conf/monitor.xml'.format(sys.path[0]))
    for x in remote_ip_port:
        threading.Thread(target=run,
                         args=(x[0], x[1], situation_value)).start()
