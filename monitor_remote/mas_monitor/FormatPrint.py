# 此模块用来输出格式化信息
from mas_monitor import GetRemoteInfo
from mas_monitor import RemoteInfoSolve


def do_situation_value(situation_value, remote_ip, remote_port):
    if situation_value == 'get_situation':
        print(GetRemoteInfo.get_situation())
    else:
        # 获取被监控主机操作系统信息
        remote_platform = GetRemoteInfo.judge_remote_platform(
            remote_ip, remote_port)
        # 获取将要返回被监控主机信息类型
        remote_info_type = RemoteInfoSolve.judge_remote_info_type(
            situation_value)
        # 调用列表方法获取被监控主机信息
        if remote_info_type == 'list_info':
            remote_situation_result = GetRemoteInfo.get_remote_situation_list(
                remote_ip, remote_port, situation_value)
        # 调用字符串方法获取被监控主机信息
        elif remote_info_type == 'str_info':
            remote_situation_result = GetRemoteInfo.get_remote_situation_str(
                remote_ip, remote_port, situation_value)
        elif remote_info_type == 'notExist':
            raise Exception('please input right situation value')

        # 输出格式化信息
        print(
            '--------------------------------{}:{}--------------------------------'
            .format(remote_ip, remote_port))
        if situation_value == 'get_openfiles':
            openfiles_info_solve_str = RemoteInfoSolve.openfiles_info_solve(
                remote_situation_result, remote_platform)
            print(openfiles_info_solve_str)
        if situation_value == 'get_platform':
            print(remote_situation_result)
        if situation_value == 'get_process':
            process_info_solve_str = RemoteInfoSolve.process_info_solve(
                remote_situation_result)
            print(process_info_solve_str)
        if situation_value == 'get_memory':
            memory_info_solve_str = RemoteInfoSolve.mem_info_solve(
                remote_situation_result, remote_platform)
            print(memory_info_solve_str)
        if situation_value == 'get_cpu':
            cpu_info_solve_str = RemoteInfoSolve.cpu_info_solve(
                remote_situation_result, remote_platform)
            print(cpu_info_solve_str)
