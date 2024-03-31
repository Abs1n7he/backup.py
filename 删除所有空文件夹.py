import os

def Emptyfolder(path): #删除空文件夹
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):  # 检查文件夹是否为空
                print('[DEl] ',dir_path)
                try:
                    os.rmdir(dir_path)  # 删除
                except:
                    os.chmod(dir_path, 0x1F0FF)  # 取消文件夹只读权限
                    os.rmdir(dir_path)
Emptyfolder(r'C:\Users\Abs1nThe\Desktop\新建文件夹')

