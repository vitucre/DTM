import socket
import time
import json
import sys
import threading
import xml.etree.ElementTree as ET


#生成器，每次迭代获取文件的最后一行，用于监控日志
def tail_file(myfile, scan_file_time):
    with open(myfile, 'r', encoding='utf-8') as f:
        f.seek(0, 2)
        while True:
            content = f.read(1472)
            if content:
                yield content
            time.sleep(scan_file_time)


#从xml中获取数据，并返回格式[['127.0.0.1',9998,60],[['监控文件1','别名'],['监控文件2','别名']...]]
def get_info_from_xml(xmlFile):
    xmlObj = ET.parse(xmlFile)
    tree = xmlObj.getroot()
    xml_list = []
    tmp = []
    for x in tree.findall('monitor_host'):
        tmp.append(x.text.split(':')[0])
        tmp.append(int(x.text.split(':')[1]))
    for y in tree.findall('scan_file_time'):
        if y.text is None:
            y.text = 3
            tmp.append(y.text)
        else:
            tmp.append(int(y.text))
        xml_list.append(tmp)
        del tmp
    for z in tree.findall('monitor_files'):
        tmp1 = []
        for n in z.findall('file_alias'):
            tmp1.append(n.text.split(','))
        xml_list.append(tmp1)
        del tmp1
    return xml_list


#调用线程监控不同日志，并发送给监控端主机
def run(host, port, scan_file_time, monitor_file, aliasname):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #监控指定文件
    t = tail_file(monitor_file, scan_file_time)
    while True:
        content = []
        content.append(next(t))
        content.append(aliasname)
        clientsocket.sendto(json.dumps(content).encode('utf-8'), (host, port))


if __name__ == '__main__':
    #从xml中获取配置格式为[['127.0.0.1',9998,60],[['监控文件1','别名'],['监控文件2','别名']...]]
    xml_list = get_info_from_xml('{}/agent.xml'.format(sys.path[0]))
    host = xml_list[0][0]
    port = xml_list[0][1]
    scan_file_time = xml_list[0][2]
    #控制循环次数
    times = 0
    for x in xml_list:
        if times == 0:
            times += 1
            continue
        else:
            for y in x:
                monitor_file = y[0]
                aliasname = y[1]
                thread = threading.Thread(target=run,
                                          args=(host, port, scan_file_time,
                                                monitor_file,
                                                aliasname)).start()
