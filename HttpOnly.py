import json
import sys
import requests
import urllib3
urllib3.disable_warnings()
proxies={'http': 'http://127.0.0.1:8080','https': 'http://127.0.0.1:8080'}
def str_to_json(str,cutLine,cutStr):
    dict1={}
    for i in str.split(cutLine):
        dict1[i.partition(cutStr)[0].strip()]=i.partition(cutStr)[2].strip()
    return dict(filter(lambda x: x[0]!='',dict1.items())) #删除空key

def json_to_str(dict,cutLine,cutStr):
    return cutLine.join([key+cutStr+value for key,value in dict.items()])
def GetRequest(req): #从字符串获取请求内容
    method= req.partition(' ')[0].strip().lower()
    path=   req.partition(' ')[2].partition(' ')[0].strip()
    host=   req.partition('\n')[2].partition('\n')[0].partition(':')[2].strip()
    headers=req.partition('\n')[2].partition('\n')[2].partition('\n\n')[0].strip()
    dict_headers = str_to_json(headers,'\n',':')
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

if __name__ == '__main__':
    with open('req.txt', 'r', encoding='utf-8') as f:
        iferror,method,path,host,headers,dict_headers,isjson,body=GetRequest(f.read())
        f.close()



    dict_Cookie=str_to_json(dict_headers['Cookie'],';','=')

    temp=dict_Cookie.copy()
    for key in dict_Cookie.keys():
        temptemp=temp.copy() #用于恢复
        temp.pop(key)
        newCookie=json_to_str(temp,'; ','=')
        # print('删除', key,newCookie)
        dict_headers['Cookie']=newCookie
        try:
            url, res = GetResponse('http', method, path, host, dict_headers, isjson, body)
        except:
            print('error')
            sys.exit()
        if res.status_code != 200:
            temp=temptemp.copy()
    #print(newCookie)
    print('以下cookie需要配置HttpOnly&Secure:')
    print(','.join(str_to_json(newCookie,';','=').keys()))


