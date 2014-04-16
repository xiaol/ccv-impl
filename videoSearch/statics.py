#coding=utf-8

from setting import clct_userWeibo, clct_netspeed, clct_userRecommend,clct_resource, clct_playLog, clct_playViewRateLog, clct_channel
from pprint import pprint
def meanOfVideosPerWeiboUser():

    users = clct_userWeibo.distinct('sinaId')
    count = len(users)
    total = clct_userWeibo.count()
    mean = total/count
    print mean

startTime = '20140309000000'
endTime = '20140310000000'
dateTime = '20140410'

def displayRate(newUser=True):
    totalRets = clct_playViewRateLog.find({'date':dateTime}).sort('uuid', -1)
    print 'total count', totalRets.count()
    rets = clct_playViewRateLog.find({'viewNum':{'$ne':0},'date':dateTime}).sort('uuid', -1)
    sum = 0
    f = file('displayRate.log','w')

    print rets.count()
    newUserCount = 0
    count = 0
    for ret in rets:
        if ret['viewNum'] <= 2 and ret['playNum'] == 0:
            count = count + 1
            continue
        if newUser:
            user = clct_user.find_one({'uuid': ret['uuid']})
            if user is not None and user['createTime'] > startTime and user['createTime'] < endTime:
                newUserCount = newUserCount + 1
            else:
                continue
        rate = float(ret['playNum'])/ret['viewNum']
        sum += rate
        f.write('playNum:'+ str(ret['playNum'])+ '  viewNum:'+ str(ret['viewNum'])+  ' rate:'+ '%.2f'%rate+ '        \t\t '+ret['uuid']+'\n')

    f.close()
    if newUser:
        print 'New users count: ', newUserCount
    print ' ',count
    print sum/(rets.count() - count)

from collections import defaultdict
import matplotlib.pyplot as plt

def displayRateRange(newUser=True):
    rets = clct_playViewRateLog.find({'viewNum':{'$ne':0},'date':dateTime}).sort('uuid', -1)
    sum = 0
    mm = defaultdict(list)

    print rets.count()
    newUserCount = 0
    for ret in rets:
        if newUser:
            user = clct_user.find_one({'uuid': ret['uuid']})
            if user is not None and user['createTime'] > startTime and user['createTime'] < endTime:
                newUserCount = newUserCount + 1
            else:
                continue
        mm[ret['viewNum']].append(ret['playNum'])

    sizes = []
    labels = []
    for k, v in mm.items():
        if len(v) == 1:
            continue
        sizes.append(len(v))
        labels.append(k)
    # The slices will be ordered and plotted counter-clockwise.
    explode = [0]*len(sizes)
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode[1] = 0.1
    explode[-1] = 0.1
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    plt.show()

def quitByFirstSight():
    rets = clct_playViewRateLog.find({'viewNum':0,'date':dateTime}).sort('uuid', -1)
    print rets.count()
    newUserCount = 0
    for ret in rets:
        user = clct_user.find_one({'uuid': ret['uuid']})
        if user is not None and user['createTime'] > startTime and user['createTime'] < endTime:
            newUserCount = newUserCount + 1
        else:
            continue
    print 'leaved users count : ', newUserCount

def missedUser():
    rets = clct_playViewRateLog.find({'date':dateTime}).sort('uuid', -1)
    print rets.count()
    count = 0
    for ret in rets:
        user = clct_user.find_one({'uuid': ret['uuid']},{'_id':1})
        if user is None:
            count = count +1
            print ret['uuid']
        else:
            continue
    print "lost users count: ", count

def findHotMovies():
    pass

def statics():
    #  5298360adc219360e4b52d62
    rets = clct_playLog.find({'resourceId':"529eee5cdc21933e9c607cdc", 'createTime':{'$gte':'20131130000000'}}).sort("operationTime", -1)
    count = rets.count()
    records = []
    timeRecords = []
    for ret in rets:
        records.append(ret['uuid'])
        timeRecords.append(ret['operationTime'][8:12])
    reSet = set(records)
    userCount = len(reSet)
    timeRecords.sort()
    print('PlayCount:', count, ' UserCount: ', userCount)
    pprint(timeRecords)

