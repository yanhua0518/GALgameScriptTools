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

INFile=open(IN, 'rb')
OUTFile=open(OUT, 'wb')

temp=INFile.read(1)
while not temp==b'':
    #A=ord(temp)
    A=struct.unpack('B',temp)[0]
    B=(((A<<2)|16128)^16128)|(A>>6)
    #write=chr(B)
    write=struct.pack('B',B)
    OUTFile.write(write)
    temp=INFile.read(1)

INFile.close()
OUTFile.close()
print ("Finished!")
