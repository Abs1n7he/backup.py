import os
import shutil
import stat
from colorama import init
init(autoreset=True)
import hashlib



#黑名单
blacklist1=["desktop.ini"]
blacklist2=[".pyc"]
 
def getAllFiles(path): #获取全部文件
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
    root=r'E:\lsp\视频'
    files = getAllFiles(root)
    
    md5s={}

    for of in files:
        file = os.path.join(root, of.strip('\\'))
        with open(file,"rb") as f:
            fileMd5=hashlib.md5(f.read()).hexdigest()
            if fileMd5 not in md5s.keys():
                md5s[fileMd5]=[file]
            else:
                md5s[fileMd5].append(file)
            f.close()
    for key,value in md5s.items():
        if len(value) != 1:
            print('\n'.join(value) , end='\n\n')
    
    # for file in deleteFiles:
    #     try:
    #         os.remove(file)
    #     except:
    #         os.chmod(file,stat.S_IWRITE)#取消只读权限
    #         os.remove(file)

