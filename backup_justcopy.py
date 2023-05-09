import os
import shutil
from colorama import init
init(autoreset=True)

#黑名单
blacklist1=["desktop.ini"]
blacklist2=[".pyc"]
 
def getAllFiles(path):
    file_list=[]
    for root,dirs,fs in os.walk(path):
        for f in fs:
            if f not in blacklist1 and os.path.splitext(f)[1] not in blacklist2:
                f_fullpath = os.path.join(root, f)
                f_relativepath = f_fullpath[len(path):]
                file_list.append(f_relativepath)
    return file_list
 
def dirCompare(raw_root,backup_root):
    raw_files = getAllFiles(raw_root)
    backup_files = getAllFiles(backup_root)
 
    setA = set(raw_files)
    setB = set(backup_files)
 
    commonfiles = setA & setB

    for of in sorted(commonfiles):
        if os.stat(raw_root+'\\'+of).st_mtime != os.stat(backup_root+'\\'+of).st_mtime:
            shutil.copy2(raw_root + of, backup_root + of)
 
    
    onlyFiles = setA ^ setB

    onlyIn_Raw = []
    onlyIn_backup = []
    for of in onlyFiles:
        if of in raw_files:
            onlyIn_Raw.append(of)
        elif of in backup_files:
            onlyIn_backup.append(of)
            
    if len(onlyIn_Raw) > 0:
        print('\033[1;32m--------------------- copy ---------------------\033[0m')
        for of in sorted(onlyIn_Raw):
            print('\033[1;32m%s\033[0m' % (backup_root + of))
            if not os.path.exists(os.path.dirname(backup_root + of)):
                os.makedirs(os.path.dirname(backup_root + of))
            shutil.copy2(raw_root + of, backup_root + of)
            
    if len(onlyIn_backup) > 0:
        print('\033[1;31m--------------------- more ---------------------\033[0m')
        for of in sorted(onlyIn_backup):
            print('\033[1;31m%s\033[0m' % (backup_root + of))
            


            
if __name__ == '__main__':
    raw_root = input('源文件目录:')
    backup_root = input('备份目录:')
    dirCompare(raw_root, backup_root)
    print("\ndone!")