import os
import shutil
import stat
from colorama import init
init(autoreset=True)


#保留共有部分，其他删除
#在没有新增文件的情况下，删除单方面被删除的文件


#黑名单
blacklist1=["desktop.ini"]
blacklist2=[".pyc"]
 
def getAllFiles(path): #获取全部文件，就这样吧，因为要对比文件修改日期
    file_list=[]
    for root,dirs,files in os.walk(path):
        for f in files:
            if f not in blacklist1 and os.path.splitext(f)[1] not in blacklist2:#文件名不在黑名单、扩展名不在黑名单
                #f为文件名（1.docx）
                f_fullpath = os.path.join(root, f)
                #f_fullpath 为完整路径（D:\work\tool\Project\备份文件\1\1.docx）
                f_relativepath = f_fullpath[len(path):]
                #f_relativepath 为完整路径取掉对比目录（\1\1.docx）
                file_list.append(f_relativepath)
                #写入列表
    return file_list

def deleteFile(files,root,of):
    deleteList=[]
    for of in sorted(files): #遍历列表删除
        print('\033[1;32m%s\033[0m' % (root + of))
        deleteList.append(root + of)
    Doit=input("Do it?(Y/N):")
    if Doit=='Y' or Doit=='y':
        for i in deleteList:
            try:
                os.remove(i)
            except:
                os.chmod(i,stat.S_IWRITE)#取消只读权限
                os.remove(i)

def dirCompare(raw_root,backup_root):
    raw_files = getAllFiles(raw_root)
    backup_files = getAllFiles(backup_root)
 
    setA = set(raw_files)#去重？
    setB = set(backup_files)
 


    onlyFiles = setA ^ setB #仅出现在其中一个目录中的文件
    onlyIn_Raw = []
    onlyIn_backup = []
    for of in onlyFiles:
        if of in raw_files:   #如果这个文件在源文件，添加到列表
            onlyIn_Raw.append(of)
        elif of in backup_files:
            onlyIn_backup.append(of)


    print('\033[1;32m--------------------- remove ---------------------\033[0m')
    if len(onlyIn_Raw) > 0:
        deleteFile(onlyIn_Raw,raw_root,of)
    if len(onlyIn_backup) > 0:
        deleteFile(onlyIn_backup,backup_root,of)


def Emptyfolder(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):  # 检查文件夹是否为空
                try:
                    os.rmdir(dir_path)  # 删除空文件夹
                except:
                    os.chmod(dir_path, 0x1F0FF)  # 取消文件夹只读权限
                    os.rmdir(dir_path)


            
if __name__ == '__main__':
    print('\033[1;31m保留共有部分，其他删除。\033[0m')
    print('\033[1;31m在没有新增文件的情况下，删除单方面被删除的文件。\033[0m')

    raw_root = input('目录1:') #对比文件夹
    backup_root = input('目录2:') #参考文件夹
    dirCompare(raw_root, backup_root)
    Emptyfolder(raw_root)
    Emptyfolder(backup_root)
    print("\ndone!")