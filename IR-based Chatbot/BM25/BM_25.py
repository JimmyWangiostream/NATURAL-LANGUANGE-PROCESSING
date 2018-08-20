from snownlp import SnowNLP
import json
from collections import OrderedDict
from multiprocessing import Pool
import socket
import time

input="申請後需要多久才會知道是否申請成功？"

questions=[]
answers=[]
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

with open('CTBC.json', encoding='utf-8') as fh:
    data = json.load(fh)
for i in range(0,338):
    questions.append(data[i]['question'])
    answers.append(data[i]['answer'])
#y=data[0]['question']
#print(questions)
####
print(questions[0])
tmp=[]
#tmp.append([])
percent=0
op=[]
index=0
check=0
print(len(questions))
for k in range(0,338):
    if((int)((k/338)%100*100)>percent):
        percent=(int)((k / 338) % 100 * 100)
        print("Now loading " + str(percent)+"%")
    if k!=183:
        tmp.append([])
        #print(k)
        #print(questions[k])
        #op=[]
        WSResult=[]
        seg(questions[k])
        for p in range(0, len(WSResult)):
            #print(WSResult[p][0])
            if WSResult[p][0]!='「' and WSResult[p][0]!='」' and WSResult[p][0]!='？' and WSResult[p][0]!='?'and WSResult[p][0]!='，'\
                    and WSResult[p][0]!='…' and  WSResult[p][0]!='/' and WSResult[p][0]!='"' and WSResult[p][0]!='（'\
                    and WSResult[p][0]!='）'and WSResult[p][0]!='╱' and WSResult[p][0]!='】' and WSResult[p][0]!='【':
                tmp[k].append(WSResult[p][0])
        #print(tmp[k])
    else:
        tmp.append([])

WSResult=[]
seg(input)
parseinput=[]
for p in range(0, len(WSResult)):
    # print(WSResult[p][0])
    if WSResult[p][0] != '「' and WSResult[p][0] != '」' and WSResult[p][0] != '？' and WSResult[p][0] != '?' and \
            WSResult[p][0] != '，' \
            and WSResult[p][0] != '…' and WSResult[p][0] != '/' and WSResult[p][0] != '"' and WSResult[p][0] != '（' \
            and WSResult[p][0] != '）' and WSResult[p][0] != '╱' and WSResult[p][0] != '】' and WSResult[p][0] != '【':
        parseinput.append(WSResult[p][0])
s=SnowNLP(tmp)
x=s.sim(parseinput)
#print(x)
Answer=x.index(max(x))
print(str(answers[Answer]))

#print(tmp[0])
#print(tmp[1])
