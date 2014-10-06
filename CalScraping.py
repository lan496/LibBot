#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def GetData(caldate):
    url = 'http://www.kulib.kyoto-u.ac.jp/modules/piCal/index.php?cid=1&smode=Monthly&caldate='+caldate
    r = requests.get(url)
    soup = BeautifulSoup(r.text.encode(r.encoding))
    
    lst=[[0 for j in range(1)] for i in range(42)]
    res=[]

    for i in range(6):
        for j in range(7):
            try:
                soup.find('table',{'id':'calbody'}).contents[4*i+7].contents[2*j+1].contents[1]
            except IndexError:
                continue
            locate=soup.find('table',{'id':'calbody'}).contents[4*i+7].contents[2*j+1]
            if len(locate.contents)<3:
                continue
            if j==0:
                lst[7*i+j][0]=unicode(locate.contents[1].contents[0].get('href'))
            else:
                lst[7*i+j][0]=unicode(locate.contents[1].get('href'))
            for k,pl in enumerate(locate.findAll('a',{'class':u'附属図書館'})):
                lst[7*i+j].append(unicode(locate.findAll('a',{'class':u'附属図書館'})[k].contents[1]))
    
    for e in lst:
        if e[0]!=0:
            res.append(e)
            t=datetime.strptime(e[0][(e[0].find('caldate')+8):],'%Y-%m-%d')
            t.isoformat()
            e[0]=t.date()

    return res


def LibClosed(lst,d):
    res=[]
    td=datetime.today()
    ub=min(td.day+d,len(lst)+1)
    for d in range(td.day,ub):
        for i,e in enumerate(lst[d-1]):
            if i==0:
                continue
            else:
                if e.find(u'休')!=-1 or e.find(u'閉')!=-1:
                    res.append(lst[d-1])
    
    return res


if __name__=='__main__':
    lst = GetData('2014-10-1')
    for l in lst:
        print l[0]

