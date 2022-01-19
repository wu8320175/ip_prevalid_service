​
项目概述：防止外网的陌生ip进入服务器的指定端口，通过本web服务来配置允许进入端口的。  
Project Overview: Prevent unfamiliar IP of the external network from entering the specified port of the server, configuring the port through this web service.  
当然终极方法是：将你的SSH密码设置复杂点，避免泄露，Set your SSH password to set up complex points to avoid leakage
## 背景 background：

服务器使用frp后，被人下了挖矿病毒，痛定思痛决定给服务器加上二次验证，只允许指定ip来访问端口，避免不正常的ip来扫描我的端口。。。所以花了一天时间写个小验证程序  
After using FRP, the server was infected with a mining virus, so I decided to add secondary verification to the server, only allowing the specified IP address to access the port, so as to avoid scanning my port with abnormal IP addresses...So I spent the day writing a little validation program

## 实现的功能如下 functions：  

1. 指定的端口，首先所有ip都不能访问，然后根据web服务验证的结果允许该ip来访问指定端口。  
The specified port is first inaccessible to all IP addresses and then allowed to access the specified port based on the result of web service authentication.  

2.将以上功能封装成web服务，先在网页端通过 二级密码 来允许当前ip的访问服务器，当前ip才能访问目的ip和端口，比如ssh服务等。  
Encapsulate the above functions into web services. First, allow the current IP to access the server through the secondary password on the web page, and the current IP can access the destination IP and port, such as SSH service.  

