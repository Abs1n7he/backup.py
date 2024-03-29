import os
import shutil
import stat
from colorama import init
init(autoreset=True)

with open(r'D:\work\tool\Project\文件\删除：重复文件\del.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip() # 过滤杂质
        if os.path.isdir(line):
            try:
                shutil.rmtree(line)
                print('dir:',line)
            except:
                os.chmod(line,0x1F0FF)#取消文件夹只读权限
                shutil.rmtree(line)
                print('dir:',line)
        elif os.path.isfile(line):
            try:
                os.remove(line)
                print('file:',line)
            except:
                os.chmod(line,stat.S_IWRITE)#取消只读权限
                os.remove(line)
                print('file:',line)


