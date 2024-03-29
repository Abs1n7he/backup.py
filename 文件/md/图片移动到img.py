import re
import sys
import os
import shutil




file = r'C:\Users\Abs1nThe\Desktop\新建文件夹\CSV.md'




def updateMD(file, dict1):  # 以字典形式替换
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            for keys, vules in dict1.items():
                if keys in line:
                    line = line.replace(keys, vules)
            file_data += line
    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)

def Emptyfolder(path):  # 删除空文件夹
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):  # 检查文件夹是否为空
                try:
                    os.rmdir(dir_path)  # 删除空文件夹
                except:
                    os.chmod(dir_path, 0x1F0FF)  # 取消文件夹只读权限
                    os.rmdir(dir_path)


file = os.path.normcase(file)  # 路径用单反斜线
f = open(file, 'r', encoding='utf-8')

mddir = os.path.split(os.path.realpath(file))[0]    # 文件目录  C:\1
imgdir = os.path.join(mddir, 'img')                 # 图片目录  C:\1\img
if not os.path.exists(imgdir):      # 创建图片目录
    os.makedirs(imgdir)
flag = False
mdupdate = {}
for line in f:
    line = line.strip()  # 过滤杂质
    if re.findall('!\[(.*?)\]\((?:[^()]+|\((?:[^()]+|\([^()]*\))*\))*\)', line) and not (re.findall('!\[(.*?)\]\(http', line)):  # 匹配有图片的行，如：![](img/30.jpg) 
        temp = re.findall(re.compile(r'\((?:[^()]+|\((?:[^()]+|\([^()]*\))*\))*\)', re.S), line)
        flag = True
    elif re.findall('<img(.*?)src(.*?)>', line) and not (re.findall('<img(.*?)src(.*?)https(.*?)>', line)):# <img src="img/10.jpg" style="zoom:50%;" />
        temp = re.findall(re.compile(r'[\'"](.*?)[\'"]', re.S), line)
        flag = True
    if flag:
        for x in temp:
            i = x.strip('(.)')          # /resource/(CVE-2017-15715)Apache解析漏洞/media/rId24.png
            i = os.path.normcase(i)     # 路径用单反斜线
            imgFile = os.path.basename(i)                               # rid24.png
            mdPath = os.path.join('img', imgFile).replace('\\', '/')    # img\rid24.png
            #moveOld = mddir + '\\' + i.strip('\/')
            moveOld = i.strip('\/')                      # C:\1\media\rid24.png
            moveNew = os.path.join(imgdir, imgFile)                     # C:\1\img\rid24.png

            try:
                shutil.move(moveOld, moveNew)
                mdupdate[x.strip('()')] = mdPath
            except:
                print('error: ' + line, moveOld, moveNew,end='\n\n')
        flag = False

f.close()
updateMD(file, mdupdate)
Emptyfolder(mddir)
