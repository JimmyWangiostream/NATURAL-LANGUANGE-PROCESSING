#!/usr/bin/python
# -*- encoding: UTF-8 -*-

from collections import OrderedDict
from multiprocessing import Pool
import socket
import time

target_host = "140.116.245.151"
target_port = 2001

WSResult = []

def seg(sentence):
    # create socket
    # AF_INET 代表使用標準 IPv4 位址或主機名稱
    # SOCK_STREAM 代表這會是一個 TCP client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client 建立連線
    client.connect((target_host, target_port))
    # 傳送資料給 target
    data = "seg@@" + sentence
    client.send(data.encode("utf-8"))

    # 回收結果信息
    data = bytes()
    while True:
        request = client.recv(8)
        if request:
            data += request
            begin = time.time()
        else:
            break

    # WSResult = []
    response = data
    if (response is not None or response != ''):
        response = response.decode('utf-8').split()
        for resp in response:
            resp = resp.strip()
            resp = resp[0:len(resp) - 1]
            temp = resp.split('(')
            word = temp[0]
            pos = temp[1]
            WSResult.append((word, pos))
    return
    #return WSResult


sentence = "2016/12/13商業大亨川普明年將成為美國總統，不過許多人擔心就任後會有利益衝突。對此，川普在推特貼文表示，就任前將卸下公司所有的職務，使支持者越來越崇拜他。"

token=[]
import re
token=re.split('，|!|:|。|,|、|;|；|「|」',sentence)
emotion=[]
pemotion="正面情緒: "
nemotion="負面情緒: "
people="人: "
event="事: "
when="時: "
place="地: "
thing="物: "
#print(token)
l=0
#
#
check=0
for n in range(0,len(token)):
    if(len(token[n])>0):
        l+=1
        WSResult = []
        seg(token[n])
        #print(WSResult)
    elif n<len(token)-1:
        if(len(token[n])==0):
            continue
    else:
        break
    for i in range(0, len(WSResult)):
        check=0
        if (WSResult[i][1])=='Nb': #人
            people+=WSResult[i][0]
            people+=" "
        elif (WSResult[i][1]) == 'VA'or (WSResult[i][1]) == 'VH': #事 type 1
            event+=WSResult[i][0]
            event+=" "
        elif (((WSResult[i][1]) == 'VC'or WSResult[i][1] == 'VJ') and i<len(WSResult)-1):
            if((WSResult[i+1][1]) != ''):
                event += WSResult[i][0]
                z=i
                for limit in range(0,15):
                    if ((WSResult[z][1])!='Na' or (WSResult[z][1])!='Nv') and z+1<len(WSResult):
                        event += WSResult[z+1][0]
                        z+=1
                    else:
                        event += " "
                        break
        elif (WSResult[i][1]) == 'Nd':  #時
            when+=WSResult[i][0]
            when+=" "
        elif(WSResult[i][1] == 'Neu'):
            if((i < len(WSResult)) - 4):
                if (WSResult[i][1] == 'Neu' and WSResult[i + 1][1] == 'FW' and WSResult[i + 2][1] == 'Neu' and
                        WSResult[i + 3][1] == 'FW' and WSResult[i + 4][1] == 'Neu'):
                        when +=WSResult[i][0]+WSResult[i+1][0]+WSResult[i+2][0]+WSResult[i+3][0]+WSResult[i+4][0]
                        when += " "
                        check=1
            if (check==0 and WSResult[i][1] == 'Neu' and WSResult[i + 1][1] == 'FW' and WSResult[i + 2][1] == 'Neu' and WSResult[i-1][1] != 'FW'):
                when += WSResult[i][0] + WSResult[i + 1][0] + WSResult[i + 2][0]
                when += " "
        elif (WSResult[i][1]) == 'Nc': #地
            place+=WSResult[i][0]
            place+=" "
        elif (WSResult[i][1]) == 'Na': #物
            thing += WSResult[i][0]
            thing += " "
        if (WSResult[i][1] == 'VH' or WSResult[i][1] == 'VHC' or WSResult[i][1] == 'VI' or WSResult[i][1] == 'VJ' or WSResult[i][1] == 'VK' or WSResult[i][1] == 'VL'):  # 情緒
            emotion.append(WSResult[i][0])

print(people)
print(event)
print(when)
print(place)
print(thing)

#print(emotion[0])
#print(emotion[1])
#print(len(emotion))

num=0
tmp=0
x=[]
y=[]
t=0
u=0
fo=open("正面.txt")
while 1:
        t+=1;
        line=fo.readline()
        if line=="":
                break
        line=line[:len(line)-1].split("\t")
        x.append(line[0].strip())
#print(x)
#print(t)
f=open("負面.txt")
while 1:
        u+=1
        line=f.readline()
        if line=="":
                break
        line=line[:len(line)-1].split("\t")
        y.append(line[0].strip())


for k in range(0,len(emotion)):
    for j in range(0, len(x)):
        if (len(emotion[k]) > 0):
            if  emotion[k]== x[j]:
                pemotion+=emotion[k]
                pemotion +=" "
                break

for k in range(0,len(emotion)):
    for j in range(0, len(y)):
        if (len(emotion[k]) > 0):
            if  emotion[k]== y[j]:
                nemotion+=emotion[k]
                nemotion += " "
                break
print(pemotion)
print(nemotion)
#print(token)
