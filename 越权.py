import sys
import re
import os
import json
import time
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

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('logo.ico'))
        self.resize(int(app.desktop().width() * 0.9), int(app.desktop().height() * 0.8))
        self.setWindowTitle('黑盒越权测试 Bate   By:Abs1nThe')

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
        session1 = QTextEdit(self)
        session2 = QTextEdit(self)
        session3 = QTextEdit(self)
        session4 = QTextEdit(self)
        session5 = QTextEdit(self)
        session6 = QTextEdit(self)
        grid.addWidget(session1, 1, 1)
        grid.addWidget(session2, 2, 1)
        grid.addWidget(session3, 3, 1)
        grid.addWidget(session4, 4, 1)
        grid.addWidget(session5, 5, 1)
        grid.addWidget(session6, 6, 1, 2, 1)
        for key, value in sessions.items():
            eval(key + ".setText(json_to_str(json.loads(sessions['" + key + "'])).strip())")

        ############## 3 ##############
        self.proxy_button = QCheckBox("启用代理",self)
        grid.addWidget(self.proxy_button, 0, 2)
        run1 = QPushButton("run", clicked=lambda: self.runReq(session1.toPlainText()))
        run2 = QPushButton("run", clicked=lambda: self.runReq(session2.toPlainText()))
        run3 = QPushButton("run", clicked=lambda: self.runReq(session3.toPlainText()))
        run4 = QPushButton("run", clicked=lambda: self.runReq(session4.toPlainText()))
        run5 = QPushButton("run", clicked=lambda: self.runReq(session5.toPlainText()))
        run6 = QPushButton("run", clicked=lambda: self.runReq(session6.toPlainText()))
        grid.addWidget(run1, 1, 2)
        grid.addWidget(run2, 2, 2)
        grid.addWidget(run3, 3, 2)
        grid.addWidget(run4, 4, 2)
        grid.addWidget(run5, 5, 2)
        grid.addWidget(run6, 6, 2, 2, 1)

        ############## 4 ##############
        self.proxy = QLineEdit(self)
        try:
            self.proxy.setText(proxy1.strip())
        except:
            pass
        self.requests1 = QTextEdit(self)
        self.requests1.setPlaceholderText("request")

        self.delete_header_button = QCheckBox("删除指定请求头",self)
        self.delete_req_header = QTextEdit(self)
        try:
            self.delete_req_header.setText(delete_req_header1.strip())
        except:
            pass

        grid.addWidget(self.proxy, 0, 3)
        grid.addWidget(self.requests1, 1, 3, 5, 1)
        grid.addWidget(self.delete_header_button, 6, 3)
        grid.addWidget(self.delete_req_header, 7, 3)

        ############## 5 ##############

        self.response = QTextEdit(self)
        self.response.setPlaceholderText("response")
        self.check_res_header_button = QCheckBox("检查响应头",self)
        self.check_res_header = QTextEdit(self)
        try:
            self.check_res_header.setText(json_to_str(json.loads(check_res_header1)).strip())
        except:
            pass

        grid.addWidget(self.response, 1, 4, 5, 1)
        grid.addWidget(self.check_res_header_button, 6, 4)
        grid.addWidget(self.check_res_header, 7, 4)

        ############## 不接受用户的富文本插入 ##############
        session1.setAcceptRichText(False)
        session2.setAcceptRichText(False)
        session3.setAcceptRichText(False)
        session4.setAcceptRichText(False)
        session5.setAcceptRichText(False)
        session6.setAcceptRichText(False)
        self.check_res_header.setAcceptRichText(False)
        self.response.setAcceptRichText(False)
        self.delete_req_header.setAcceptRichText(False)
        self.requests1.setAcceptRichText(False)

        self.show()

    def runReq(self,session):
        ############## 设置代理 ##############
        if self.proxy_button.isChecked():
            proxies.update({'http': self.proxy.text(), 'https': self.proxy.text()})

        ############## 从request获取请求方式、path、header等 ##############
        req = self.requests1.toPlainText()
        iferror, method, path, host, headers, dict_headers, isjson, body = GetRequest(req)
        if not iferror:  # 缺失告警
            self.response.setText('<span style="color:#ff0000">bad request</span>')
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
        ############## 发送请求 ##############
        try:
            url, res = GetResponse(self.https.currentText(), method, path, host, dict_headers, isjson, body)
        except:
            self.response.setText('<span style="color:#ff0000">request fail,check host or http</span>')
            return

        ############## 记录日志 ##############html
        if LogSwitch == 'True':
            if not os.path.isfile(logFile):
                with open(logFile, 'a', encoding='utf-8') as log:
                    log.write('<head><style type="text/css">.div1{margin-left:40px;}</style></head>')
                    log.close()
            with open(logFile, 'a', encoding='utf-8') as log:
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

if __name__ == '__main__':
    ############## 获取配置文件，初始化配置文件 ##############
    configFile = 'BlackBox.config'
    logFile = time.strftime("%Y%m%d.html", time.localtime(time.time()))
    if not os.path.isfile(configFile):
        with open(configFile, 'w', encoding='utf-8') as f:
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
    sessions = {}
    LogSwitch = 'False'
    with open(configFile, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('Log'):
                LogSwitch = line.partition('=')[2].strip()
            elif line.startswith('proxy'):
                proxy1 = line.partition('=')[2].strip()
            elif line.startswith('session'):
                sessions[line.partition('=')[0].strip()] = line.partition('=')[2].strip()
            elif line.startswith('delete_req_header'):
                delete_req_header1 = line.partition('=')[2].strip()
            elif line.startswith('cherk_res_header'):
                check_res_header1 = line.partition('=')[2].strip()
        f.close()
    ############## PyQt5 ##############
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

