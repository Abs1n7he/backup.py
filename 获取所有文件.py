import os

for root, dirs, files in os.walk(r'C:\Users\Abs1nThe\Desktop\02-ActiveMQ'):  # root,dirs,files 目录、文件夹、文件名(列表)
    print('root:',root)
    for dir in dirs:
        print('dir:',os.path.join(root, dir))
    for file in files:
        print('file:', os.path.join(root, file))
    print()
