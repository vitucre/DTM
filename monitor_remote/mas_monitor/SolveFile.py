#该模块用来处理文件
import xml.etree.ElementTree as ET
import sys
import time


#从xml文件获取配置
def get_info_from_xml():
    xmlObj = ET.parse('{}/monitor.xml'.format(sys.path[0]))
    tree = xmlObj.getroot()
    for x in tree.findall('ip_port'):
        ip_port_from_xml = x.text
    remote_ip_port = []
    #拆解后形如['192.168.6.1:9999', '127.0.0.1:9999']
    for y in ip_port_from_xml.split(','):
        #拆解后形如['192.168.6.1','9999']
        tmp_list = y.split(':')
        tmp_list.append(int(tmp_list.pop(1)))
        remote_ip_port.append(tmp_list)
    return remote_ip_port


#生成器，每次迭代获取文件的最后一行，用于监控日志
def tail_file(myfile):
    with open(myfile, 'r', encoding='utf-8') as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if line:
                yield line
            else:
                time.sleep(1)
