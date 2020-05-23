# -*- coding: utf-8 -*-
# For Windows OS Only....

import sys
import os

def main(argv):

    if len(argv)<2 or argv[1]=='':
        print ("Usage: "+argv[0][argv[0].rfind("\\")+1:]+" <OMV file\> [output\]")
        return False
    elif len(argv)>2 and arfv[2]:
        ogvFN=argv[2]
    else:
        ogvFN=argv[1].replace('.omv','.ogv')
    omvFN=argv[1]
    try:
        omv=open(omvFN,'rb')
        data=omv.read()
        offset=data.index(b'OggS')
        omv.close()
    except:
        print("Input file error!")
        return False
    ogv=open(ogvFN,'wb')
    ogv.write(data[offset:])
    ogv.close()
    
    return True

if __name__=="__main__":
    main(sys.argv)
