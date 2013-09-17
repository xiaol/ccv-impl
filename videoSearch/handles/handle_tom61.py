# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import sys, os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from lxml import etree
import re, pprint
from common.common import getCurTime
from common.Domain import Resource,Channel
from common.HttpUtil import get_html
from setting import clct_channel
from handle_embed import getVideoUrl


'''
    只抽取第一页
'''
def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url, "gbk"))
    videos = tree.xpath('//div[@class="f_box"]/dl/dt/a')
    p_video_info = re.compile(r'addFlash\([\'"]?(\w+)[\'"]?\s*,\s*[\'"]?([\w#]+)[\'"]?')
    ret = []
    for video in videos:
        try:
            url = video.xpath('./@href')[0]
            title = video.xpath('./@title')[0]
            html = get_html(url, "gbk")
            video_info = p_video_info.search(html).groups()
            #html = etree.HTML(html).xpath('//input[@id="html_code"]/@value')[0]

            video_type = video_info[0]
            if not video_type in ['tudou', 'youku', 'iqiyi', 'qiyi', 'letv', 'qq', 'pptv', 'sina', 'ku6', '56']:
                continue
            if video_type == "qiyi":
                video_type = 'iqiyi'

            vid = video_info[1]
            vid = vid.replace("#a","1")
            vid = vid.replace("#b","2")
            vid = vid.replace("#c","3")
            vid = vid.replace("#d","4")
            vid = vid.replace("#e","5")
            vid = vid.replace("#f","6")
            vid = vid.replace("#g","7")
            vid = vid.replace("#h","8")
            vid = vid.replace("#i","9")
            vid = vid.replace("#j","0")

            url = getVideoUrl(vid, video_type)
            if url:
                ret.append(buildResource(url, title, channelId, vid, video_type))
        except:
            print url
            continue

    return ret


def buildResource(url, title, channelId, videoId, video_type):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    resource['type'] = 'video'
    resource['videoType'] = video_type
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    pprint.pprint(handle('http://www.tom61.com/xsxpfj/xssp/', 100128, 1))