from setting import clct_userDiscard,clct_user
from bson import ObjectId
def userBehavior():
    rets = clct_userDiscard.find({})
    count = rets.count()
    sum = 0
    mm = defaultdict(list)
    for ret in rets:
        sum += len(ret['discardList'])
        for dislike in ret['discardList']:
            if len(mm[dislike]) == 0:
                resourceR = clct_resource.find_one({'_id':ObjectId(dislike)})
                if resourceR is None:
                    continue
                mm[dislike].append(resourceR['resourceName'])
            else:
                mm[dislike].append(mm[dislike][0])
    sizes = []
    labels = []
    for k, v in mm.items():
        if len(v) <= 100:
            continue
        sizes.append(len(v))
        labels.append(v[0])
        # The slices will be ordered and plotted counter-clockwise.
    explode = [0]*len(sizes)
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode[1] = 0.1
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    plt.show()

    print sum,' ', count, ' ', float(sum)/count

    likeRets = clct_user.find({'likeList':{'$exists':True}})
    likeCount = likeRets.count()
    likeSum = 0
    lmm = defaultdict(list)
    for likeRet in likeRets:
        likeSum += len(likeRet['likeList'])
        for like in likeRet['likeList']:
            if len(lmm[like]) == 0:
                resourceR = clct_resource.find_one({'_id':ObjectId(like)})
                lmm[like].append(resourceR['resourceName'])
            else:
                lmm[like].append(lmm[like][0])
    lsizes = []
    llabels = []
    for k, v in lmm.items():
        if len(v) <= 20:
            continue
        lsizes.append(len(v))
        llabels.append(v[0])
        # The slices will be ordered and plotted counter-clockwise.
    lexplode = [0]*len(lsizes)
    lcolors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    lexplode[1] = 0.1
    plt.pie(lsizes, explode=lexplode, labels=llabels, colors=lcolors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    plt.show()

    print likeSum, ' ', likeCount, ' ', float(likeSum)/likeCount

def getSumOfLikeAndDiscard():
    rets = clct_userDiscard.find({})
    rets.sort('_id',1)
    count = rets.count()
    sum = 0
    for ret in rets:
        sum += len(ret['discardList'])
        #print sum
    print sum,' ', count, ' ', float(sum)/count

    likeRets = clct_user.find({'likeList':{'$exists':True}})
    likeCount = likeRets.count()
    likeSum = 0
    for likeRet in likeRets:
        likeSum += len(likeRet['likeList'])
        #print likeRet['likeList']
    print likeSum, ' ', likeCount, ' ', float(likeSum)/likeCount

def getTag():
    rets = clct_user.find({'tagList':{'$exists':True}})
    print rets.count()


def draw():
    from matplotlib.dates import DayLocator, HourLocator,MonthLocator ,WeekdayLocator, DateFormatter, drange
    from matplotlib.dates import MONDAY
    import datetime

    mondays   = WeekdayLocator()
    days = DayLocator(None, 3)
    months    = MonthLocator()
    yList = [0]*55

    yList[0] = 0.11; yList[1] = 0.109; yList[2] = 0.108;yList[3] = 0.11; yList[4] = 0.111; yList[5] = 0.109; yList[6] = 0.111; yList[7] = 0.109; yList[8] = 0.108; yList[9] = 0.111; yList[10] = 0.112
    figure, axes = plt.subplots()
    startDate = datetime.datetime(2014, 3, 6, 0, 0, 0)
    endDate = datetime.datetime(2014, 4, 30, 0, 0, 0)
    delta = datetime.timedelta(hours=24)
    dates = drange(startDate , endDate, delta)
    axes.plot_date(dates,  yList,  '-',  marker='.',  linewidth=1)
    axes.xaxis.set_major_locator(days)
    axes.xaxis.set_major_formatter( DateFormatter("%b '%d"))
    axes.xaxis.set_minor_locator(mondays)
    axes.fmt_xdata = DateFormatter("%b '%d")
    plt.ylim(0.08,0.20)
    plt.ylabel('播放率')

    axes.autoscale_view()
    axes.xaxis.grid(True, 'major')
    axes.xaxis.grid(True, 'minor')
    axes.grid(True)
    figure.autofmt_xdate()
    plt.show()


def playDurationRate():
    rets = clct_playLog.find({}).limit(10000)

    mm = defaultdict(list)
    for ret in rets:
        retR = clct_resource.find_one({'_id': ObjectId(ret['resourceId'])})
        if retR is None or retR['duration'] == -1 or retR['duration'] == 0:
            continue
        retC = clct_channel.find_one({'channelId': retR['channelId']})
        if retC['channelType'] != 17:
            continue
        rate = float(int(ret['playTime'])/1000)/retR['duration']
        if float('%.1f'%rate) == 0.0:
            continue
        mm['%.1f'%rate].append(1)

    sizes = []
    labels = []
    for k, v in mm.items():
        sizes.append(len(v))
        labels.append(k)
        # The slices will be ordered and plotted counter-clockwise.
    explode = [0]*len(sizes)
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode[1] = 0.1
    explode[-1] = 0.1
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    plt.show()


def speedLog():
    rets = clct_netspeed.find({'operationTime':{'$lte': '20140404000000'}}).limit(1000)
    mm = defaultdict(list)
    import ast
    for ret in rets:
        speed = ast.literal_eval(ret['msg'])['speedroad']
        if speed < 10:
            mm['<10'].append(1)
        elif speed <30:
            mm['10-30'].append(1)
        else:
            mm['30~'].append(1)

    sizes = []
    labels = []
    for k, v in mm.items():
        sizes.append(len(v))
        labels.append(k)
        # The slices will be ordered and plotted counter-clockwise.
    explode = [0]*len(sizes)
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode[1] = 0.1
    explode[-1] = 0.1
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')
    plt.show()



if __name__ == '__main__':
    #statics()
    #userBehavior()
    #missedUser()
    #quitByFirstSight()
    #draw()
    #getTag()
    #playDurationRate()
    #getSumOfLikeAndDiscard()
    speedLog()
    displayRate(False)
    displayRateRange(False)
