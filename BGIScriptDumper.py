# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
import struct
import codecs
import unicodedata

if len(sys.argv) < 2:
    print ("error\n")
    print (sys.argv[0]+" <script\>")
    quit()

SC=sys.argv[1]
EX=sys.argv[1]+".txt"

try:
    SCFile=open(SC, 'rb')
except FileNotFoundError:
    print(SC+" Error!\tCan't find file!")
    exit()
except:
    print("Error!")
    exit()

SCFile.seek(0)
test=SCFile.read(20)
if not test==b'BurikoCompiledScript':
    print(SC+" Error!\tNot a script file!")
    exit()

test=SCFile.read(4)
while not test==b'\x01\x00\x00\x00':
    test=SCFile.read(4)
SCFile.seek(-4,1)
offset=SCFile.tell()


while not test==b'\x03\x00\x00\x00':
    test=SCFile.read(4)
locate=struct.unpack('L',SCFile.read(4))[0]
SCFile.seek(locate+offset)
textInFile=SCFile.read()
SCFile.seek(offset)
TXFile=open(EX,'w',1,"UTF_16")
textOffset=locate
end=locate+offset
#while SCFile.tell()<os.path.getsize(SC):
while SCFile.tell()<end:
    test=SCFile.read(4)
    if test==b'\x03\x00\x00\x00':
        address=SCFile.tell()
        locate=struct.unpack('L',SCFile.read(4))[0]
        textLocate=locate-textOffset
        text=textInFile[textLocate:textInFile.find(b'\x00',textLocate)]
        try:
            text.decode('Shift-JIS')
        except:
            text=b''
            textUTF=u""
        else:
            textUTF=text.decode('Shift-JIS')
            if unicodedata.east_asian_width(textUTF[0])!='Na':
                TXTemp=u'○'+'%.6d'%address+u'○'+textUTF+u'\n●'+'%.6d'%address+u'●'+textUTF+u'\n\n'
                TXFile.write(TXTemp)
            



#SCFile.seek(locate+offset)
#temp=SCFile.read(1)
#while not temp==b"":
    #if temp==b'\x00':
        #temp=b'\r\n'
    #TXFile.write(temp)
    #temp=SCFile.read(1)
    
SCFile.close()
TXFile.close()
print ("Finished!")

