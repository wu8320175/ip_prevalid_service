​
## 背景 background：

        服务器使用frp后，贼难受被人下了挖矿病毒，痛定思痛决定给服务器加上二次验证，只允许指定ip来访问端口，避免不正常的ip来扫描我的端口。。。所以花了一天时间写个小验证程序
        After the server used FRP, the thief was attacked by a mining virus. After learning from the experience, he decided to add a secondary verification to the server. Only the specified IP is allowed to access the port, so as to avoid abnormal IP scanning my port... So I spent a day writing a small verification program

## 实现的功能如下 functions：

1. 指定的端口，首先所有ip都不能访问，然后根据web服务验证的结果允许该ip来访问指定端口。
The specified port is first inaccessible to all IP addresses and then allowed to access the specified port based on the result of web service authentication.

2.将以上功能封装成web服务，先在网页端通过 二级密码 来允许当前ip的访问服务器，当前ip才能访问目的ip和端口，比如ssh服务等。
Encapsulate the above functions into web services. First, allow the current IP to access the server through the secondary password on the web page, and the current IP can access the destination IP and port, such as SSH service.

## 使用工具 tools：

        Python，python-iptables库，flask （用于web服务）

## 原因： python简单。。。。。，flask搭个服务更简单。
Reason:Python is simple....., Flask takes a service easier

首先python-iptables库安装和使用
First Python-iptables library installation and use

pip install --upgrade python-iptables

参考 ref：
官方网站 official:https://github.com/ldx/python-iptables

Python iptc库csdn的博客 https://blog.csdn.net/sinat_27690807/article/details/115999838?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-2.pc_relevant_paycolumn_v2&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7Edefault-2.pc_relevant_paycolumn_v2&utm_relevant_index=5

FLASK部分还没打算写：
如果有朋友有需要我再更吧。。
The flash section is not intended to write:
If anynoe needs it, I'll add this part.


EXAMPLE:使用示例
```
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
#...随意发挥 Free to play
```
