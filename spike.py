# 码率(kbps)=文件大小(KB) * 8 / 时间(秒)
# !/usr/bin/python3.4
# -*- coding: utf-8 -*-

import os


# 字节bytes转化kb\m\g
def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)


# 获取文件大小
def getDocSize(path):
    try:
        size = os.path.getsize(path)
        return formatSize(size)
    except Exception as err:
        print(err)


# 获取文件夹大小
def getFileSize(path):
    sumsize = 0
    try:
        filename = os.walk(path)
        for root, dirs, files in filename:
            for fle in files:
                size = os.path.getsize(path + fle)
                sumsize += size
        return formatSize(sumsize)
    except Exception as err:
        print(err)

size=float(getDocSize("./static/uploads/temp/jhgs.mp4")[:-1])*1024*1024
print(size)
from moviepy.editor import VideoFileClip

clip = VideoFileClip("./static/uploads/temp/jhgs.mp4")
print( clip.duration ) # seconds

malv = size*8/clip.duration/1000
print("视频码率为："+str(malv)+"kbps")