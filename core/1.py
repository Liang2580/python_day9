#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: liang 
import  configparser
import  paramiko
import time
import os
import optparse
from multiprocessing import Process, Lock

class Tools(object):
  def __init__(self):
      parser = optparse.OptionParser()
      parser.add_option("-H", "--H", dest="high", help="high")
      parser.add_option("-g", "--g", dest="g", help="g")
      parser.add_option("--cmd", "--cmd", dest="cmd", help="cmd")
      self.options, self.args = parser.parse_args()
      self._data(self._file(self.options,self.args))
  def _file(self,options,args):
      """判断属性是否为空，取出H和g"""
      file_list = []
      file_list1=[]
      if args and args[0] == "batch_run":
          if options.high is not None or options.g is not None or options.cmd is not None:
              config = configparser.ConfigParser()
              config.read("accounts.cfg")
              g = options.g.split(",")
              h = options.high.split(",")
              for i in g:
                if i not in config.options("server-g"):
                  print("找不到%s信息组"%i)
                  g.remove(i)
              for i in h:
                 file_list.append(i)
              for i in g:
                s = config["server-g"][i]
                s = s.split(",")
                file_list = file_list +s
              ret1 = config.sections()
              del ret1[0]
              for i in file_list:
                if i in ret1:
                  file_list1.append(i)
                else:
                  print("找不到主机名%s" %i)
                  continue
              return file_list1
      else:
        exit("请输入正确的参数")

  def _data(self,file_list):
      data_dic = {}
      config = configparser.ConfigParser()
      config.read("accounts.cfg")
      for i in file_list:
        data_dic[i] = {
          "server": config[i]["server"],
          "port": config[i]["port"],
          "username": config[i]["username"],
          "password": config[i]["password"]
        }
      lock = Lock()
      for i in data_dic:
          Process(target=self._ssh, args=(lock,data_dic[i])).start()

  def _ssh(self,l,data_dic):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        l.acquire()
        print("---------%s----------" %data_dic["server"])
        ssh.connect(data_dic["server"], int(data_dic["port"]),data_dic["username"], data_dic["password"])
        stdin, stdout, stderr = ssh.exec_command(self.options.cmd)
        if stdout.read().decode():
            stdin, stdout, stderr = ssh.exec_command(self.options.cmd)
            print(stdout.read().decode())
        else:
            print (stderr.read().decode())
        l.release()
        #判断是否进程同步
        time.sleep(2)

if __name__ == "__main__":
  t =Tools()