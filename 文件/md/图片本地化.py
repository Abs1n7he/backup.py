import re
import requests
import os




file = r'C:\Users\Abs1nThe\Desktop\新建文件夹\CSV.md'



def updateMD(file, dict1):  # 以字典形式替换
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            for keys, vules in dict1.items():
                if keys in line:
                    line = line.replace(keys, vules)
            file_data += line
        f.close()
    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)
        f.close()

file = os.path.normcase(file)  # 路径用单反斜线
with open(file, 'r', encoding='utf-8') as f:
    flag = False
    mdupdate = {}
    for line in f:
        line = line.strip()  # 过滤杂质
        if re.findall('!\[(.*?)\]\(http', line):
            temp = re.findall(re.compile(r'\((?:[^()]+|\((?:[^()]+|\([^()]*\))*\))*\)', re.S), line)
            flag = True
        elif re.findall('<img(.*?)src(.*?)http(.*?)>', line):
            temp = re.findall(re.compile(r'[\'"](.*?)[\'"]', re.S), line)
            flag = True
        if flag:
            for x in temp:
                i = x.strip('()')          # /resource/(CVE-2017-15715)Apache解析漏洞/media/rId24.png
                mdupdate[i] = 'img/' + i.split('/')[-1]
        flag = False
    f.close()


updateMD(file, mdupdate)


imgdir=os.path.join(os.path.split(os.path.realpath(file))[0], 'img')
if not os.path.exists(imgdir):
   os.makedirs(imgdir)#创建目录
os.chdir(imgdir) #设置目录为img目录

for keys in mdupdate:     #下载图片
   myfile = requests.get(keys)
   open(keys.split('/')[-1], 'wb').write(myfile.content)