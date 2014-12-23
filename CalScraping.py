#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

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
        if len(d.contents[1])==1:
            with_tag=""
            for e in d.contents[3]:
                with_tag+=unicode(e)
            p=re.compile(r"<[^>]*?>")
            status=p.sub("",with_tag).strip()
            schedule[i].append(status)
        elif len(d.contents[1])==2:
            schedule[i].append(unicode(d.contents[1].contents[1].string).strip())
        else:
            for j in range(0,len(d.contents[1]),3):
                schedule[i].append(unicode(d.contents[1].contents[j].contents[1]).strip())
        schedule[i][0]=caldate.split('-')[0]+'-'+caldate.split('-')[1]+'-'+str(i+1)

    return schedule
    #return date

if __name__=='__main__':
    lst = GetData('2015-1-1')
    #lst=LibClosed(lst,30)
    for l in lst:
        for e in l:
            print e
        print '#'*10

