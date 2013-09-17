# -*- coding: utf-8 -*-
__author__ = 'klb3713'

import sys, os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]
from lxml import etree
import re,pprint
from common.common import getCurTime
from common.Domain import Resource,Channel
from common.HttpUtil import get_html
from setting import clct_channel


def getVideoUrl(videoId, video_type):
    url = ""
    url_map = {
        "youku" : "http://v.youku.com/v_show/id_%s.html" %videoId,
        "tudou" : "http://www.tudou.com/programs/view/%s/" %videoId,
        "sina" : "http://video.sina.com.cn/v/b/%s.html" %videoId,
        "56" : "http://www.56.com/u11/v_%s.html" %videoId,
        "ku6" : "http://v.ku6.com/show/%s.html" %videoId,
        "pps" : "http://ipd.pps.tv/play_%s.html" %videoId
    }

    if video_type == "iqiyi":
        info_url = 'http://cache.video.qiyi.com/v/%s' % videoId
        info_xml = get_html(info_url)
        url = re.search(u'<videoUrl>([^<]+)</videoUrl>', info_xml).groups()[0]

    else:
        url = url_map.get(video_type, "")

    return url


def getVideoInfo(url, html=""):
    if not html:
        html = get_html(url)
    tree = etree.HTML(html)
    swf_urls = tree.xpath('//embed/@src')

    ret = []
    for swf_url in swf_urls:
        try:
            videoId = ""
            url = None
            video_type = None
            if swf_url.find("youku.com") >= 0:
                video_type = "youku"
                p_vids = [r'/sid/(\w+)/', r'VideoIDS=(\w+)']
                for vid in p_vids:
                    if re.search(vid, swf_url):
                        videoId = re.search(vid, swf_url).groups()[0]
                        break
                    else:
                        continue
                url = "http://v.youku.com/v_show/id_%s.html" %videoId

            elif swf_url.find("svn/trunk/youku/") >= 0:
                video_type = "youku"
                videoId = re.search(r'VideoIDS=(\w+)', swf_url).groups()[0]
                url = "http://v.youku.com/v_show/id_%s.html" %videoId

            elif swf_url.find("opengg.5ihaitao.com/") >= 0:
                video_type = "youku"
                videoId = re.search(r'VideoIDS=(\w+)', swf_url).groups()[0]
                url = "http://v.youku.com/v_show/id_%s.html" %videoId

            elif swf_url.find("tudou.com") >= 0:
                video_type = "tudou"
                p_vids = [r'tudou.com/v/([\w-]+)/', r'tudou.com/l/(\w+)/']
                for vid in p_vids:
                    if re.search(vid, swf_url):
                        videoId = re.search(vid, swf_url).groups()[0]
                        break
                    else:
                        continue
                url = "http://www.tudou.com/programs/view/%s/" %videoId

            elif swf_url.find("sina.com.cn") >= 0:
                video_type = "sina"
                videoId = re.search(r'/vid=(\d+[_]?\d+)', swf_url).groups()[0].replace('_', '-')
                url = "http://video.sina.com.cn/v/b/%s.html" %videoId

            elif swf_url.find("56.com") >= 0:
                video_type = "56"
                p_vids = [r'/v_(\w+)\.swf', r'/cpm_(\w+)\.swf']
                for vid in p_vids:
                    if re.search(vid, swf_url):
                        videoId = re.search(vid, swf_url).groups()[0]
                        break
                    else:
                        continue
                url = "http://www.56.com/u11/v_%s.html" %videoId

            elif swf_url.find("ku6.com") >= 0:
                video_type = "ku6"
                videoId = re.search(r'/refer/([\w\.]+)/', swf_url).groups()[0]
                url = "http://v.ku6.com/show/%s.html" %videoId

            elif swf_url.find("qiyi.com") >= 0:
                video_type = "iqiyi"
                videoId = re.search(r'\.com/(\w+)/', swf_url).groups()[0]
                info_url = 'http://cache.video.qiyi.com/v/%s' % videoId
                info_xml = get_html(info_url)
                url = re.search(u'<videoUrl>([^<]+)</videoUrl>', info_xml).groups()[0]

            elif swf_url.find("pps.tv") >= 0:
                video_type = "pps"
                videoId = re.search(r'/sid/(\w+)/', swf_url).groups()[0]
                url = "http://ipd.pps.tv/play_%s.html" %videoId

            if videoId and url and video_type:
                ret.append({"url": url, "video_type": video_type, "videoId": videoId})
            else:
                print(swf_url)
                continue

        except Exception, e:
            print(swf_url, e)
            continue

    return ret


