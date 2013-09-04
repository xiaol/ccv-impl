# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

from lxml import etree
import re, pprint, json
from common.common import getCurTime
from common.Domain import Resource,Channel
from common.HttpUtil import get_html
from setting import clct_channel


def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url))
    videos = tree.xpath('//div[@id="block-channel-content"]//a[@class="title"]')

    ret = []
    base_url = "http://www.acfun.tv"
    for video in videos:
        try:
            title = video.xpath('./text()')[0]
            url = base_url + video.xpath('./@href')[0]
            html = get_html(url)
            acfun_id = re.search(r"\[[Vv]ideo\](\d+)\[/[Vv]ideo\]", html)
            if not acfun_id:
                acfun_id = re.search(r"src=\"/newflvplayer/player.*id=(\d+)", html).groups()[0]
            else:
                acfun_id = acfun_id.groups()[0]
            video_info = json.loads(get_html("http://www.acfun.tv/api/getVideoByID.aspx?vid="+acfun_id))
            video_id = video_info["vid"]
            video_type = video_info["vtype"]
            ret.append(buildResource(url, title, channelId, video_id, video_type))
        except Exception, e:
            print e
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
    pprint.pprint(handle('http://www.acfun.tv/tag/66170.aspx',100055,1))