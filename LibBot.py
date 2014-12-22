#-*- coding:utf-8 -*-
import twitter
from datetime import datetime
from dateutil.relativedelta import relativedelta
import traceback
import secret_KUlibbot
import CalScraping as cal


def FetchList():
    thismonth=datetime.today().strftime(u'%Y-%m-1')
    nextmonth=(datetime.today()+relativedelta(months=1)).strftime(u'%Y-%m-1')
    
    lst=cal.GetData(thismonth)+cal.GetData(nextmonth)

    return lst
    

def PostTodayProgram(api,lst):
    todaymsg=u'<本日の日程>\n'

    td=datetime.today()
    for i,l in enumerate(lst[td.day-1]):
        if i==0:
            continue
        else:
            todaymsg+=lst[td.day-1][i]
            todaymsg+=u'\n'

    postdate=u'['
    postdate+=datetime.now().strftime(u'%Y-%m-%d %H:%M')
    postdate+=u'現在'
    postdate+=u']\n'
    
    api.PostUpdate((todaymsg+postdate).encode('utf-8'))
    #print todaymsg+postdate

def PostTomorrowProgram(api,lst):
    tomorrowmsg=u'<明日の日程>\n'

    td=datetime.today()
    for i,l in enumerate(lst[td.day]):
        if i==0:
            continue
        else:
            tomorrowmsg+=lst[td.day][i]
            tomorrowmsg+=u'\n'

    postdate=u'['
    postdate+=datetime.now().strftime(u'%Y-%m-%d %H:%M')
    postdate+=u'現在'
    postdate+=u']\n'
    
    api.PostUpdate((tomorrowmsg+postdate).encode('utf-8'))
    #print tomorrowmsg+postdate

def PostCloseDay(api,lst): 
    head=u'<近日の休館日>\n'
    foot=u'['+unicode(datetime.now().strftime(u'%Y-%m-%d %H:%M'))+u'現在]\n'
    
    msglist=[]
    for e in cal.LibClosed(lst,80):
        msg=u'   '
        msg+=e[0][5:]
        wday=[u'Mon',u'Tue',u'Wed',u'Thu',u'Fri',u'Sat',u'Sun']
        msg+=u'('
        msg+=wday[datetime.strptime(e[0],"%Y-%m-%d").weekday()]
        msg+=u')\n'
        msglist.append(msg)

    postmsg=head
    for e in msglist:
        if len(postmsg+foot+e)>135:
            postmsg+=foot
            api.PostUpdate(postmsg.encode('utf-8'))
            #print postmsg
            postmsg=head+e
        else:
            postmsg+=e
    if len(postmsg)>len(head):
        postmsg+=foot
        if len(postmsg)>140:
            postmsg=head+'too long to show.\n'+foot
        api.PostUpdate(postmsg.encode('utf-8'))
        #print postmsg

def ModifyFollowers(api):
    followers=api.GetFollowers()
    friends=api.GetFriends()
    followers_set=set(followers)
    friends_set=set(friends)

    non_friends=followers_set-friends_set
    if len(non_friends)==0:
        #print 'No need for follow back'
    else:
        for friend in non_friends:
            api.CreateFriendship(friend.id)
            #print "Follow friend name:",
            #print friend.screen_name


if __name__=='__main__':
    api = twitter.Api(
        consumer_key = secret_KUlibbot.twDict['consumer_key'],
        consumer_secret = secret_KUlibbot.twDict['consumer_secret'],
        access_token_key = secret_KUlibbot.twDict['access_token_key'],
        access_token_secret = secret_KUlibbot.twDict['access_token_secret']
    )

    lst=FetchList()
    PostTodayProgram(api,lst)
    PostTomorrowProgram(api,lst)
    PostCloseDay(api,lst)
    try:
        ModifyFollowers(api)
    except:
        pass

