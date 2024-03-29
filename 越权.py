import sys
import re
import os
import json
import time
import glob
import requests
import base64
import urllib3
urllib3.disable_warnings()

from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtWidgets import *


proxies={}
################ 自定义函数 ################
def ecd(str):
    return str.replace('<','&lt;').replace('>','&gt;')
def jsonXmlBody(headers,body):
    if 'Content-Type' in headers.keys():
        if 'json' in headers['Content-Type'] and body.startswith('{'):
            return json.dumps(json.loads(body), indent=4, ensure_ascii=False, sort_keys=False,separators=(',', ';'))
        elif 'xml' in headers['Content-Type'] and body.startswith('<'):
            return printXML(body).replace('ns0:','')
        else:
            return '<br>'+ecd(body)
def str_to_json(str):
    dict1={}
    for i in str.split('\n'):
        dict1[i.partition(':')[0].strip()]=i.partition(':')[2].strip()
    return dict(filter(lambda x: x[0]!='',dict1.items())) #删除空key
def json_to_str(dict):
    return ''.join([key+': '+value+'\n' for key,value in dict.items()])

import xml.etree.ElementTree as ET
def printXML(str):          # XML 字符串格式化打印
    # 创建XML元素
    element = ET.XML(str)
    # 使用indent()函数进行格式化打印
    ET.indent(element)
    return ET.tostring(element, encoding='unicode')

def GetRequest(req): #从字符串获取请求内容
    method= req.partition(' ')[0].strip().lower()
    path=   req.partition(' ')[2].partition(' ')[0].strip()
    host=   req.partition('\n')[2].partition('\n')[0].partition(':')[2].strip()
    headers=req.partition('\n')[2].partition('\n')[2].partition('\n\n')[0].strip()
    dict_headers = str_to_json(headers)
    body = req.partition('\n\n')[2]
    if 'Content-Type' in dict_headers.keys() and 'json' in dict_headers['Content-Type'] and body.strip().startswith('{'):
        isjson=True
        body = json.loads(body)
    else:
        isjson=False
    if not (method and path and host):#缺失告警
        return False,method,path,host,headers,dict_headers,isjson,body
    else:
        return True,method,path,host,headers,dict_headers,isjson,body

def GetResponse(http,method,path,host,dict_headers,isjson,body):  #http为'http'或'https'
    url = http + "://" + host + path
    try:
        if method in ['get', 'options', 'delete','head']:
            res = eval('requests.' + method + '(url,headers=dict_headers,timeout=20,verify=False,proxies=proxies,allow_redirects=False)')
        elif method in ['post', 'put']:
            if isjson:
                res = eval('requests.' + method + '(url,headers=dict_headers,json=body,timeout=20,verify=False,proxies=proxies,allow_redirects=False)')
            else:
                res = eval('requests.' + method + '(url,headers=dict_headers,data=body,timeout=20,verify=False,proxies=proxies,allow_redirects=False)')
        else:#请求方式错误告警
            return False
    except:
        return False
    return url,res

