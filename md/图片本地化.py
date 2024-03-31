import re
import shutil
import random
import stat
import string
import sys
import time
import urllib

import filetype
import requests
import os
from colorama import init
init(autoreset=True)


def get_files(path):
    files = []
    for i in os.scandir(path):
        if i.is_file():
            files.append(i.path)
    return files
def saveLog(txt,Logfile):
    with open(Logfile, 'a', encoding='utf-8') as log:
        log.write(txt)
        log.close()
def GetLinkFromMd(file):
    saveLog('\n【★】'+file+'\n', Logfile)
    if not os.path.isfile(file):
        print('\033[1;31m[error]\033[0m 文件不存在 "%s"' % file)
        sys.exit()
    file = os.path.normcase(file)  # 路径用单反斜线
    dict1 = {}
    with open(file, 'r', encoding='utf-8') as f: #GB2312 utf-8
        for line in f:
            line = line.strip()  # 过滤杂质
            if re.findall('!\[(.*?)\]\((?:.*)\)', line):  # 因为文件名里可以有()，所以贪心匹配可能匹配到二位一体,所以下面用![分割
                # print('line:',line,line.count('!['))
                list1 = list(filter(None, line.split('![')))
                # print('list:',*list1)
                for i in list1:
                    if re.findall('\]\((?:.*)\)', i):
                        temp = re.findall(re.compile(r'\]\((.*?)\.(png|jpg|jpeg|bmp|svg|tiff|webp|gif)(\s*)\)', re.S),i)
                        if temp != []:
                            link = (temp[0][0] + '.' + temp[0][1]).strip()
                        else:
                            temp = re.findall(re.compile(r'\]\(\S*\)', re.S), i)[0]
                            link = temp[2:len(temp) - 1]
                        while True:             #重复的value要改掉,所以直接用了随机数
                            Random = ''.join(random.choice(string.ascii_uppercase) for _ in range(6))
                            if Random not in dict1.values():
                                dict1[link.strip('./').strip('.\\').strip('/').strip('\\')] = Random+os.path.splitext(link)[1] #随机数+扩展名
                                break
            if re.findall('<img(.+)>', line):
                line = line[line.index('<img'):]
                list1 = list(filter(lambda x:'<img' not in x and x.strip(), re.split('\ssrc(\s*)=', line)))
                for i in list1:
                    i = i.strip()
                    link = i[1:i[1:].index(i[0]) + 1]
                    while True:
                        Random = ''.join(random.choice(string.ascii_uppercase) for _ in range(6))
                        if Random not in dict1.values():
                            dict1[link.strip('./').strip('.\\').strip('/').strip('\\')] = Random + os.path.splitext(link)[1]  # 随机数+扩展名
                            break
        f.close()
    dict1 = dict(filter(lambda x: x[0] != '', dict1.items()))

    return dict1

def downloadOrMoveImg(imgDir, dict1):
    log='************** 下载&移动 **************'
    print('\033[5;37m************** 下载&移动 **************\033[0m')
    if not os.path.exists(imgPath):  # 创建目录
        os.makedirs(imgPath)
    os.chdir(mdPath)    # 设置工作目录为md的目录
    listNoChange=[]        # 不需要更改md
    listChangeNoMove=[]
    listDownload={}
    for key, value in dict1.items():  # 需要下载图片
        if key.lower().startswith('http'):
            listDownload[key]=value
        else:
            if os.path.normcase(os.path.split(os.path.abspath(key))[0])==os.path.normcase(imgPath): #图片不需要移动
                if key.startswith(imgDir):
                    listNoChange.append(key)
                    log += '\n[info] 相对路径，不需要移动，不需要改md：'+key
                    print('\033[1;32m[info]\033[0m 相对路径，不需要移动，不需要改md：', key)
                else:
                    listChangeNoMove.append(key)
                    dict1[key] = os.path.basename(key)
                    log += '\n[info] 绝对路径，不需要移动，但需要改md：'+key
                    print('\033[1;32m[info]\033[0m 绝对路径，不需要移动，但需要改md：',key)
            else:
                try:# 移动图片
                    newfile = os.path.join(imgPath, value)
                    TempKey     = os.path.normcase(key)                                     #########奇葩，全改成小写了？
                    newfile = os.path.normcase(newfile)

                    log += '\n[info] 移动 "%s" 到 "%s"'% (os.path.abspath(TempKey), newfile)
                    print('\033[1;32m[info]\033[0m 移动 "%s" 到 "%s"' % (os.path.abspath(TempKey), newfile))
                    if TempKey!=newfile:
                        shutil.move(TempKey, newfile)
                except:
                    log += '\n[error] 文件不存在 '+key
                    print('\033[1;31m[error]\033[0m 文件不存在 "%s"' % key)
                    listNoChange.append(key)
    ############ 设置图片目录、下载 ############
    os.chdir(imgPath)
    for key,value in listDownload.items():
        myfile = requests.get(key)
        open(value, 'wb').write(myfile.content)
        imgDownloadPath=os.path.join(imgPath, value)
        log += '\n[info] 下载 "%s" 到 "%s"' % (key, imgDownloadPath)
        print('\033[1;32m[info]\033[0m 下载 "%s" 到 "%s"' % (key, imgDownloadPath))
        if not re.findall(r'.\.(png|jpg|jpeg|bmp|svg|tiff|webp|gif)$',value):
            kind = filetype.guess(imgDownloadPath)
            if kind is None:
                log +='\n[error] 格式未知 "%s" "%s"' % (key, imgDownloadPath)
                print('\033[1;31m[error]\033[0m 格式未知 "%s" "%s"' % (key, imgDownloadPath))
            else:
                type=kind.extension
                if not value.endswith('.'+type):
                    dict1[key]=value+'.'+type
                    os.rename(imgDownloadPath,imgDownloadPath+'.'+type)


    ############ 删掉报错的图片，md中不更改 ############
    for i in listNoChange:
        dict1.pop(i)
    saveLog(log, Logfile)

