import json
from collections import OrderedDict
from multiprocessing import Pool
import socket
import time
input=["我想辦理自動扣款，請問如何申請？","如何申請預借現金密碼？","如何於網路預借現金使用「一次性預借現金密碼」?",
       "如何調高我的預借現金額度呢?","預借現金款項應如何繳還，會有利息或其它費用嗎?","預借現金是否有日限額的限制?",
       "預借現金應如何判斷可預借多少金額?","預借現金有無金額限制?","如果我不想使用預借現金服務，如何辦理?",
       "我想辦理分期靈活金，請問有什麼資格限制？"]

V=0
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
WSResult=[]
#seg(input)
resultTwo=[]
resultOne=[]
####
#print(questions[0])
tmp=[]
#tmp.append([])
percent=0
op=[]
index=0
check=0
checkP=""
tmp1=0
tmp2=0
print(len(questions))
for k in range(0,338):
    if((int)((k/338)%100*100)>percent):
        percent=(int)((k / 338) % 100 * 100)
        print("Now loading " + str(percent)+"%")
#for k in range(0, 50):
#    if ((int)((k / 50) % 100 * 100) > percent):
#        percent = (int)((k / 50) % 100 * 100)
#        print("Now loading " + str(percent) + "%")
    if k!=183:
        tmp.append([])
        tmp[k].append('<s>')
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
                if WSResult[p][0] not in tmp:
                    V+=1
                tmp[k].append(WSResult[p][0])
        tmp[k].append('</s>')
    else:
        tmp.append([])

parseinput=[]
for i in range(0,len(input)):
    parseinput.append([])
    parseinput[i]=['<s>']
    WSResult = []
    seg(input[i])
    for p in range(0, len(WSResult)):
        if WSResult[p][0] != '「' and WSResult[p][0] != '」' and WSResult[p][0] != '？' and WSResult[p][0] != '?' and \
                WSResult[p][0] != '，' \
                and WSResult[p][0] != '…' and WSResult[p][0] != '/' and WSResult[p][0] != '"' and WSResult[p][0] != '（' \
                and WSResult[p][0] != '）' and WSResult[p][0] != '╱' and WSResult[p][0] != '】' and WSResult[p][0] != '【':
            if WSResult[p][0] not in tmp:
                V += 1
            parseinput[i].append(WSResult[p][0])
    parseinput[i].append('</s>')
bigramresult=[]
bigramoutput=[]
trigramresult=[]
trigramoutput=[]
V-=2 #<s> </s> not count
#implement bigram
for l in range(0,len(parseinput)):
    for i in range(0,len(parseinput[l])-1):
        count1=0 #bigram count wi
        count2=0 #bigram count wi wi+1
        for j in range(0,len(tmp)):
            for k in range(0,len(tmp[j])):
                if(parseinput[l][i]==tmp[j][k]):
                    count1+=1
                    if(k<len(tmp[j])-1):
                        if(parseinput[l][i+1]==tmp[j][k+1]):
                            count2+=1
        temp=(1+count2)/(V+count1)
        bigramresult.append(temp)
    bigramans=1.0
    for k in range(0,len(bigramresult)):
        bigramans=bigramans*float(bigramresult[k])
    bigramoutput.append(bigramans)
    bigramresult.clear()

#print("Bigram Result is "+str(bigramans))

##implement trigram
finalindex=0
count3=0
count4=0

for i in range(0,len(tmp)):
    tmp[i].insert(0,'<ss>')
    finalindex=len(tmp[i])
    tmp[i].insert(finalindex, '</ss>')

for t in range(0,len(parseinput)):
    parseinput[t].insert(0,'<ss>')
    parseinput[t].insert(len(parseinput[t]),'</ss>')
    for i in range(0,len(parseinput[t])-2):
        count3=0 #trigram count wi wi+1
        count4=0 #trigram count wi wi+1 wi+2
        for j in range(0,len(tmp)):
            for k in range(0,len(tmp[j])):
                if(parseinput[t][i]==tmp[j][k]):
                    if(k<len(tmp[j])-2):
                        if(parseinput[t][i+1]==tmp[j][k+1]):
                            count3+=1
                            if (parseinput[t][i+2] == tmp[j][k+2]):
                                count4+=1
        temp=(1+count3)/(V+count4)
        trigramresult.append(temp)
    trigramans=1.0
    #print("pareinput= "+str(parseinput))
    for k in range(0,len(trigramresult)):
        trigramans=trigramans*float(trigramresult[k])
    trigramoutput.append(trigramans)
    trigramresult.clear()
##output###
for i in range(0,len(input)):
    print(str(input[i])+" Bigram result= "+str(bigramoutput[i])+" , "+"Trigram result= "+str(trigramoutput[i]))
