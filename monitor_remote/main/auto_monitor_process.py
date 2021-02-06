#监控文件与获取到的信息进行对比，如果匹配，则存在，如果不匹配，则不存在进程
import sys
import threading
import time
import telnetlib
sys.path.append('{}/..'.format(sys.path[0]))
from mas_monitor import SolveFile
from mas_monitor import GetRemoteInfo
from mas_monitor import RemoteInfoSolve


#此线程用于判断被监控文件是否被对端主机进程占用
#monitor_ip_file形如[[127.0.0.1,9999,3600],[监控pid1,监控pid2,...]]
def run(monitor_ip_file):
    while True:
        #探测对端主机端口
        try:
            telnetlib.Telnet(monitor_ip_file[0][0], monitor_ip_file[0][1], 5)
        except:
            print('cant connect to {}:{}'.format(monitor_ip_file[0][0],
                                                 monitor_ip_file[0][1]))
        else:
            #定时获取对端主机openfile信息
            #日志名称
            logname = '{}_{}_{}.log'.format(
                monitor_ip_file[0][0], monitor_ip_file[0][1],
                time.strftime('%y%m%d', time.localtime(time.time())))
            #控制循环次数
            times = 0
            for y in monitor_ip_file:
                if times == 0:
                    remote_situation_result = GetRemoteInfo.get_remote_situation_list(
                        y[0], y[1], 'get_process')
                    remote_pid = []
                    for z in remote_situation_result:
                        remote_pid.append(z['pid'])
                elif times == 1:
                    #判断被监控文件是否被对端主机进程占用并将结果写入日志文件
                    with open('{}/../logs/{}'.format(sys.path[0], logname),
                              'a',
                              encoding='utf-8') as f:
                        for z in y:
                            if z not in remote_pid:
                                f.write(
                                    '{}\tpid:{}\t is lost detected\n'.format(
                                        time.asctime(
                                            time.localtime(time.time())), z))
                            elif z in remote_pid:
                                f.write(
                                    '{}\tpid:{}\t is detected successfully\n'.
                                    format(
                                        time.asctime(
                                            time.localtime(time.time())), z))
                times += 1
        #间隔探测对端主机
        time.sleep(monitor_ip_file[0][2])


if __name__ == '__main__':
    #从xml处获取需要监控的文件,形如[[[127.0.0.1,9999,3600],[监控pid1,监控pid2,...]],[[192.168.6.112,10000,3600],[监控pid1,监控pid2,...]]]
    monitor_obj = SolveFile.get_file_from_xml('{}/../conf/monitor.xml'.format(
        sys.path[0]))
    for x in monitor_obj:
        threading.Thread(target=run, args=(x, )).start()
