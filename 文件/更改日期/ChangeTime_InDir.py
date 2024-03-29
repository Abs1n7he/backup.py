#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, sys
import time


thedir = r'C:\Users\Abs1nThe\Downloads\樊宜沛入职材料-OD'
xgsj = r'2024/03/19 16:00:00'





xgsj = int(time.mktime(time.strptime(xgsj, "%Y/%m/%d %H:%M:%S")))
for root,dirs,files in os.walk(thedir):
    for f in files:
        file=os.path.join(root, f)
        stinfo = os.stat(file)
        os.utime(file, (stinfo.st_atime, xgsj))
    break#仅当前文件夹


