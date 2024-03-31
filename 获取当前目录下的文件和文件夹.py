import os


def get_files(path):        #不会看子目录
    dirs = []
    files = []
    for i in os.scandir(path):
        if i.is_dir():
            dirs.append(i.path)
        elif i.is_file():
            files.append(i.path)
    return dirs, files
dirs, files=get_files(r'C:\Users\Abs1nThe\Desktop\02-ActiveMQ')
print(dirs)
print(files)