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
        try:
            ch.encode("GBK")
        except:
            tran+=u"·"
        else:
            tran+=ch
    return tran.encode("GBK")



if len(sys.argv) < 2:
    print ("error\n")
    print (sys.argv[0]+" <script\> <txt\> <script_cn\>")
    quit()

SC=sys.argv[1]
TX=sys.argv[2]
CN=sys.argv[3]

try:
    SCFile=open(SC,'rb')
except FileNotFoundError:
    print(SC+" Error!\tCan't find file!")
    exit()
except:
    print("Error!")
    exit()
try:
    TXFile=open(TX,'r',1,'UTF-16')
except FileNotFoundError:
    print(TX+" Error!\tCan't find file!")
    exit()
except:
    print("Error!")
    exit()


SCFile.seek(0)
test=SCFile.read(20)
if not test==b'BurikoCompiledScript':
    print(SC+" Error!\tNot a script file!")
    exit()
    
SCFile.seek(0)
test=SCFile.read(4)
while not test==b'\x01\x00\x00\x00':
    test=SCFile.read(4)
SCFile.seek(-4,1)
offset=SCFile.tell()

SCFile.seek(0)
CNFile=open(CN,'wb')
CNFile.write(SCFile.read())
SCFile.close()
newOffset=CNFile.tell()

textToFile=b""
for line in TXFile.readlines():
    TXTemp=line
    if TXTemp=="":
        break
    if TXTemp[0]==u'●':
        text=TXTemp[8:-1]
        textGBK=transcode(text)+b'\x00'
        address=int(TXTemp[1:7])
        if textToFile.find(textGBK)>=0:
            locate=textToFile.find(textGBK)+newOffset-offset
        else:
            locate=len(textToFile)+newOffset-offset
            textToFile=textToFile+textGBK
        CNFile.seek(address)
        CNFile.write(struct.pack('L',locate))

CNTemp=textToFile
CNFile.seek(newOffset)
CNFile.write(CNTemp)

CNFile.close()
TXFile.close()
print ("Finished!")

