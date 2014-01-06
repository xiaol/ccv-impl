#coding=utf-8
# 更新主控脚本
# 从channel表读取配更新配置，进行更新

from common.SingletonProcessDecoration import SingletonProcessDecoration
from setting import clct_channel
import sys,time,json,traceback
from common.common import getCurTime
from pprint import pprint
from common.ParallelUtil import ThreadPool

#设置全局超时时间
import socket
socket.setdefaulttimeout(60)


def process_channel(channel):
    print '==================  start %s %s ========================='%(channel['channelId'],channel['channelName'])
    pprint(channel)
    try:
        handleFrequents = int(float(channel['handleFrequents']))
    except:
        print 'Wrong handleFrequents:',channel['handleFrequents']
        raise Exception('Wrong handleFrequents:' + str(channel['handleFrequents']))
    #计算下次更新时间
    tCur = time.mktime(time.localtime())
    if channel['nextSearchTime'] == u'00000000000000':
        channel['nextSearchTime'] = '20130628165558'
    tPreNext = time.mktime(time.strptime(channel['nextSearchTime'],'%Y%m%d%H%M%S'))
    tNext =  tPreNext + (int((tCur - tPreNext) / handleFrequents) + 1) * handleFrequents
    t = time.strftime('%Y%m%d%H%M%S',time.localtime(tNext))
    print 'Next Update Time:',t
    #更新下次更新时间
    clct_channel.update({'_id':channel['_id']},{'$set':{'nextSearchTime': t}})
    
    #开始搜索
    for i,searchHandle in enumerate(channel['searchHandleList']):
        if searchHandle == "":
            continue
        print '[%d] %s %s'%(i,channel['sourceList'][i],searchHandle)
        handleModule,handleName = searchHandle.split('.')
        __import__(handleModule)
        module = sys.modules[handleModule]
        print module.handle(channel['channelId'],handleName,channel['sourceList'][i])

def doWork(channel):
    try:
        process_channel(channel)
    except:
        print '=========== process_channel %s error ============='%channel['channelId']
        clct_channel.update({'_id':channel['_id']},{'$set':{'searchStatus':'error','searchMsg':traceback.format_exc(),\
                                                            'searchTime':getCurTime()}})
        print traceback.format_exc()
    else:
        print '=========== process_channel %s success ============='%channel['channelId']
        clct_channel.update({'_id':channel['_id']},{'$unset':{'searchStatus':1,'searchMsg':1}})
        clct_channel.update({'_id':channel['_id']},{'$set':{'searchTime':getCurTime()}})

    #修改下次更新时间

    sys.stdout.flush()

def main():
    while True:
        channels = clct_channel.find({'searchHandleList':{"$ne":[]},"processed":True,\
                                      'nextSearchTime':{'$lte':getCurTime(),"$not":{"$in":["","00000000000000"]}}}, timeout=False)
        threadPool = ThreadPool(5)
        for channel in channels:
            threadPool.do(doWork,channel)
        threadPool.join()
        print 'loop'
        time.sleep(6)



if __name__ == '__main__':
    main()

    

