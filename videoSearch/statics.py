#code=utf-8

from setting import clct_userWeibo, clct_userRecommend,clct_resource, clct_playLog, clct_playViewRateLog
from pprint import pprint

def meanOfVideosPerWeiboUser():
    users = clct_userWeibo.distinct('sinaId')
    count = len(users)
    total = clct_userWeibo.count()
    mean = total/count
    print mean

startTime = '20131230000000'
endTime = '20131231000000'

def displayRate():
    totalRets = clct_playViewRateLog.find({'updateTime':{'$gte':startTime,'$lte': endTime}}).sort('uuid', -1)
    print 'total count', totalRets.count()
    rets = clct_playViewRateLog.find({'viewNum':{'$ne':0},'updateTime':{'$gte':startTime,'$lte': endTime}}).sort('uuid', -1)
    sum = 0
    f = file('displayRate.log','w')

    print rets.count()
    for ret in rets:
        rate = float(ret['playNum'])/ret['viewNum']
        sum += rate
        f.write('playNum:'+ str(ret['playNum'])+ '  viewNum:'+ str(ret['viewNum'])+  ' rate:'+ '%.2f'%rate+ '        \t\t '+ret['uuid']+'\n')

    f.close()
    print sum/rets.count()

from collections import defaultdict
import matplotlib.pyplot as plt

def displayRateRange():
    rets = clct_playViewRateLog.find({'viewNum':{'$ne':0},'updateTime':{'$gte':startTime,'$lte': endTime}}).sort('uuid', -1)
    sum = 0
    mm = defaultdict(list)

    print rets.count()
    for ret in rets:
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
                mm[dislike].append(resourceR['resourceName'])
            else:
                mm[dislike].append(mm[dislike][0])
    sizes = []
    labels = []
    for k, v in mm.items():
        if len(v) <= 50:
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
        if len(v) <= 10:
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

if __name__ == '__main__':
    #statics()
    #userBehavior()
    displayRate()
    displayRateRange()
