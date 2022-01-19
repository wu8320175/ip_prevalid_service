# -*- coding:utf-8 -*-
from distutils.command.config import config
import re
from flask import Flask,render_template,request,redirect,url_for,session,flash,abort,Response
import iptables_op as op
import json
import sys

#Made by jerry5 2021/1/18
config_path = './config.json'
#读取配置 config
with open(config_path) as f:
    portconfig=json.load(f)

app = Flask(__name__)
# app.debug=True
#必须sudo启动 run：
#sudo gunicorn -w 4 -b 0.0.0.0:6001  index:app

@app.before_first_request
def before_first_request():
    #检查当前web端口是否在禁用的端口列表里
    web_port = request.host.split(":")[-1].strip()
    if web_port in portconfig["port_list"]:
        raise Exception('web端口不能设置在端口禁用列表内,请重新设置config')
    else:
        #预先将端口添加到禁用名单
        for p in portconfig["port_list"]:
            p=str(p)
            if op.add_reject_port(p):
                print("端口"+p+"初始化成功！")
            else:
                print("端口"+p+"之前已经被初始化")

## 端口二次验证页面
@app.route('/login/',methods=['GET','POST'])
def login():
    rd_html='login/login_frame.html'
    return render_template(rd_html,url=url_for("login_inner"))
    
## 端口二次验证页面
@app.route('/login_inner/',methods=['GET','POST'])
def login_inner():
    if request.host.split(":")[-1].strip() in portconfig["port_list"]:
        raise Exception('web端口不能设置在端口禁用列表内,请重新设置config')
    #基础信息
    cur_ip  = request.remote_addr
    port_list=str(op.find_all_ip_ports(cur_ip))
    
    rd_html='login/login.html'

    #放行验证POST
    if request.method == 'POST':
        
        #验证口令
        password = request.form.get('password')
        if password != portconfig['password']:
            return render_template(rd_html,status=2,msg='口令错误')
        cur_ip = request.form.get('cur_ip')
        #验证端口
        port = op.check_port_list(request.form.get('port'),portconfig["port_list"])
        if port is None:
            return render_template(rd_html,status=2,msg='端口格式错误，或不在放行范围内！',cur_ip=cur_ip,port_list=port_list)

#         #检查并禁止端口，如果是新增加返回true，已存在则返回false
#         for p in portconfig["port_list"]:
#             if op.init_port(p):
#                 print(p,"端口成功禁用！")
#             else:
#                 print(p,"端口之前已经被禁用！")
#         op.init_port(port)
        if request.form.get('allow'):
            #检查是否已经放行了ip和端口
            if op.find_ip(cur_ip,port) is not None:
                return render_template(rd_html,status=2,msg='该ip已经放行了该端口！',cur_ip=cur_ip,port_list=port_list)
            
            
            #放行ip到指定端口
            if op.add_ip(cur_ip,port):
                # return redirect(url_for('auth.login')) 
                #return redirect(url_for('login',status=1,msg='端口'+port+'放行成功！'))
                return render_template(rd_html,status=1,msg='端口'+port+'放行成功！',cur_ip=cur_ip,port_list=port_list)

            else:
                #return redirect(url_for('login',status=2,msg='端口'+port+'放行失败！'))
                
                return render_template(rd_html,status=2,msg='端口'+port+'放行失败！',cur_ip=cur_ip,port_list=port_list)
        elif request.form.get('ban'):
            #禁止ip和端口
            if op.find_ip(cur_ip,port) is None:
                return render_template(rd_html,status=2,msg='该ip未放行该端口！',cur_ip=cur_ip,port_list=port_list)
            
            if op.delete_ip(cur_ip,port):
                #return redirect(url_for('login',status=1,msg='端口'+port+'禁止成功！'))
                return render_template(rd_html,status=1,msg='端口'+port+'禁止成功！',cur_ip=cur_ip,port_list=port_list)
            else:
                #return redirect(url_for('login',status=2,msg='端口'+port+'禁止失败！'))
                return render_template(rd_html,status=2,msg='端口'+port+'禁止失败！',cur_ip=cur_ip,port_list=port_list)
    
    #status 初始进入是0，验证成功后改为1，验证失败后改为2
    return render_template(rd_html,status=0,cur_ip=cur_ip,port_list=port_list)




