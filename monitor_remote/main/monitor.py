import sys
import threading
import telnetlib
sys.path.append('{}/..'.format(sys.path[0]))
from mas_monitor import SolveFile
from mas_monitor import FormatPrint


def run(remote_ip, remote_port, situation_value):
    #探测端口是否连通
    try:
        telnetlib.Telnet(remote_ip, remote_port, 5)
    except:
        print('cant connect to {}:{}'.format(remote_ip, remote_port))
        return
    else:
        #获取并输出被监控主机状态信息
        FormatPrint.do_situation_value(situation_value, remote_ip, remote_port)


if __name__ == '__main__':
    situation_value = sys.argv[1]
    monitor_ip_port = SolveFile.get_remote_ip('{}/../conf/monitor.xml'.format(
        sys.path[0]))
    for x in monitor_ip_port:
        threading.Thread(target=run,
                         args=(x[0], x[1], situation_value)).start()
