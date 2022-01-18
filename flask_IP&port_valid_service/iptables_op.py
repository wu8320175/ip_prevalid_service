import iptc

#Made by jerry5 2021/1/18
# 增删改查
table='filter'
chain='INPUT'


#初始拒绝所有对该端口的访问
def add_reject_port(port):
    #先禁止所有对指定端口的访问
    if find_reject_port(port) is None:
        rule_d = {'protocol': 'tcp', 'target': 'REJECT', 'tcp': {'dport': port}}
        iptc.easy.insert_rule(table,chain,rule_d)
        return True
    return False

#查找对应端口是否已经设置禁止访问
def find_reject_port(port):
    for i in iptc.easy.dump_chain(table,chain):
        if 'src' not in i:
            if 'tcp' in i and 'dport' in i['tcp'] and port in i['tcp']['dport']:
                return i
    return None

#删除对应的端口的禁止权限，并清除该端口下的所有ip
def delete_reject_port(port):
    res=find_reject_port(port)
    if res is not None:
        #清除端口
        iptc.easy.delete_rule(table,chain,res)
        #清除该端口下的所有ip
        for i in iptc.easy.dump_chain(table,chain):
            if 'src' not in i:
                if 'tcp' in i and 'dport' in i['tcp'] and port in i['tcp']['dport']:
                    iptc.easy.delete_rule(table,chain,i)
        return True
    return False

#获取所有被禁用的port
def get_all_port():
    port_list=[]
    for i in iptc.easy.dump_chain(table,chain):
        if 'src' not in i:
            if 'tcp' in i and 'dport' in i['tcp'] and 'REJECT' in i['target']:
                port_list.append(i['tcp']['dport'])
    return port_list


#获取所有在该port下允许访问的ip
def get_all_ip_in_port(port):
    ip_list=[]
    if find_reject_port(port) is None:
        return None
    for i in iptc.easy.dump_chain(table,chain):
        if 'src' in i:
            if 'tcp' in i and 'dport' in i['tcp'] and port in i['tcp']['dport'] and 'ACCEPT' in i['target']:
                ip_list.append(i['src'])
    return ip_list

#添加ip和指定端口  允许该ip访问该端口
def add_ip(ip,port):
    if find_ip(ip,port) is None:
        rule_d = {'protocol': 'tcp','src':ip, 'target': 'ACCEPT', 'tcp': {'dport': port}}
        iptc.easy.insert_rule(table,chain,rule_d)
        return True
    return False

#查找指定ip和端口
def find_ip(ip,port):
    for i in iptc.easy.dump_chain(table,chain):
        if 'src' in i and ip in i['src']:
            if 'tcp' in i and 'dport' in i['tcp'] and port in i['tcp']['dport']:
                return i
    return None

#查找某ip下设置的所有端口
def find_all_ip_ports(ip):
    port_list=[]
    for i in iptc.easy.dump_chain(table,chain):
        if 'src' in i and ip in i['src']:
            if 'tcp' in i and 'dport' in i['tcp']:
                port_list.append(i['tcp']['dport'])
    return port_list

#删除对应ip和端口，禁止该ip访问对应端口
def delete_ip(ip,port):
    res=find_ip(ip,port)
    if res is not None:
        iptc.easy.delete_rule(table,chain,res)
        return True
    return False

#将某ip允许访问的端口设置为另一个端口
def update_ip_port(ip,raw_port,des_port):
    delete_ip(ip,raw_port)
    add_ip(ip,des_port)

#检测端口是否合法，并且只允许在low-high的范围
import re
value = re.compile(r'^\d+?$')

def check_port(port):
    #port:str
    if not isinstance(port,int):
        port=str(port)

    if value.match(port):
        if int(port)>0 and int(port)<65535:
            return True
    return False
    

def check_port_range(port,low,high):
    #low,high  限制端口的范围
    if not isinstance(port,str):
        port=str(port)
    if not isinstance(low,str):
        low=str(low)
    if not isinstance(high,str):
        high=str(high)

    if check_port(port) and check_port(low) and check_port(high):
        if int(port)>=int(low) and int(port)<=int(high):
            return port
    return None
    
    # result = value.match(port)
    # if result and low<=port and port<=high:
    #     return str(port)
    # else:
    #     return None

# 检查当前设置的port是否在port_list内
def check_port_list(port,port_list):
    if not isinstance(port,str):
        port=str(port)
    if check_port(port) and port in port_list:
        return port
    else:
        return None