#清除指定端口的函数
def delete_port(port):
    if op.delete_reject_port(port):
        if port in portconfig['port_list']:
            #移除并写回config文件
            portconfig['port_list'].remove(port)
            with open(config_path,'w') as f:
                json.dump(portconfig,f)
        return True
        # return port+'禁止端口清除成功！'
    else:
        return False
        # return port+'禁止端口清除失败！' 

#添加指定端口的函数
def add_port(port):
    if op.add_reject_port(port):
        if port not in portconfig['port_list']:
            #移除并写回config文件
            portconfig['port_list'].append(port)
            with open(config_path,'w') as f:
                json.dump(portconfig,f)
        return True
        # return port+'添加禁止端口成功！'
    else:
        return False
        # return port+'添加禁止端口失败！' 

## 端口二次验证页面
@app.route('/port_search/',methods=['GET','POST'])
def port_search():
    rd_html='port/port_search_frame.html'
    return render_template(rd_html,url=url_for("port_search_inner"))

@app.route('/port_search_inner/',methods=['GET','POST'])
def port_search_inner():
    if request.host.split(":")[-1].strip() in portconfig["port_list"]:
        raise Exception('web端口不能设置在端口禁用列表内,请重新设置config')
    
    
    rd_html='port/port_search.html'

    #放行验证POST
    if request.method == 'POST':
        
        #验证口令
        password = request.form.get('password')
        if password != portconfig['password']:
            return render_template(rd_html,status=2,msg='口令错误')
        
        port=request.form.get('port').strip()

        # 检查port
        if not op.check_port(port):
            return render_template(rd_html,status=2,msg='端口格式存在问题！')

        ip_list=op.get_all_ip_in_port(port)
        if ip_list is not None:
            return render_template(rd_html,status=1,port=port,ip_list=str(ip_list))
        else:
            return render_template(rd_html,status=2,msg="该端口下没有放行的ip")

    return render_template(rd_html,status=0)


## 端口二次验证页面
@app.route('/ports/',methods=['GET','POST'])
def ports():
    rd_html='port/ports_frame.html'
    return render_template(rd_html,url=url_for("ports_inner"))

## 端口二次验证页面
@app.route('/ports_inner/',methods=['GET','POST'])
def ports_inner():
    web_port = request.host.split(":")[-1].strip()
    if web_port in portconfig["port_list"]:
        raise Exception('web端口不能设置在端口禁用列表内,请重新设置config')
    #基础信息
    port_list=str(op.get_all_port())
    
    rd_html='port/ports.html'

    #放行验证POST
    if request.method == 'POST':
        
        #验证口令
        password = request.form.get('password')
        if password != portconfig['password']:
            return render_template(rd_html,status=2,msg='口令错误')
        
        port=request.form.get('port').strip()

        # 检查port
        if not op.check_port(port):
            return render_template(rd_html,status=2,msg='端口格式存在问题！',port_list=port_list)

        if port == portconfig['web_port']:
            return render_template(rd_html,status=2,msg='禁止端口不能和web端口相同！',port_list=port_list)
        
        if request.form.get('add'):
            #添加端口
            if add_port(port):
                return render_template(rd_html,status=1,msg='禁止端口'+port+'添加成功',port_list=port_list)
            else:
                return render_template(rd_html,status=2,msg='禁止端口'+port+'添加失败！或已经存在！',port_list=port_list)

        elif request.form.get('delete'):
            #删除端口
            if delete_port(port):
                return render_template(rd_html,status=1,msg='禁止端口'+port+'删除成功或不存在！',port_list=port_list)
            else:
                return render_template(rd_html,status=2,msg='禁止端口'+port+'删除失败！',port_list=port_list)

    #status 初始进入是0，验证成功后改为1，验证失败后改为2
    return render_template(rd_html,status=0,port_list=port_list)
    
if __name__ == '__main__':
    if portconfig['web_port'] in portconfig['port_list']:
        raise Exception('web端口不能设置在端口禁用列表内,请重新设置config')
    app.run(host="0.0.0.0", port=portconfig['web_port'])