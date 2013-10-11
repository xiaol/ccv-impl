# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import os
import sys
from setting import clct_channel, clct_resource, GIF_SERVER, GIF_SERVER_PORT, GIF_SERVER_DIR, GIF_TEMP_DIR
from pprint import pprint
from common.common import getCurTime


def insertResouce(resouceList, channelId):
    """ 入库 """

    numInserted = 0
    for resource in resouceList:
        try:
            resource['weight'] = -1
            clct_resource.insert(resource, safe=True)
            numInserted += 1
        except Exception, e:
            print("insert Error!", e)

    #如果成功有gif插入，则更新频道
    if numInserted > 0:
        clct_channel.update({'channelId': channelId}, {'$set': {'updateTime': getCurTime()}})
    #清除权重
    clct_resource.update({'channelId': channelId, 'weight': {'$ne': -1}}, {'$set': {'weight': -1}}, multi=True)


def startSearch(handleName, url, channelId, **keyParams):
    #获取模块
    __import__(handleName)
    module = sys.modules[handleName]
    channel = clct_channel.find_one({'channelId': channelId})

    #抽取
    result = module.handle(url, channelId, **keyParams)

    for one in result:
        if not channel['autoOnline']:
            one['isOnline'] = False
        one['duration'] = channel['duration']
        one['categoryId'] = channel['channelType']
        one['type'] = 'gif'

    #拷贝本地gif和png到47服务器 然后删除本地图片
    cmd = 'scp -P %d -r %s/videoCMS/gif_resource/%d %s:%s' \
          % (GIF_SERVER_PORT, GIF_TEMP_DIR, channelId, GIF_SERVER, GIF_SERVER_DIR)
    os.popen(cmd)
    cmd = 'rm -f %s/videoCMS/gif_resource/%d/*.*' % (GIF_TEMP_DIR, channelId)
    os.popen(cmd)

    #入库
    if len(result) != 0:
        insertResouce(result, channelId)


def handle(channelId, handleName, url):
    channel = clct_channel.find_one({'channelId': channelId})
    channelId = channel['channelId']

    if handleName == 'onegif':
        startSearch('handlesGif.handle_onegif', url, channelId)
    elif handleName == 'forgifs':
        startSearch('handlesGif.handle_forgifs', url, channelId)


if __name__ == '__main__':
    handle(100056, 'forgifs', 'http://forgifs.com/gallery/main.php')
    pass
