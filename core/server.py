"""核心代码"""
from conf import settings
import paramiko
import threading
import os
from core import logger



log_type = "system"  # 系统日志记录到文件中
system_logger = logger.logger(log_type)

class REMOTE_HOST(object):
    #远程操作主机
    def __init__(self, host, port ,username, password, cmd):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.cmd = cmd

    def run(self):
        """起线程连接远程主机后调用"""
        # cmd_str 这个是执行的命令
        cmd_str = self.cmd.split()[0]
        #
        if hasattr(self, cmd_str):      #反射 eg:调用put方法
            # 如果这个命令在类方法中就可以被调用
            getattr(self, cmd_str)() # 直接执行类方法

            # 如果不在类方法中
        else:
            #setattr(x,'y',v)is  equivalent  to   ``x.y=v''
            setattr(self, cmd_str, self.command)  # 替换为 command的方法
            getattr(self, cmd_str)()  #调用command方法，执行批量命令处理

    def log(self,host,cmd):
        '''添加log 功能'''
        system_logger.info("Account {%s} sign in cmd %s"%(host,cmd))

    def command(self):
        """批量命令处理"""
        ssh = paramiko.SSHClient()  #创建ssh对象
        #允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.host,port=self.port,username=self.username,password=self.password)
        stdin,stdout,stderr = ssh.exec_command(self.cmd)
        #result = stdout.read()
        res, err = stdout.read(), stderr.read()
        result = res if res else err
        if result:
            self.log(self.host,self.cmd)
        #
        print("%s".center(50, "-") % self.host)
        # 打印出正常的执行结果
        print(result.decode())

        ssh.close()

    def put(self):
        """上传文件"""
        filename = self.cmd.split()[1]  #要上传的文件
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(filename, filename)
        self.log(self.host,self.cmd)
        print("put sucesss")

        transport.close()
    def help(self):
        '''帮助'''
        msg='''
        ################
        1. 如果需要退出就exit 退出
        2. 你上传的家目录只能在你的用户家目录下
        '''
        print(msg)
def show_host_list():
    """通过选择分组显示主机名与IP"""
    # 通过 index 和key 的方式显示
    for index, key in enumerate(settings.msg_dic):
        # 显示 用户组信息
        print(index + 1, key, len(settings.msg_dic[key]))

    while True:
        choose_host_list = input(">>>(eg:group1)").strip()

        # 获取到组的信息
        host_dic = settings.msg_dic.get(choose_host_list)
        # 如果有信息
        if host_dic:
            #print(host_dic)
            for key in host_dic:
                # 打印出IP地址
                print(key, host_dic[key]["IP"])
            # 返回IP地址
            return host_dic
        else:
            print("NO exit this group!")


def interactive(choose_host_list):
    """根据选择的分组主机起多个线程进行批量交互"""
    thread_list = []
    while True:
        cmd = input(">>>").strip()

        if cmd=='exit':
            exit("good bye")
        elif cmd:
            for key in choose_host_list:
                host, port, username, password = choose_host_list[key]["IP"], choose_host_list[key]["port"], \
                                                 choose_host_list[key]["username"], choose_host_list[key]["password"]
                func = REMOTE_HOST(host, port, username, password, cmd)  # 实例化类
                t = threading.Thread(target=func.run)  # 起线程
                t.start()
                thread_list.append(t)
            for t in thread_list:
                t.join()  # 主线程等待子线程执行完毕

        else:
            continue


def run():
    choose_host_list = show_host_list()
    interactive(choose_host_list)