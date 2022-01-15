#
# 增删改查,Add, delete, modify and query
table='filter'
chain='INPUT'
#如果没有特殊需求，不需要修改，If there are no special requirements, no modification is required

#初始拒绝所有对该端口的访问
def init_port(port):
    #先禁止所有对指定端口的访问 
    #First, disable all access to the specified port
    if find_reject_port(port) is None:
        rule_d = {'protocol': 'tcp', 'target': 'REJECT', 'tcp': {'dport': port}}
        iptc.easy.insert_rule(table,chain,rule_d)
        return True
    return False

#查找对应端口是否已经设置禁止访问
#Check whether the corresponding port has been disabled
def find_reject_port(port):
    for i in iptc.easy.dump_chain(table,chain):
        if 'src' not in i:
            if 'tcp' in i and 'dport' in i['tcp'] and port in i['tcp']['dport']:
                return i
    return None

#删除对应的端口的禁止权限
#Delete the deny permission of the corresponding port

def delete_reject_port(port):
    res=find_reject_port(port)
    if res is not None:
        iptc.easy.delete_rule(table,chain,res)
        return True
    return False

#添加ip和指定端口  允许该ip访问该端口
#Add an IP address and specify a port to allow the IP address to access the port
def add_ip(ip,port):
    if find_ip(ip,port) is None:
        rule_d = {'protocol': 'tcp','src':ip, 'target': 'ACCEPT', 'tcp': {'dport': port}}
        iptc.easy.insert_rule(table,chain,rule_d)
        return True
    return False

#检查指定ip和端口是否已经设置
#Check whether the specified IP address and port are set
def find_ip(ip,port):
    for i in iptc.easy.dump_chain(table,chain):
        if 'src' in i and ip in i['src']:
            if 'tcp' in i and 'dport' in i['tcp'] and port in i['tcp']['dport']:
                return i
    return None

#查找某ip下设置的所有允许访问端口
#Finds all allowed ports set under an IP address
def find_all_ip_ports(ip):
    port_list=[]
    for i in iptc.easy.dump_chain(table,chain):
        if 'src' in i and ip in i['src']:
            if 'tcp' in i and 'dport' in i['tcp']:
                port_list.append(i['tcp']['dport'])
    return port_list

#删除对应ip和端口，禁止该ip访问对应端口
#Delete the corresponding IP address and port and forbid the IP address from accessing the corresponding port
def delete_ip(ip,port):
    res=find_ip(ip,port)
    if res is not None:
        iptc.easy.delete_rule(table,chain,res)
        return True
    return False

#将某ip允许访问的端口设置为另一个端口
#Set the port that one IP address is allowed to access to another port
def update_ip_port(ip,raw_port,des_port):
    delete_ip(ip,raw_port)
    add_ip(ip,des_port)

#检测端口是否合法，并且只允许在low-high的范围
#Check whether the port is valid and only allowed in the low-high range
import re
value = re.compile(r'^\d+?$')
def check_port(port,low,high):
    #low,high  限制端口的范围
    if not isinstance(port,str):
        port=str(port)
    result = value.match(port)
    if result and low<=int(port) and int(port)<=high:
        return True
    else:
        return False
