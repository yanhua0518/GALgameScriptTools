# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os
from ctypes import *
import struct


# Change this key to your game's key.
DEFAULT_KEY=[0x2E, 0x4B, 0xDD, 0x2A, 0x7B, 0xB0, 0x0A, 0xBA,
             0xF8, 0x1A, 0xF9, 0x61, 0xB0, 0x18, 0x98, 0x5C]

def Decrypt(string,l,k):
    key=28807
    localKey=key*k%65536
    newString=b''
    for n in range(0,l):
        newString+=struct.pack('H',localKey^struct.unpack('H',string[n*2:n*2+2])[0])
    return newString

def Decrypt1(string,key):
    if not key:
        key=DEFAULT_KEY
    size=len(string)
    keyBuf=c_char_p(struct.pack('16B',*key))
    newString=string
    dll.decrypt1(newString,size,keyBuf)
    return newString

def Decrypt2(string):
    size=len(string)
    newString=string
    dll.decrypt2(newString,size,0)
    return newString

def Decrypt3(string):
    size=len(string)
    newString=string
    dll.decrypt3(newString,size)
    return newString

def Decrypt4(string):
    size=len(string)
    newString=string
    dll.decrypt2(newString,size,1)
    return newString

def Decrypt5(string):
    key=[0x2D, 0x62, 0xF4, 0x89, 0x2D, 0x62, 0xF4, 0x89,
         0x2D, 0x62, 0xF4, 0x89, 0x2D, 0x62, 0xF4, 0x89]
    size=len(string)
    keyBuf=c_char_p(struct.pack('16B',*key))
    newString=string
    dll.decrypt1(newString,size,keyBuf)
    return newString

def Decompress(string,size):
    newString=bytes(size)
    dll.decompress(string,newString,size)
    return newString

def FakeCompress(string):
    ssSize=len(string)
    dataSize=ssSize+int(ssSize/8)+8
    if not ssSize%8==0:
        dataSize+=1
    newString=struct.pack('2I',dataSize,ssSize)+bytes(dataSize-8)
    dll.fakeCompress(string,newString,ssSize)
    return newString

def Compress(string,level):
    length=len(string)
    size=c_int(0)
    p=dll.compress(string,length,pointer(size),level)
    newString=string_at(p,size)
    return newString

try:
    dll=CDLL(os.getcwd()+'\\Decryption.dll')
except:
    print("Can't open Decryption.dll")
    quit()

