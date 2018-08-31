# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
import struct
import codecs
import unicodedata

def transcode(uni):
    tran=u""
    for ch in uni:
        #if isinstance(ch, unicode):
        try:
            ch.encode("BIG5")
        except:
            tran+=u"·"
        else:
            if ch==u"　":
                tran+=u" "
            else:
                tran+=ch
    return tran.encode("BIG5")

def getNameEnd(uni):
    num=0
    for ch in uni:
        if ch==u'◁':
            break
        num=num+1
    return num

#自动换行
def checkReturn(txt):
    checkN=0
    while checkN<len(txt)-26:
        checkN=checkN+26
        checkT=txt[checkN]
        if checkT==u"，" or checkT==u"。" or checkT==u"！" or checkT==u"？" or checkT==u"、" or checkT==u"」" or checkT==u"』":
            txt=txt[:checkN-2]+u"\\n"+txt[checkN-2:]
            
    return transcode(txt)

if len(sys.argv) < 3:
    print ("error\n")
    print (sys.argv[0]+" <script\> <script_ex\> <script_pk\>")
    quit()

SC=sys.argv[1]
IN=sys.argv[2]
OUT=sys.argv[3]

SCFile=open(SC,'rb')    #脚本文件
INFile=open(IN,'r',1,"UTF-16")    #文本文件
OUTFile=open(OUT,'wb')  #输出文件
RN="\n"   #换行
SCFile.seek(0)
INFile.seek(0)
SCTemp=SCFile.read(1)
textTemp=u" "
count=0
hasName=False
nextLine=True
stop=False
while SCTemp:
    if nextLine:
        while (textTemp[0]!=u'●' and textTemp[0]!=u'◆'):    #定位译文行
            textTemp=INFile.readline()
            if textTemp==u"":    #文件结尾
                textTemp=u" "
                stop=True
                break
        if not stop:
            correctCount=int(textTemp[1:7])
            if textTemp[0]==u'●':   #无人名
                hasName=False
                name=u""
                nameGBK=b''
                text=textTemp[8:-1]
                textGBK=transcode(text)
            else:   #有人名
                hasName=True
                nameEnd=getNameEnd(textTemp)
                name=textTemp[9:nameEnd]
                nameGBK=transcode(name)
                text=textTemp[nameEnd+1:-1]
            if len(text)>26:
                textGBK=checkReturn(text)
            else:
                textGBK=transcode(text)
            textTemp=u" "
        nextLine=False  #等待下次触发
    OUTFile.write(SCTemp)   #写入已读取部分
    if SCTemp==b'\x00':
        SCCheck=SCFile.read(1)
        if not SCCheck:  #文件结尾中断
            break
        if (SCCheck==b'\x41' or SCCheck==b'\x42'):   # 文本开头0041/0042
            #SCFile.seek(-4,1)
            countTemp=SCFile.read(2)
            count=struct.unpack('H',countTemp)[0]   #读入行号
            #SCFile.seek(2,1)    #重定位指针
            if count==correctCount: #通过行号判断真伪
                #nameCheck=SCFile.read(1)
                #if nameCheck==b'\x00':
                    #SCFile.seek(-2,1)
                    #SCTemp=SCFile.read(1)
                    #continue
                if SCCheck==b'\x42':
                    hadName=True
                else:
                    hadName=False
                if hasName==hadName:    #通过是否有人名判断真伪
                    OUTFile.write(SCCheck)  #写入41/42标示
                    OUTFile.write(countTemp)    #写入行号
                    OUTFile.write(SCFile.read(2))   #写入000f标示
                    if hasName: #有人名
                        #SCFile.seek(-1,1)    #重定位指针
                        OUTFile.write(SCFile.read(1))  #写入0f标示
                        OUTFile.write(nameGBK)  #写入人名
                        OUTFile.write(b'\x00')   #写入人名结尾00
                    
                    OUTFile.write(textGBK)  #写入文本
                    nextLine=True   #触发下次文本读取
                    textEnd=False
                    while not textEnd:  #判断脚本中文本结束
                        endTemp=SCFile.read(1) #读取下一位
                        if endTemp==b'\x25':
                            endCheck=SCFile.read(1)
                            if endCheck==b'\x4b':
                                textEnd=True    #结束符号254b
                            else:
                                SCFile.seek(-1,1)   #重定位指针
                    SCFile.seek(-2,1)   #重定位到25
                else:
                    SCFile.seek(-3,1)
            else:
                SCFile.seek(-3,1)
        else:
            SCFile.seek(-1,1)
    SCTemp=SCFile.read(1)


SCFile.close()
INFile.close()
OUTFile.close()
print("Finished!")
