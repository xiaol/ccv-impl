#coding=utf-8
__author__ = 'ding'
from pymongo import Connection
import time

con = Connection('h37:20010')
clct_resource = con.tiercel.resource
clct_channel = con.tiercel.channel

for channel in clct_channel.find(timeout=False):
    resourceIt = clct_resource.find({'channelId':channel['channelId']},timeout=False).sort([('number',1),('createTime',1)])
    SIZE = resourceIt.count()

    print channel
    print SIZE
    if SIZE == 0:
        continue

    t_start = time.mktime(time.strptime(channel['createTime'],'%Y%m%d%H%M%S'))
    try:
        t_now = time.mktime(time.strptime(channel['updateTime'],'%Y%m%d%H%M%S'))
    except:
        t_now = time.time()
    t_span = (t_now - t_start)/SIZE
    t_this = t_start

    #间隔过短，修改开始时间
    if t_span < 3600 :
        t_span = 3600
        t_start = t_now - t_span*SIZE

    for resource in resourceIt:
        t_this += t_span
        updateTime = time.strftime('%Y%m%d%H%M%S',time.localtime(t_this))
        print updateTime
        clct_resource.update({'_id':resource['_id']},{'$set':{'updateTime':updateTime}})