def updateMD(file, dict1,newDir):  # 以字典形式替换
    log = '\n************** 更新MD **************'
    print('\033[5;37m************** 更新MD **************\033[0m')
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            for keys, vules in dict1.items():
                if keys in line:
                    line = line.replace(keys, newDir+'/'+vules)
                    log+='\n[info] "%s" 替换为 "%s"' % (keys,newDir+'/'+vules)
                    print('\033[1;32m[info]\033[0m "%s" 替换为 "%s"' % (keys,newDir+'/'+vules))
            file_data += line
        f.close()
    with open(file, "w", encoding="utf-8") as f:
        f.write(file_data)
        f.close()
    log += '\nDone!\n'
    print('Done!')
    saveLog(log, Logfile)

def deleteMdAndImg(file,dict1):
    log ='\n************** 删除 **************'
    for i in dict1.keys():
        if not i.lower().startswith('http'):
            delfile=os.path.normcase(os.path.join(mdPath, i))
            if os.path.isfile(delfile):
                try:
                    os.remove(delfile)
                    log+='\n[info] 已删除：'+delfile
                    print('\033[1;32m[info]\033[0m 已删除：', delfile)
                except:
                    os.chmod(delfile, stat.S_IWRITE)  # 取消只读权限 or os.chmod(delfile, 0x1F0FF)
                    os.remove(delfile)
            else:
                log += '\n[error] 文件不存在 "%s"' % delfile
                print('\033[1;31m[error]\033[0m 文件不存在 "%s"' % delfile)
    try:
        os.remove(file)
        log += '\n[info] 已删除：%s\n' % file
        print('\033[1;32m[info]\033[0m 已删除：', file)
    except:
        os.chmod(file, stat.S_IWRITE)  # 取消只读权限
        os.remove(file)
    saveLog(log, Logfile)

if __name__ == '__main__':
    Logfile=os.path.join(os.getcwd(), time.strftime("%Y%m%d.log", time.localtime(time.time())))     #日志文件
    imgDir = 'img'  #图片目录

    use=2           #方法：1 or 2
    mode='delete'   #模式：update or delete

    if mode=='delete':
        if input('删除模式!请确认(y/Y):').lower() != 'y':
            sys.exit()
    if use==2:
        print('输入目录，处理仅该目录下的md')
        try:
            path = input('path:')
        except:
            sys.exit()
    if use==1:
        ################## 用法1：连续输入md文件 ##################
        print('连续输入md文件')
        while True:
            try:
                file = input('file:').replace('\\','\\\\')
                mdPath = os.path.dirname(file)          #md的目录
                imgPath = os.path.join(mdPath, imgDir)  #md下的img
                dict1=GetLinkFromMd(file)
                #print(dict1)

                if mode=='update' and dict1:        #下载、移动图片、更新md
                    downloadOrMoveImg(imgDir, dict1)
                    updateMD(file, dict1,imgDir)
                elif mode=='delete':
                    deleteMdAndImg(file,dict1)      #删除md和图片
            except:pass
    elif use==2:
        ################## 用法2：输入目录，处理仅该目录下的md ##################
        files=get_files(path)
        mdPath = path.strip('/').strip('\\')
        imgPath = os.path.join(mdPath, imgDir)  #md下的img
        dictDelete={}
        for file in files:
            if os.path.splitext(file)[1] =='.md':
                dict1=GetLinkFromMd(file)
                if mode=='update' and dict1:         #下载、移动图片、更新md
                    downloadOrMoveImg(imgDir, dict1)
                    updateMD(file, dict1,imgDir)

                dictDelete[file]=dict1
        if mode == 'delete':
            for file,dict1 in dictDelete.items():
                deleteMdAndImg(file,dict1)          #删除md和图片








