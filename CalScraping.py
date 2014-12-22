#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def LibClosed(lst,d):
    res=[]
    td=datetime.today()
    ub=min(td.day+d,len(lst)+1)
    for d in range(td.day,ub):
        for e in lst[d-1]:
            if e.find(u'休')!=-1 or e.find(u'閉')!=-1:
                res.append(lst[d-1])
    
    return res

def GetData(caldate):
    url = 'http://www.kulib.kyoto-u.ac.jp/modules/piCal/index.php?cid=1&smode=Monthly&caldate='+caldate
    r = requests.get(url)
    soup = BeautifulSoup(r.text.encode(r.encoding))
    s = soup.find('table',{'id':'calbody'})
    date=[]
    for i in range(7,len(s),4):
        for j in range(1,15,2):
            day=s.contents[i].contents[j]
            if len(day)>2:
                for k in range(len(day)):
                    try:
                        lib=day.contents[k]['class'][0]
                        if lib==u'附属図書館':
                            date.append(day.contents[k])
                    except:
                        continue
                for k in range(len(day)):
                    try:
                        lib=day.contents[k].a['class'][0]
                        if lib==u'附属図書館':
                            date.append(day.contents[k])
                    except:
                        continue
    
    schedule=[[0] for i in range(len(date))]
    for i,d in enumerate(date):
        if len(d)==2:
            schedule[i].append(d.contents[1].strip())
        else:
            for j in range(0,len(d),3):
                schedule[i].append(d.contents[j].contents[1].strip())
        schedule[i][0]=caldate[:8]+str(i+1)

    return schedule

if __name__=='__main__':
    lst = GetData(datetime.today().strftime('%Y-%m-%d'))
    lst=LibClosed(lst,30)
    for l in lst:
        print l

