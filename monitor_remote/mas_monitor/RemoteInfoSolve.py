#此模块用来解析处理被监控主机信息


#判断将要返回被监控主机信息类型
def judge_remote_info_type(situation_value):
    list_info = ['get_process', 'get_openfiles', 'get_memory', 'get_cpu']
    str_info = ['get_platform']
    if situation_value in list_info:
        return 'list_info'
    elif situation_value in str_info:
        return 'str_info'
    else:
        return 'notExist'


#打开文件信息格式化处理
def openfiles_info_solve(remote_situation_result, remote_platform):
    openfiles_info_solve_str = 'pid\topen_files\n'
    for x in remote_situation_result:
        if remote_platform == 'linux':
            if len(x['open_files']) != 0:
                for y in x['open_files']:
                    openfiles_info_solve_str += '{}\t{}\n'.format(
                        x['pid'], y[0])
        elif remote_platform == 'windows':
            if x['open_files'] is not None:
                for y in x['open_files']:
                    openfiles_info_solve_str += '{}\t{}\n'.format(
                        x['pid'], y[0])
    return openfiles_info_solve_str


#进程信息格式化处理
def process_info_solve(remote_situation_result):
    process_info_solve_str = 'pid\tusername\tname\n'
    for x in remote_situation_result:
        process_info_solve_str += '{}\t{}\t{}\n'.format(
            x['pid'], x['username'], x['name'])
    return process_info_solve_str


#cpu信息格式化处理
def cpu_info_solve(remote_situation_result, remote_platform):
    if remote_platform == 'linux':
        cpu_info_solve_str = 'user\tnice\tsystem\tiowait\tsteal\tidle\n'
        #控制循环次数
        times = 0
        for x in remote_situation_result:
            if times == 0:
                user = x[0]
                nice = x[1]
                system = x[2]
                iowait = x[4]
                steal = x[7]
                idle = x[3]
                cpu_info_solve_str += '{}%\t{}%\t{}%\t{}%\t{}%\t{}%\n'.format(
                    user, nice, system, iowait, steal, idle)
                times += 1
                continue
            elif times == 1:
                cpu_info_solve_str += 'logicalCPU count:{}\n'.format(x[0])
                times += 1
                continue
            elif times == 2:
                cpu_info_solve_str += 'load average:{},{},{}\n'.format(
                    x[0], x[1], x[2])
                break
    elif remote_platform == 'windows':
        cpu_info_solve_str = 'user\tnice\tsystem\tiowait\tsteal\tidle\n'
        times = 0
        for x in remote_situation_result:
            if times == 0:
                user = x[0]
                system = x[1]
                idle = x[2]
                cpu_info_solve_str += '{}%\t\t{}%\t\t\t{}%\n'.format(
                    user, system, idle)
                times += 1
                continue
            elif times == 1:
                cpu_info_solve_str += 'logicalCPU count:{}\n'.format(x[0])
                break
    return cpu_info_solve_str


#内存信息格式化处理
def mem_info_solve(remote_situation_result, remote_platform):
    if remote_platform == 'linux':
        mem_info_solve_str = '\ttotal\tused\tfree\tshared\tbuff/cache\tavailable\tprecent\n'
        #控制循环次数
        times = 0
        for x in remote_situation_result:
            if times == 0:
                mem_total = x[0] // 1024 // 1024
                mem_used = x[3] // 1024 // 1024
                mem_free = x[4] // 1024 // 1024
                mem_shared = x[9] // 1024 // 1024
                mem_buff_cache = (x[7] + x[8]) // 1024 // 1024
                mem_available = x[1] // 1024 // 1024
                mem_precent = x[2]
                mem_info_solve_str += 'Mem:\t{}M\t{}M\t{}M\t{}M\t{}M\t\t{}M\t\t{}%\n'.format(
                    mem_total, mem_used, mem_free, mem_shared, mem_buff_cache,
                    mem_available, mem_precent)
                times += 1
                continue
            elif times == 1:
                swap_total = x[0] // 1024 // 1024
                swap_used = x[1] // 1024 // 1024
                swap_free = x[2] // 1024 // 1024
                swap_precent = x[3]
                mem_info_solve_str += 'Swap:\t{}M\t{}M\t{}M\t\t\t\t\t\t{}%\n'.format(
                    swap_total, swap_used, swap_free, swap_precent)
                break
    elif remote_platform == 'windows':
        mem_info_solve_str = '\ttotal\tused\tfree\tavailable\tprecent\n'
        #控制循环次数
        times = 0
        for x in remote_situation_result:
            if times == 0:
                mem_total = x[0] // 1024 // 1024
                mem_used = x[3] // 1024 // 1024
                mem_free = x[4] // 1024 // 1024
                mem_available = x[1] // 1024 // 1024
                mem_precent = x[2]
                mem_info_solve_str += 'Mem:\t{}M\t{}M\t{}M\t{}M\t\t{}%\n'.format(
                    mem_total, mem_used, mem_free, mem_available, mem_precent)
                times += 1
                continue
            elif times == 1:
                swap_total = x[0] // 1024 // 1024
                swap_used = x[1] // 1024 // 1024
                swap_free = x[2] // 1024 // 1024
                swap_precent = x[3]
                mem_info_solve_str += 'Swap:\t{}M\t{}M\t{}M\t\t\t{}%\n'.format(
                    swap_total, swap_used, swap_free, swap_precent)
                break
    return mem_info_solve_str
