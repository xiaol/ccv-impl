#coding=utf-8
__author__ = 'ding'
__doc__ = '''用来分析计算前一天的 播放、浏览数据；并累加到eresource表'''
import sys, os
sys.path += [os.path.dirname(os.path.dirname(os.path.dirname(__file__)))]
import  time
from videoCMS.conf import clct_resource
from videoCMS.conf import clct_playViewRateLog
from collections import defaultdict
from bson import ObjectId


def calc(date):
    resourceMap = defaultdict(lambda: {'v': 0, 'p': 0})
    result = list(clct_playViewRateLog.find({'date':date}))
    sum_play = 0
    sum_view = 0
    num = 0
    for log in result:
        if 'viewList' not in log and 'playList' not in log:
            continue
        #if len(log.get('viewList', [])) < 3:
        #    continue
        playList = log.get('playList', [])
        viewList = log.get('viewList', [])
        sum_play += len(playList)
        sum_view += len(viewList)
        num += 1
        for resourceId in playList:
            resourceMap[resourceId]['p'] += 1
        for resourceId in viewList:
            resourceMap[resourceId]['v'] += 1

    for resourceId in resourceMap:
        r_v = resourceMap[resourceId]['v']
        r_p = resourceMap[resourceId]['p']
        print resourceId, r_p, r_v
        clct_resource.update({'_id': ObjectId(resourceId)}, {'$inc': {'r_v': r_v, 'r_p': r_p}})
    print num
    print sum_play, '/', sum_view


def calcYesterday():
    #已统计至：2014-3-27
    date = time.strftime('%Y%m%d', time.localtime(time.time()-1*24*3600))
    print date
    calc(date)



if __name__ == '__main__':
    calcYesterday()