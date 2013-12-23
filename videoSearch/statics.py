#code=utf-8

from setting import clct_userWeibo, clct_userRecommend,clct_resource, clct_playLog, clct_playViewRateLog
from pprint import pprint

def meanOfVideosPerWeiboUser():
    users = clct_userWeibo.distinct('sinaId')
    count = len(users)
    total = clct_userWeibo.count()
    mean = total/count
    print mean


def displayRate():
    rets = clct_playViewRateLog.find({'viewNum':{'$ne':0},'updateTime':{'$gte':'20131222000000','$lte': '20131223000000'}}).sort('uuid', -1)
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
    rets = clct_playViewRateLog.find({'viewNum':{'$ne':0},'updateTime':{'$gte':'20131220000000','$lte': '20131221000000'}}).sort('uuid', -1)
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


if __name__ == '__main__':
    #statics()
    #displayRateRange()
    displayRate()