def handle(url, channelId, tvNumber):
    tree = etree.HTML(get_html(url))
    swf_urls = tree.xpath('//embed/@src')

    ret = []
    for swf_url in swf_urls:
        try:
            videoId = None
            url = None
            title = None
            video_type = None
            if swf_url.find("youku.com") >= 0:
                video_type = "youku"
                videoId = re.search(r'/sid/(\w+)/', swf_url).groups()[0]
                url = "http://v.youku.com/v_show/id_%s.html" %videoId
                title = etree.HTML(get_html(url)).xpath('//meta[@name="description"]/@content')[0]

            elif swf_url.find("tudou.com") >= 0:
                video_type = "tudou"
                p_vids = [r'tudou.com/v/([\w-]+)/', r'tudou.com/l/(\w+)/']
                for vid in p_vids:
                    if re.search(vid, swf_url):
                        videoId = re.search(vid, swf_url).groups()[0]
                        break
                    else:
                        continue
                url = "http://www.tudou.com/programs/view/%s/" %videoId
                html = get_html(url, 'gbk')
                title = re.search(u'<title>([^<]+)_在线视频观看_土豆网视频[^<]+</title>', html).groups()[0]

            elif swf_url.find("sina.com.cn") >= 0:
                video_type = "sina"
                videoId = re.search(r'/vid=(\d+[_]?\d+)', swf_url).groups()[0].replace('_', '-')
                url = "http://video.sina.com.cn/v/b/%s.html" %videoId
                title = etree.HTML(get_html(url)).xpath('//meta[@name="description"]/@content')[0]

            elif swf_url.find("56.com") >= 0:
                video_type = "56"
                p_vids = [r'/v_(\w+)\.swf', r'/cpm_(\w+)\.swf']
                for vid in p_vids:
                    if re.search(vid, swf_url):
                        videoId = re.search(vid, swf_url).groups()[0]
                        break
                    else:
                        continue
                url = "http://www.56.com/u11/v_%s.html" %videoId
                title = etree.HTML(get_html(url)).xpath('//h1[@id="vh_title"]/text()')[0]

            elif swf_url.find("ku6.com") >= 0:
                video_type = "ku6"
                videoId = re.search(r'/refer/([\w\.]+)/', swf_url).groups()[0]
                url = "http://v.ku6.com/show/%s.html" %videoId
                title = etree.HTML(get_html(url, "gbk")).xpath('//meta[@name="title"]/@content')[0]

            elif swf_url.find("qiyi.com") >= 0:
                video_type = "iqiyi"
                videoId = re.search(r'\.com/(\w+)/', swf_url).groups()[0]
                info_url = 'http://cache.video.qiyi.com/v/%s' % videoId
                info_xml = get_html(info_url)
                title = re.search(u'<title><!\[CDATA\[\s*([^<]+)\s*\]\]></title>', info_xml).groups()[0]
                url = re.search(u'<videoUrl>([^<]+)</videoUrl>', info_xml).groups()[0]

            elif swf_url.find("pps.tv") >= 0:
                video_type = "pps"
                videoId = re.search(r'/sid/(\w+)/', swf_url).groups()[0]
                url = "http://ipd.pps.tv/play_%s.html" %videoId
                title = etree.HTML(get_html(url, "gbk")).xpath('//meta[@name="description"]/@content')[0]

            if videoId and url and title and video_type:
                ret.append(buildResource(url, title, channelId, videoId, video_type))
            else:
                print(swf_url)
                continue

        except Exception, e:
            print(swf_url, e)
            continue

    return ret



def buildResource(url, title, channelId, videoId, video_type):
    resource = Resource()
    resource['resourceName'] = title
    resource['resourceUrl'] = url
    resource['channelId'] = channelId
    #resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
    resource['type'] = 'video'
    resource['videoType'] = video_type
    resource['videoId'] =  videoId
    resource['createTime'] = getCurTime()

    return resource.getInsertDict()


if __name__ == '__main__':
    #pprint.pprint(handle('http://www.250.im/category/shipin/haofuli', 100128, 1))
    #pprint.pprint(handle('http://www.250.im/category/shipin/zhongkouwei', 100128, 1))
    #pprint.pprint(handle('http://www.hugebo.com/category/kaixinshipin', 100128, 1))
    pprint.pprint(handle('http://www.gaoxiaoing.com/archives/category/funnyscreen', 100128, 1))