![image](https://user-images.githubusercontent.com/24267883/149650892-36c95553-48d6-412d-bab6-9156c2816f19.png)

## 使用工具 tools：  

        Python，python-iptables库，flask （用于web服务）  

## 原因： python简单。。。。。，flask搭个服务更简单。    
Reason:Python is simple....., Flask takes a service easier    

### 首先库安装和使用  
First library installation and use  

## 特别说明： python 必须在sudo权限下或者root权限的用户下执行，才能使用python-iptables库  
Special note: Python must be executed under Sudo permission to use the Python-iptables library   
下载项目，然后flask_IP&port_valid_service目录下，修改config.json文件，配置密码和禁止的端口  
Download the project, then Flask_ip & port_valid_service directory, modify the config.json file, configure the password and the forbidden port    
注意：禁止端口不要加上flask启动的web端口  
Note: Forbidden ports Do not add Flask-started web port  
```
在ubuntu下：
sudo pip install --upgrade python-iptables  
sudo pip install flask

进入index.py的目录 Enter the directory of index.py  
cd  flask_IP&port_valid_service

启动： Run:
sudo python index.py

在centos下，可能先安装iptables

1. sudo yum install iptables-services

2. systemctl start iptables.service
● iptables.service - IPv4 firewall with iptables
   Loaded: loaded (/usr/lib/systemd/system/iptables.service; enabled; vendor preset: enabled)
   Active: active (exited) since Sun 2022-01-16 22:22:34 CST; 1s ago
  Process: 16982 ExecStart=/usr/libexec/iptables/iptables.init start (code=exited, status=0/SUCCESS)
 Main PID: 16982 (code=exited, status=0/SUCCESS)

Jan 16 22:22:34 iZ0jleum1rgkepql5fg95pZ systemd[1]: Starting IPv4 firewall with iptables...
Jan 16 22:22:34 iZ0jleum1rgkepql5fg95pZ iptables.init[16982]: iptables: Applying firewall rules: [  OK  ]
Jan 16 22:22:34 iZ0jleum1rgkepql5fg95pZ systemd[1]: Started IPv4 firewall with iptables.

3.run python
[root@iZ0j flask_IP&port_valid_service]# python index.py
Traceback (most recent call last):
  File "index.py", line 4, in <module>
    import iptables_op as op
  File "/root/flask_IP&port_valid_service/iptables_op.py", line 2, in <module>
    import iptc
  File "/usr/local/lib64/python3.6/site-packages/iptc/__init__.py", line 10, in <module>
    from iptc.ip4tc import (is_table_available, Table, Chain, Rule, Match, Target, Policy, IPTCError)
  File "/usr/local/lib64/python3.6/site-packages/iptc/ip4tc.py", line 13, in <module>
    from .xtables import (XT_INV_PROTO, NFPROTO_IPV4, XTablesError, xtables,
  File "/usr/local/lib64/python3.6/site-packages/iptc/xtables.py", line 825, in <module>
    raise XTablesError("can't find directory with extensions; "
## iptc.errors.XTablesError: can't find directory with extensions; please set XTABLES_LIBDIR

如果出现以上报错，解决方法（找到iptables的xtables文件夹位置，设置环境变量）：  
If there is an error, the solution (find the iptables xTables folder location, set the environment variable)  
1）：
rpm -qa|grep iptables

iptables-libs-1.8.4-17.1.al8.x86_64
iptables-1.8.4-17.1.al8.x86_64
iptables-ebtables-1.8.4-17.1.al8.x86_64
iptables-services-1.8.4-17.1.al8.x86_64

2）：
rpm -ql iptables-1.8.4-17.1.al8.x86_64
![image](https://user-images.githubusercontent.com/24267883/149664238-41837436-6a8a-4ce1-afbf-f6bd25d7580a.png)

3）：
export XTABLES_LIBDIR=/usr/lib64/xtables/
或者进入环境变量设置永久生效：  
Or enter the environment variable setting permanently effective:  

 vim ~/.bash_profile  
 在最后添加两行：  Add two lines at the end:  
 XTABLES_LIBDIR=/usr/lib64/xtables/  
 export XTABLES_LIBDIR  
 source ~/.bash_profile  

4.rerun flask,允许flask程序   
 sudo python index.py  
```

最后FLASK web页面
界面部分参考了：  
The html-page section refers to：https://blog.csdn.net/Rover95/article/details/118967794
最开始丑陋的第一版：  
The first version of the ugly:  
![image](https://user-images.githubusercontent.com/24267883/149650930-d07b2a08-a8ec-4453-9aaf-228d9b109eaf.png)

ip进行端口验证的页面：  
IP performs port verification page:  
http://127.0.0.1:80/login/  
![image](https://user-images.githubusercontent.com/24267883/149660421-1f9a6334-5b66-4727-8126-0211c5d8186a.png)

准入端口管理页面：  
Access port management page:  
http://127.0.0.1:80/ports/  
![image](https://user-images.githubusercontent.com/24267883/149660468-75981d5a-9499-40a2-9006-6468e17182ad.png)

查看某个端口下允许进入的IP：  
View IPs allowed under a port:  
http://127.0.0.1:80/port_search/?password=123456&port=6002


如果你要配置frp服务的话，请参考：  
If you want to configure the FRP service, please refer to  
https://github.com/fatedier/frp  

iptc 参考 ref：  
官方网站 official:https://github.com/ldx/python-iptables  

Python iptc库csdn的博客 https://blog.csdn.net/sinat_27690807/article/details/115999838?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-2.pc_relevant_paycolumn_v2&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-2.pc_relevant_paycolumn_v2&utm_relevant_index=5  



所有的iptables操作代码在iptables_OP.py 文件  
All code in iptables_op.py file  
EXAMPLE:使用示例  

```
#first command:
sudo python

#先检查端口是否合法 
#Check whether the port is valid
if check_port('6001',6000,7000):
    #you code here
    pass

#初始化指定端口 拒绝所有访问
#Initialize a specified port to deny all access
init_port("6001")

#删除6001的端口的拒绝访问
#Delete the access denial for port 6001
# delete_reject_port('6001')

#只允许'192.168.0.1' 访问6001端口
#Only '192.168.0.1' is allowed to access port 6001
add_ip('192.168.0.1','6001')

#只允许'192.168.0.2' 访问6001端口
#Only '192.168.0.2' is allowed to access port 6001
add_ip('192.168.0.2','6001')

# 禁止'192.168.0.2' 访问6001端口
# Prohibit '192.168.0.2' access 6001 port
delete_ip('192.168.0.2','6001')

#查看当前所有的权限设置  
View all current permission Settings  
iptc.easy.dump_all()
iptc.easy.dump_chain('filter','INPUT')

#...随意发挥 Free to play

```


