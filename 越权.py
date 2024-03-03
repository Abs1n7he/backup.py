import sys
import re
import os
import json
import time
import glob
import requests
import urllib
import urllib3
urllib3.disable_warnings()

from PyQt5.QtGui import QIcon, QTextCharFormat,QPixmap, QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSlot, QMetaObject

proxies={}
def ecd(str):
    return str.replace('<','&lt;').replace('>','&gt;')
def str_to_json(str):
    dict={}
    for i in str.split('\n'):
        dict[i.partition(':')[0]]=i.partition(':')[2].strip()
    while '' in dict.keys():
        dict.pop('')
    return dict
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
    if 'Content-Type' in dict_headers.keys() and 'json' in dict_headers['Content-Type'] and body[0] == '{':
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
        self.status.showMessage('黑盒越权测试 Bate 1.1   By:Abs1nThe', 5000)  # 状态栏显示 文本 5秒


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
        if self.LogSwitch == 'True':
            action_log.setChecked(True)
        action_log.triggered.connect(lambda: self.update_check_state(action_log))
        log=file.addAction(action_log)
    def update_check_state(self, action):
        if action.isChecked():
            action.setIconVisibleInMenu(True)  # 显示勾号
            self.LogSwitch = 'True'
        else:
            action.setIconVisibleInMenu(False)  # 隐藏勾号
            self.LogSwitch = 'False'
        self.updateConfigFile('Log=',self.LogSwitch)
    ############## 修改配置文件中日志的值 ##############
    def updateConfigFile(self,key,value):
        with open(self.configFile, 'r', encoding='utf-8') as f:
            temp=[]
            for line in f:
                if line.startswith(key):
                    temp.append('Log='+value+'\n')
                else:
                    temp.append(line)
            f.close()
        with open(self.configFile, 'w', encoding='utf-8') as f:
            f.writelines(temp)
            f.close()

    def saveConfig_windows(self):

        # 创建新窗口
        self.new_window = QWidget()
        self.new_window.resize(int(app.desktop().width() * 0.3), int(app.desktop().height() * 0.3))
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



    def initUI(self):
        self.setWindowIcon(QIcon('logo.ico'))
        self.resize(int(app.desktop().width() * 0.9), int(app.desktop().height() * 0.8))
        self.setWindowTitle('黑盒越权测试 Bate 1.1   By:Abs1nThe')



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
        self.session1 = QTextEdit(self)
        self.session2 = QTextEdit(self)
        self.session3 = QTextEdit(self)
        self.session4 = QTextEdit(self)
        self.session5 = QTextEdit(self)
        self.session6 = QTextEdit(self)
        grid.addWidget(self.session1, 1, 1)
        grid.addWidget(self.session2, 2, 1)
        grid.addWidget(self.session3, 3, 1)
        grid.addWidget(self.session4, 4, 1)
        grid.addWidget(self.session5, 5, 1)
        grid.addWidget(self.session6, 6, 1, 2, 1)

        ############## 3 ##############
        self.proxy_button = QCheckBox("启用代理",self)
        grid.addWidget(self.proxy_button, 0, 2)
        run1 = QPushButton("run", clicked=lambda: self.runReq(self.session1.toPlainText()))
        run2 = QPushButton("run", clicked=lambda: self.runReq(self.session2.toPlainText()))
        run3 = QPushButton("run", clicked=lambda: self.runReq(self.session3.toPlainText()))
        run4 = QPushButton("run", clicked=lambda: self.runReq(self.session4.toPlainText()))
        run5 = QPushButton("run", clicked=lambda: self.runReq(self.session5.toPlainText()))
        run6 = QPushButton("run", clicked=lambda: self.runReq(self.session6.toPlainText()))
        grid.addWidget(run1, 1, 2)
        grid.addWidget(run2, 2, 2)
        grid.addWidget(run3, 3, 2)
        grid.addWidget(run4, 4, 2)
        grid.addWidget(run5, 5, 2)
        grid.addWidget(run6, 6, 2, 2, 1)

        ############## 4 ##############
        self.proxy = QLineEdit(self)
        self.request = QTextEdit(self)
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
        self.check_res_header = QTextEdit(self)
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



    def runReq(self,session):
        ############## 设置代理 ##############
        if self.proxy_button.isChecked():
            proxies.update({'http': self.proxy.text(), 'https': self.proxy.text()})

        ############## 从request获取请求方式、path、header等 ##############
        req = self.request.toPlainText()
        iferror, method, path, host, headers, dict_headers, isjson, body = GetRequest(req)
        if not iferror:  # 缺失告警
            self.response.setText('<span style="color:#ff0000">bad request</span>')
            self.status.showMessage('Error 请求失败,检查method,path,host', 5000)
            return

        ############## 删除长度，替换session ##############
        try:
            dict_headers.pop('Content-length')
        except:
            pass
        for key, value in str_to_json(session).items():
            dict_headers[key] = value

        ############## 删除指定请求头 ##############
        if self.delete_header_button.isChecked():
            for i in self.delete_req_header.toPlainText().split(','):
                try:
                    dict_headers.pop(i.strip())
                except:
                    pass

        # 置空
        self.response.setText('')
        self.status.showMessage('Loading...', 5000)
        ############## 发送请求 ##############
        try:
            url, res = GetResponse(self.https.currentText(), method, path, host, dict_headers, isjson, body)
        except:
            self.response.setText('<span style="color:#ff0000">request fail,check host or http</span>')
            self.status.showMessage('Error 请求失败,检查host,http', 5000)
            return

        ############## 记录日志 ##############html
        if self.LogSwitch == 'True':
            if not os.path.isfile(self.logFile):
                with open(self.logFile, 'a', encoding='utf-8') as log:
                    log.write('<head><style type="text/css">.div1{margin-left:40px;}</style></head>')
                    log.close()
            with open(self.logFile, 'a', encoding='utf-8') as log:
                log.write(time.strftime("<details><summary>[%Y/%m/%d %H:%M:%S] ",
                                        time.localtime(time.time())) + url + "</summary>" +
                          "<div class=\"div1\"><p>" + req.partition(headers)[0].replace('\n', '<br>') + ''.join(
                    [key + ': ' + value + '<br>' for key, value in dict_headers.items()]) + req.partition(headers)[
                              2].replace('\n', '<br>') + "</p><br>")
                log.write('<p>[response:]<br>' + str(res.status_code) + " " + res.reason + "<br>" +
                          ''.join([k + ':' + v + '<br>' for k, v in res.headers.items()]) + "<br>" +
                          res.text + "</p></div></details>")
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
            if key in bad_res_header:
                response_text += '<span style="color:#ff0000">%s: %s</span><br>' % (str(key), str(value))
            else:
                response_text += '<span style="color:#00a000">%s:</span> %s<br>' % (str(key), str(value))
        if len(lack_res_header) > 0:
            response_text += '<span style="color:#ff0000">缺失响应头: <br>' + '<br>'.join(
                lack_res_header) + '</span><br>'
        self.response.setText(response_text)

        ############## 输出响应体 ##############
        if 'application/json' in res.headers['Content-Type'] and res.text[0] == '{':
            self.response.append(json.dumps(json.loads(res.text), indent=4, ensure_ascii=False, sort_keys=False,
                                       separators=(',', ';')))
        elif 'xml' in res.headers['Content-Type'] and res.text[0] == '<':
            self.response.append(printXML(res.text).replace('ns0:', ''))
        else:
            self.response.append('<br>' + ecd(res.text))
        self.status.showMessage('Success 请求成功', 5000)

if __name__ == '__main__':


    app = QApplication(sys.argv)
    qss="Aqua.qss"
    try:
        with open(glob.glob("*.qss")[0]) as f:
            app.setStyleSheet(f.read())
            f.close()
    except:pass
    ex = Example()
    sys.exit(app.exec_())

