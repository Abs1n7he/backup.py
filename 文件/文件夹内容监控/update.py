import os
import shutil
import stat
import time
from colorama import init
init(autoreset=True)

#黑名单
blacklist1=["desktop.ini"]
blacklist2=[".pyc"]
 
def getAllFiles(path): #获取全部文件，就这样吧，因为要对比文件修改日期
    file_list=[]
    for root,dirs,fs in os.walk(path):
        for f in fs:
            if f not in blacklist1 and os.path.splitext(f)[1] not in blacklist2:#文件名不在黑名单、扩展名不在黑名单
                #f为文件名（1.docx）
                f_fullpath = os.path.join(root, f)
                #f_fullpath 为完整路径（D:\work\tool\Project\备份文件\1\1.docx）
                f_relativepath = f_fullpath[len(path):]
                #f_relativepath 为完整路径取掉对比目录（\1\1.docx）
                file_list.append(f_relativepath)
                #写入列表
    return file_list
 

def update(dir1):
    files1 = getAllFiles(dir1)
    while True:
        files2 = getAllFiles(dir1)

        setA = set(files1)
        setB = set(files2)

        onlyFiles = setA ^ setB #仅出现在其中一个目录中的文件

        onlyIn_files1 = []
        onlyIn_files2 = []
        for of in onlyFiles:
            if of in files1:   #如果这个文件在源文件，添加到列表
                onlyIn_files1.append(of)
            elif of in files2:
                onlyIn_files2.append(of)

        if len(onlyIn_files1) > 0:
            for of in sorted(onlyIn_files1): #遍历列表，复制到备份文件夹
                print('\033[1;31mDEL:%s\033[0m' % (dir1 + of))

                
        if len(onlyIn_files2) > 0:
            for of in sorted(onlyIn_files2): #遍历列表删除
                print('\033[1;32mNEW:%s\033[0m' % (dir1 + of))
        files1=files2
        time.sleep(10)


if __name__ == '__main__':
    dir1 = input('目录:')
    update(dir1)


