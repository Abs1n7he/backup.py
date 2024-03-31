import os
def getAllFiles(path, black_dir):  # 获取全部文件
    black_dir=list(filter(None,black_dir)) #去除空值
    file_list = []
    for root, dirs, files in os.walk(path):  # root,dirs,files 目录、文件夹、文件名(列表)
        if not any(i in root for i in black_dir):  # 排除的目录
            for f in files:  # 每个文件名
                if f not in black_file and os.path.splitext(f)[1] not in black_suffix:  # 文件名、扩展名不在黑名单
                    # f: 1.docx
                    f_fullpath = os.path.join(root, f)  # D:\work\tool\Project\备份文件\1\1.docx
                    file_list.append(f_fullpath[len(path):])  # 相对路径 \1\1.docx
    return file_list

black_file = ["desktop.ini"]    # 文件名黑名单
black_suffix = [".md"]          # 后缀黑名单
black_dir=['']                  #文件夹黑名单
print(getAllFiles(r'C:\Users\Abs1nThe\Desktop\02-ActiveMQ', black_dir))
