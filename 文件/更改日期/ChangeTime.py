#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os, sys
import time
while True:
    try:
        file = input('file:')
        stinfo = os.stat(file)
        #print(stinfo)
        print("修改时间: %s" % time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(stinfo.st_mtime)))

        xgsj = input('"修改时间"改为:')   #2023/10/06 23:54:10
        xgsj = int(time.mktime(time.strptime(xgsj, "%Y/%m/%d %H:%M:%S")))

        os.utime(file, (stinfo.st_atime, xgsj))
    except:
        pass