################ 自定义QTextEdit + 失焦 ################
class MyQTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super(MyQTextEdit, self).__init__(parent)
    def setColor(self):
        if self.objectName()=='request': #self.request.setObjectName('request') 区分上色手法
            req = self.toPlainText()
            headers = req.partition('\n')[2].partition('\n\n')[0].strip()
            if req and headers:
                temp = []
                for i in headers.split('\n'):
                    temp.append('<span style="color:#00a000">%s</span>' % i.partition(':')[0] + ': ' + i.partition(':')[2].strip())
                self.setText(req.partition(headers)[0].replace('\n', '<br>') + '<br>'.join(temp) + req.partition(headers)[2].replace('\n', '<br>'))
        else:
            temp=[]
            for i in self.toPlainText().strip().split('\n'):
                if i:
                    temp.append('<span style="color:#00a000">%s</span>'% i.partition(':')[0]+': '+i.partition(':')[2].strip())
            self.setText('<br>'.join(temp))
    def focusOutEvent(self, event): #失焦
        super(MyQTextEdit, self).focusOutEvent(event)
        self.setColor()


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        ############## 获取配置文件，初始化配置文件 ##############
        self.configFile = 'BlackBox.config'
        self.logFile = time.strftime("%Y%m%d.html", time.localtime(time.time()))
        if not os.path.isfile(self.configFile):
            with open(self.configFile, 'w', encoding='utf-8') as f:
                f.write('#日志记录\nLog=True\n\n' +
                        '#http代理\nproxy=http://127.0.0.1:8080\n\n' +
                        '#用户session\n' +
                        'session5={"Referer":"baidu.com","origin":""}\n' +
                        'session6={"Cookie":"","X-Csrf_Token":""}\n\n' +
                        '#删除指定请求头\n' +
                        'delete_req_header=Cookie,X-Csrf_Token,Referer\n\n' +
                        '#检查响应头\n' +
                        'cherk_res_header={"x-content-type-option":"nosniff","Access-Control-Allow-Origin":"^http(.*?).baidu.com","Access-Control-Allow-Credentials":"true","X-Frame-Options":"(SAMEORIGIN)|(sameorigin)","Content-Security-Policy":"frame-ancestors https://*.baidu.com","x-xss-protection":"1; mode=block"}')
                f.close()

        ############## 读取配置 ##############
        self.sessions = {}
        self.LogSwitch = 'False'
        with open(self.configFile, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('Log'):
                    self.LogSwitch = line.partition('=')[2].strip()
                elif line.startswith('proxy'):
                    self.proxy1 = line.partition('=')[2].strip()
                elif line.startswith('session'):
                    self.sessions[line.partition('=')[0].strip()] = line.partition('=')[2].replace('\'', '"').strip()
                elif line.startswith('delete_req_header'):
                    self.delete_req_header1 = line.partition('=')[2].strip()
                elif line.startswith('cherk_res_header'):
                    self.check_res_header1 = line.partition('=')[2].replace('\'', '"').strip()
                elif line.startswith('request'):
                    self.request1 = line.partition('=')[2].strip()
            f.close()

        self.initUI()
        self.menu()
        self.show()
        ############## 状态栏显示 ##############
        self.status = self.statusBar()
        self.status.showMessage('越权测试 Bate 1.0   By:Abs1nThe', 5000)  # 状态栏显示 文本 5秒

    def update_check_state(self,action):
        if action.isChecked():
            action.setIconVisibleInMenu(True)  # 显示勾号
            value = 'True'
        else:
            action.setIconVisibleInMenu(False)  # 隐藏勾号
            value = 'False'
        if action.objectName()=='log':
            self.LogSwitch = value
            #self.updateConfigFile('Log=',value)
        elif action.objectName()=='setCookie':
            self.SetCookieSwitch = value


    # ############## 修改配置文件中日志的值 ##############          非必要
    # def updateConfigFile(self,key,value):
    #     with open(self.configFile, 'r', encoding='utf-8') as f:
    #         temp=[]
    #         for line in f:
    #             if line.startswith(key):
    #                 temp.append(key+value+'\n')
    #             else:
    #                 temp.append(line)
    #         f.close()
    #     with open(self.configFile, 'w', encoding='utf-8') as f:
    #         f.writelines(temp)
    #         f.close()
    def saveConfig_windows(self):

        # 创建新窗口
        self.new_window = QWidget()
        self.new_window.resize(int(app.desktop().screenGeometry(0).width() * 0.3), int(app.desktop().screenGeometry(0).height() * 0.3))
        self.new_window.setWindowTitle('保存配置')
        grid1 = QGridLayout(self)

        self.save_proxy = QCheckBox("代理", self)
        self.save_session1 = QCheckBox("session1", self)
        self.save_session2 = QCheckBox("session2", self)
        self.save_session3 = QCheckBox("session3", self)
        self.save_session4 = QCheckBox("session4", self)
        self.save_session5 = QCheckBox("session5", self)
        self.save_session6 = QCheckBox("session6", self)
        self.save_session6 = QCheckBox("session6", self)
        self.save_req = QCheckBox("request", self)
        self.save_req_header = QCheckBox("删除请求头", self)
        self.save_res_header = QCheckBox("检查响应头", self)
        self.selectAll_btn = QPushButton("全选", clicked=lambda: self.selectAll())
        self.saveConfig_btn = QPushButton("保存", clicked=lambda: self.saveConfig())
        grid1.addWidget(self.save_session1, 0, 0)
        grid1.addWidget(self.save_session2, 1, 0)
        grid1.addWidget(self.save_session3, 2, 0)
        grid1.addWidget(self.save_session4, 3, 0)
        grid1.addWidget(self.save_session5, 4, 0)
        grid1.addWidget(self.save_session6, 5, 0)
        grid1.addWidget(self.save_proxy, 0, 1)
        grid1.addWidget(self.save_req, 1, 1)
        grid1.addWidget(self.save_req_header, 2, 1)
        grid1.addWidget(self.save_res_header, 3, 1)
        grid1.addWidget(self.selectAll_btn, 4, 1)
        grid1.addWidget(self.saveConfig_btn, 5, 1)


        self.new_window.setLayout(grid1)
        self.new_window.show()
    def selectAll(self):
        for checkbox in self.new_window.findChildren(QCheckBox):#self.new_window中全部的QCheckBox
            checkbox.setChecked(True)
    def saveConfig(self):
        maxnum=0
        for i in glob.glob("BlackBox.config.bak*"):
            maxnum=int(re.findall(re.compile(r'BlackBox.config.bak(\d*)', re.S), i)[0])
        os.rename(self.configFile,"BlackBox.config.bak%d" %(maxnum+1))  #旧配置重命名
        with open(self.configFile, 'w', encoding='utf-8') as f:         #写入新配置文件
            f.write('#日志记录\nLog=True')

            for key, value in {
                'save_proxy':       ['self.proxy.text()',                               '\nproxy',                '\n\n#http代理'],
                '':['','','\n\n#用户session'],
                'save_session1':    ['str_to_json(self.session1.toPlainText())',        '\nsession1'],
                'save_session2':    ['str_to_json(self.session2.toPlainText())',        '\nsession2'],
                'save_session3':    ['str_to_json(self.session3.toPlainText())',        '\nsession3'],
                'save_session4':    ['str_to_json(self.session4.toPlainText())',        '\nsession4'],
                'save_session5':    ['str_to_json(self.session5.toPlainText())',        '\nsession5'],
                'save_session6':    ['str_to_json(self.session6.toPlainText())',        '\nsession6'],
                'save_req':         [r'self.request.toPlainText().replace("\n","\\n")',                      '\nrequest',              '\n\n#请求'],
                'save_req_header':  ['self.delete_req_header.toPlainText()',            '\ndelete_req_header',    '\n\n#删除指定请求头'],
                'save_res_header':  ['str_to_json(self.check_res_header.toPlainText())','\ncherk_res_header',     '\n\n#检查响应头']
            }.items():
                if  not key :#空值，只输出value[2]
                    f.write(value[2])
                elif eval('self.'+key+'.isChecked()'):
                    try:
                        f.write(value[2])
                    except:pass
                    f.write(value[1]+'='+str(eval(value[0])))
            f.close()
        self.new_window.close()#关闭窗口



    def menu(self):
        ############## 菜单栏 ##############
        bar = self.menuBar()
        # 往菜单栏添加菜单项目
        file = bar.addMenu("文件")
        # 给菜单项目添加子菜单
        # new = file.addAction("新建")

        save = file.addAction("保存配置")
        save.setShortcut("CTRL+S")  # 设置快捷键
        save.triggered.connect(self.saveConfig_windows)

        action_log = QAction('记录日志', self, checkable=True)
        action_log.setObjectName('log')
        if self.LogSwitch == 'True':
            action_log.setChecked(True)
        action_log.triggered.connect(lambda: self.update_check_state(action_log))
        file.addAction(action_log)

        self.SetCookieSwitch='False'    ########################                  self.SetCookieSwitch
        action_SetCookie=QAction('Set-Cookie', self, checkable=True)
        action_SetCookie.setObjectName('setCookie')
        action_SetCookie.triggered.connect(lambda: self.update_check_state(action_SetCookie))
        file.addAction(action_SetCookie)

    def initUI(self):

        self.setWindowTitle('越权测试 Bate 1.0   By:Abs1nThe')
        self.resize(int(app.desktop().screenGeometry(0).width() * 0.9), int(app.desktop().screenGeometry(0).height() * 0.8))


        ############## base64 Logo ##############
        ico='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'
        logo=QPixmap()
        logo.loadFromData(base64.b64decode(ico))
        icon=QIcon()
        icon.addPixmap(logo,QIcon.Normal,QIcon.Off)
        self.setWindowIcon(icon)
        # self.setWindowIcon(QIcon('logo.ico'))

        ############## 1 ##############
        grid = QGridLayout(self)
        self.https = QComboBox(self)
        self.https.addItems(['https', 'http'])
        grid.addWidget(self.https, 0, 0)
        grid.addWidget(QLabel('session1',self), 1, 0)
        grid.addWidget(QLabel('session2',self), 2, 0)
        grid.addWidget(QLabel('session3',self), 3, 0)
        grid.addWidget(QLabel('session4',self), 4, 0)
        grid.addWidget(QLabel('session5',self), 5, 0)
        grid.addWidget(QLabel('session6',self), 6, 0, 2, 1)

        ############## 2 ##############
        self.session1 = MyQTextEdit(self)# 失焦
        self.session2 = MyQTextEdit(self)
        self.session3 = MyQTextEdit(self)
        self.session4 = MyQTextEdit(self)
        self.session5 = MyQTextEdit(self)
        self.session6 = MyQTextEdit(self)

        grid.addWidget(self.session1, 1, 1)
        grid.addWidget(self.session2, 2, 1)
        grid.addWidget(self.session3, 3, 1)
        grid.addWidget(self.session4, 4, 1)
        grid.addWidget(self.session5, 5, 1)
        grid.addWidget(self.session6, 6, 1, 2, 1)

        ############## 3 ##############
        self.proxy_button = QCheckBox("启用代理",self)
        grid.addWidget(self.proxy_button, 0, 2)
        run1 = QPushButton("run", clicked=lambda: self.runReq(self.session1))
        run2 = QPushButton("run", clicked=lambda: self.runReq(self.session2))
        run3 = QPushButton("run", clicked=lambda: self.runReq(self.session3))
        run4 = QPushButton("run", clicked=lambda: self.runReq(self.session4))
        run5 = QPushButton("run", clicked=lambda: self.runReq(self.session5))
        run6 = QPushButton("run", clicked=lambda: self.runReq(self.session6))
        grid.addWidget(run1, 1, 2)
        grid.addWidget(run2, 2, 2)
        grid.addWidget(run3, 3, 2)
        grid.addWidget(run4, 4, 2)
        grid.addWidget(run5, 5, 2)
        grid.addWidget(run6, 6, 2, 2, 1)

        ############## 4 ##############
        self.proxy = QLineEdit(self)
        self.request = MyQTextEdit(self)# 失焦
        self.request.setObjectName('request')
        self.request.setPlaceholderText("request")
        self.delete_header_button = QCheckBox("删除指定请求头", self)
        self.delete_req_header = QTextEdit(self)
        grid.addWidget(self.proxy, 0, 3)
        grid.addWidget(self.request, 1, 3, 5, 1)
        grid.addWidget(self.delete_header_button, 6, 3)
        grid.addWidget(self.delete_req_header, 7, 3)


        ############## 5 ##############
        self.response = QTextEdit(self)
        self.response.setPlaceholderText("response")
        self.check_res_header_button = QCheckBox("检查响应头",self)
        self.check_res_header = MyQTextEdit(self)# 失焦
        grid.addWidget(self.response, 1, 4, 5, 1)
        grid.addWidget(self.check_res_header_button, 6, 4)
        grid.addWidget(self.check_res_header, 7, 4)

        ############## 赋值 ##############
        for key, value in self.sessions.items():
            eval('self.'+key + '.setText(json_to_str(' + value + ').strip())')
        for key,value in {'proxy':'self.proxy1.strip()','request':r'self.request1.replace("\\n","\n")',
                          'delete_req_header':'self.delete_req_header1.strip()',
                          'check_res_header':'json_to_str(json.loads(self.check_res_header1)).strip()'}.items():
            try:
                eval('self.'+key+'.setText('+value+')')
            except:pass
        ############## 上色 ##############
        self.session1.setColor()
        self.session2.setColor()
        self.session3.setColor()
        self.session4.setColor()
        self.session5.setColor()
        self.session6.setColor()
        self.check_res_header.setColor()
        self.request.setColor()

        ############## 不接受用户的富文本插入 ##############
        self.session1.setAcceptRichText(False)
        self.session2.setAcceptRichText(False)
        self.session3.setAcceptRichText(False)
        self.session4.setAcceptRichText(False)
        self.session5.setAcceptRichText(False)
        self.session6.setAcceptRichText(False)
        self.check_res_header.setAcceptRichText(False)
        self.response.setAcceptRichText(False)
        self.delete_req_header.setAcceptRichText(False)
        self.request.setAcceptRichText(False)

        ############## 创建主界面窗口并设置为中心窗口 ##############
        mainwidget = QWidget()
        mainwidget.setLayout(grid)
        self.setCentralWidget(mainwidget)


    def runReq(self,textEdit):
        # print(self.SetCookieSwitch)

        self.response.clear()

        session=textEdit.toPlainText()
        ############## 设置代理 ##############
        if self.proxy_button.isChecked():
            proxies.update({'http': self.proxy.text(), 'https': self.proxy.text()})
        else:
            proxies.update({'http': '', 'https': ''})

        ############## 从request获取请求方式、path、header等 ##############
        req = self.request.toPlainText()
        iferror, method, path, host, headers, dict_headers, isjson, body = GetRequest(req)
        if not iferror:  # 缺失告警
            self.response.setText('<span style="color:#ff0000">bad request</span>')
            self.status.showMessage('Error 请求失败,检查method,path,host', 5000)
            return

        ############## 删除长度，替换session ##############
        try:
            del dict_headers['Content-Length']
        except:
            pass
        jsonSession=str_to_json(session)
        for key, value in jsonSession.items():
            dict_headers[key] = value

        ############## 删除指定请求头 ##############
        if self.delete_header_button.isChecked():
            for i in self.delete_req_header.toPlainText().split(','):
                try:
                    dict_headers.pop(i.strip())
                except:
                    pass


        self.status.showMessage('Loading...', 5000)
        ############## 发送请求 ##############
        try:
            url, res = GetResponse(self.https.currentText(), method, path, host, dict_headers, isjson, body)
        except:
            self.response.setText('<span style="color:#ff0000">request fail,check host or http</span>')
            self.status.showMessage('Error 请求失败,检查host,http', 5000)
            return

        req_1=req.partition(headers)[0]
        req_2=req.partition(headers)[2]
        ############## 记录日志 ##############html
        if self.LogSwitch == 'True':
            if not os.path.isfile(self.logFile):
                with open(self.logFile, 'a', encoding='utf-8') as log:
                    log.write('<head><style type="text/css">.div1{margin-left:40px;}</style></head>')
                    log.close()
            with open(self.logFile, 'a', encoding='utf-8') as log:
                log.write(time.strftime("<details><summary>[%Y/%m/%d %H:%M:%S] ",
                                        time.localtime(time.time())) + url + "</summary>" +
                          "<div class=\"div1\"><p>" + req_1.replace('\n', '<br>') +
                          ''.join([key + ': ' + value + '<br>' for key, value in dict_headers.items()]) + req_2.replace('\n', '<br>') + "</p><br>")
                log.write('<p>[response:]<br>' + str(res.status_code) + " " + res.reason + "<br>" +
                          ''.join([k + ':' + v + '<br>' for k, v in res.headers.items()]) + "<br><span>" +
                          ecd(res.text) + "</span></p></div></details>")
                log.close()

        ############## 检查响应头 ##############
        bad_res_header = []  # 错误响应头
        lack_res_header = []  # 缺失响应头
        if self.check_res_header_button.isChecked():
            for key, value in str_to_json(self.check_res_header.toPlainText()).items():
                if key in res.headers.keys() and not (
                        value == res.headers[key] or re.findall(value, res.headers[key])):
                    bad_res_header.append(key)
                else:
                    lack_res_header.append(key)

        ############## 输出响应码，响应头 ##############
        response_text = str(res.status_code) + ' ' + res.reason + '<br>'
        for key, value in res.headers.items():
            if key in bad_res_header+['Set-Cookie']:
                response_text += '<span style="color:#ff0000">%s: %s</span><br>' % (str(key), str(value))
            else:
                response_text += '<span style="color:#00a000">%s:</span> %s<br>' % (str(key), str(value))
        if len(lack_res_header) > 0:
            response_text += '<span style="color:#ff0000">缺失响应头: <br>' + '<br>'.join(
                lack_res_header) + '</span><br>'
        self.response.setText(response_text)

        ############## 输出响应体 ##############
        self.response.append(jsonXmlBody(res.headers,res.text.strip()))
        self.status.showMessage('Success 请求成功', 5000)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        with open(glob.glob("*.qss")[0]) as f:
            app.setStyleSheet(f.read())
            f.close()
    except:pass
    ex = Example()
    sys.exit(app.exec_())

