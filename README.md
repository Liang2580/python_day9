简单的一个批量分发的一个python3 开发的一个小工具
settings 是配置文件所在的地方。
服务器的IP 和 用户名 密码存放的位置

可以执行linux的命令。也可以使用帮助

使用的方式如下：
#python36 bin/main.py
1 group1 2
2 group2 3

##(eg:group1)group1
h1 192.168.57.128
h2 192.168.57.129
ls
------------------------192.168.57.129------------------------
aa
anaconda-ks.cfg
__init__.py
ls
Python-3.6.0
Python-3.6.0.tgz

------------------------192.168.57.128------------------------
aa
anaconda-ks.cfg
__init__.py
ls

cat aa

上传 :
put cc /root
put sucesss
put sucesss
>>>


查看日志

2018-02-24 16:05:19,302 - system - INFO - Account {192.168.57.129} sign in cmd ls
2018-02-24 16:05:19,554 - system - INFO - Account {192.168.57.128} sign in cmd ls
2018-02-24 16:08:01,732 - system - INFO - Account {192.168.57.129} sign in cmd ls
2018-02-24 16:08:01,857 - system - INFO - Account {192.168.57.128} sign in cmd ls
2018-02-24 16:08:05,455 - system - INFO - Account {192.168.57.129} sign in cmd cat aa
2018-02-24 16:08:05,588 - system - INFO - Account {192.168.57.128} sign in cmd cat aa
2018-02-24 16:08:39,484 - system - INFO - Account {192.168.57.129} sign in cmd put cc /root
2018-02-24 16:08:39,641 - system - INFO - Account {192.168.57.128} sign in cmd put cc /root

