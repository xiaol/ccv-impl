__author__ = 'ding'
from bson import ObjectId

from pymongo import Connection

con = Connection('60.28.29.37:20010')
clct_resource = con.tiercel.resource

con39 = Connection('60.28.29.39:20010')
clct_statisticsLog = con39.tiercel.statisticsLog


def fix(resourceIdList):

    begin = 0
    print 'resourceIdList len:',len(resourceIdList)
    resourceIdList = list(set(resourceIdList))
    print 'uni len:',len(resourceIdList)


    while begin < len(resourceIdList):
        if begin + 100 > len(resourceIdList):
            ids = resourceIdList[begin:]
        else:
            ids = resourceIdList[begin : begin+100]
        obids = []
        for one in ids:
            try:
                obids.append(ObjectId(one))
            except:
                pass
        for resource in clct_resource.find({'_id':{'$in':obids}}, {'channelId':1}):
            clct_statisticsLog.update({'resourceId':str(resource['_id'])}, {'$set':{'channelId':resource['channelId']}},multi=True)
        begin += 100
        print begin

resourceIdList = clct_statisticsLog.distinct('resourceId')

print len(resourceIdList)
fix(resourceIdList)
