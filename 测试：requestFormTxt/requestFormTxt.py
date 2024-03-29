import json
import sys
import requests
import urllib3
urllib3.disable_warnings()
from my_requests import *



if __name__ == '__main__':
    #proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
    proxies = {}

    txt='req.txt'
    http='http'


    with open(txt, 'r', encoding='utf-8') as f:
        iferror,method,path,host,url,headers,dict_headers,isjson,body=GetRequest(http,f.read())
        f.close()
    if iferror == False:
        print('txt解析错误，' + method)
    else:
        res = GetResponse(method,url, dict_headers, isjson, body, proxies)
        print(res.status_code)
        print(res.reason)
        print(res.text)






