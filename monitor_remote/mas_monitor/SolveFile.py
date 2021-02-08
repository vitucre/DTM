#该模块用来处理xml文件
import xml.etree.ElementTree as ET


#获取本地主机ip:port,返回格式为['ip',port]
def get_local_ip(conf_file):
    xmlObj = ET.parse(conf_file)
    tree = xmlObj.getroot()
    local_ip_port = []
    for x in tree.findall('local_host'):
        local_ip_port.append(x.text.split(':')[0])
        local_ip_port.append(int(x.text.split(':')[1]))
    return local_ip_port


#从xml文件获取被监控主机ip:port，返回格式形如([127.0.0.1,9999],[192.168.6.112,10000])
def get_remote_ip(conf_file):
    xmlObj = ET.parse(conf_file)
    tree = xmlObj.getroot()
    monitor_ip_port = []
    for x in tree.iter('ip_port'):
        tmp = []
        tmp.append(x.text.split(':')[0])
        tmp.append(int(x.text.split(':')[1]))
        monitor_ip_port.append(tmp)
    return monitor_ip_port


#从xml文件获取文件信息，返回格式形如[[[127.0.0.1,9999,3600],[监控pid1,监控pid2,...]],[[192.168.6.112,10000,3600],[监控pid1,监控pid2,...]]]
def get_remote_files(conf_file):
    xmlObj = ET.parse(conf_file)
    tree = xmlObj.getroot()
    monitor_ip_dir = []
    for x in tree.findall('remote_host'):
        tmp1 = []
        tmp2 = []
        tmp = []
        for y in x.findall('ip_port'):
            tmp1.append(y.text.split(':')[0])
            tmp1.append(int(y.text.split(':')[1]))
        for i in x.findall('detect_interval_time'):
            if i.text is None:
                i.text = 3600
                tmp1.append(i.text)
            else:
                tmp1.append(int(i.text))
        for j in x.findall('monitor_pid'):
            for z in j.text.split(','):
                tmp2.append(int(z))
        tmp.append(tmp1)
        tmp.append(tmp2)
        monitor_ip_dir.append(tmp)
    return monitor_ip_dir
