#code=utf-8

from setting import clct_userWeibo, clct_userRecommend,clct_resource, clct_playLog
from pprint import pprint

def meanOfVideosPerWeiboUser():
    users = clct_userWeibo.distinct('sinaId')
    count = len(users)
    total = clct_userWeibo.count()
    mean = total/count
    print mean


def displayRate():
    pass

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
    statics()
