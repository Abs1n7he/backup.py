import json
import sys
import requests
import urllib3
urllib3.disable_warnings()

from my_requests import *



if __name__ == '__main__':
    proxies = {}
    #proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
    txt='req.txt'
    http = 'https'


    with open(txt, 'r', encoding='utf-8') as f:
        iferror,method,path,host,url,headers,dict_headers,isjson,body=GetRequest(http,f.read())
        f.close()
    dict_Cookie=str_to_cookie(dict_headers['Cookie'])
    temp=dict_Cookie.copy()
    for key in dict_Cookie.keys():
        temptemp=temp.copy() #用于恢复
        temp.pop(key)
        newCookie=cookie_to_str(temp)
        # print('删除', key,newCookie)
        dict_headers['Cookie']=newCookie
        try:
            res = GetResponse(method,url, dict_headers, isjson, body, proxies)
        except:
            print('error')
            sys.exit()
        ############## 检查项 ################
        if res.status_code != 200:              # 通过响应码200检查
        # if json.loads(res.text)['errno']!=0:    # 通过json响应体检查
        # if res.reason!='OK'
            temp=temptemp.copy()
        else:
            lastReq = res
        print()



    print('以下cookie需要配置HttpOnly&Secure:')
    print(lastReq.request.headers['Cookie'])
    print(','.join(str_to_cookie(newCookie).keys()))



