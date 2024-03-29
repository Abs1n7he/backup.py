import os
i = 1

# thedir = input('目录:')
# name = input('前缀:')








thedir = r'E:\Download\ANi'
name = ''    #前缀

for root,dirs,files in os.walk(thedir):
    #files.sort(key=lambda x:int(x.split('.')[0]))                # 1.jpg 排序后重命名 、为防止出现1、10、2、20，这种排序
    #files.sort(key=lambda x:int(x.split('(')[-1].split(')')[0]))  # x(1).jpg 排序后重命名


    for f in files:
        
        #newname = f+".7z" #加后缀
        newname = name+"{:0>2d}".format(i)+os.path.splitext(f)[1]  #重命名为name_01.jpg

        print("%s\t改为 %s" %(f,newname))

        os.rename(os.path.join(root, f),os.path.join(root, newname)) #建议确认后再开启

        i=i+1

