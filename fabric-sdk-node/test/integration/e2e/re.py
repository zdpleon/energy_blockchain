import os
import sys
 
old_file ='/home/leon/workspace/src/github.com/hyperledger/fabric/fabric-sdk-node/test/integration/e2epy/config.json'
f =open(old_file,'r+')

flist=f.readlines()
flist[45]='	         "a"\n'
flist[46]='	         "a"\n'
flist[47]='	         "100"\n'
f=open(old_file,'w+')
f.writelines(flist)