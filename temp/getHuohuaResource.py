__author__ = 'ding'
from videoCMS.conf import clct_resource
import sys


resourceList = clct_resource.find({'videoType':'huohua','isOnline':True})


for resource in resourceList:
    print 'http://cdn.video.weiweimeishi.com'+resource['videoId']