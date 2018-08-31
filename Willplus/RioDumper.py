# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
import struct
import codecs
import unicodedata

if len(sys.argv) < 2:
    print ("error\n")
    print (sys.argv[0]+" <script\> <script_ex\>")
    quit()

IN=sys.argv[1]
OUT=sys.argv[2]

INFile=open(IN,'rb')    #脚本文件
OUTFile=open(OUT,'w',1,'utf-16')  #输出文件
RN="\n"   #换行
INFile.seek(0)
temp=INFile.read(1)
count=0
lastCount=-1
while temp:
    if temp==b'\x00':
        check=INFile.read(1)
        if not check:   # 文件结尾中断
            break
        if (check==b'\x41' or check==b'\x42'):   # 文本开头0041/0042
            OUTTemp=b""  #重置写入文本
            #INFile.seek(-4,1)
            countTemp=INFile.read(2)
            count=struct.unpack('H',countTemp)[0]   #读入行号
            #INFile.seek(2,1)    #重定位指针
            if count==lastCount+1:  #通过行号判断文本开头真伪
                #nameCheck=INFile.read(1)    #检查是否为对话
                #if nameCheck==chr(0):
                    #continue
                if check==b'\x42':   #是对话：读入人名
                    INFile.seek(3,1)
                    hasName=True
                    name=b""
                    nameUTF=""
                    nameTemp=INFile.read(1)
                    while not nameTemp==b'\x00':
                        name=name+nameTemp
                        nameTemp=INFile.read(1)
                    nameUTF=name.decode("Shift-JIS")
                else:   #不是对话
                    hasName=False
                    INFile.seek(2,1)   #定位指针
                text=b"" #重置临时文本
                textEnd=False
                while not textEnd:  #判断文本结束
                    textTemp=INFile.read(1) #读取下一位
                    if textTemp==b'\x25':
                        textCheck=INFile.read(1)
                        if textCheck==b'\x4b':
                            textEnd=True    #结束符号254b
                        else:
                            INFile.seek(-1,1)   #重定位指针
                    if not textEnd:
                        text=text+textTemp  #写入text
                textUTF=text.decode("Shift-JIS")
                if hasName:
                    namePart=u'▷'+nameUTF+u'◁' #有人名
                    Apart=u'◇'+'%.6d'%count+u'◇'    #原文行开头
                    Bpart=u'◆'+'%.6d'%count+u'◆'    #译文行开头
                else:
                    namePart="" #无人名
                    Apart=u'○'+'%.6d'%count+u'○'    #原文行开头
                    Bpart=u'●'+'%.6d'%count+u'●'    #译文行开头
                OUTTemp=Apart+namePart+textUTF+RN+Bpart+namePart+textUTF+RN+RN
                OUTFile.write(OUTTemp)  #写入文件
                lastCount=count #记录行号
            else:
                INFile.seek(-3,1)
        else:   #非文本开头
            INFile.seek(-1,1)   #重定位指针
    temp=INFile.read(1) #读取下一位

INFile.close()
OUTFile.close()
print("Finished!")
