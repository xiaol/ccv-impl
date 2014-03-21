#coding=utf-8
__author__ = 'ding'

import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

from lxml import etree
import re,pprint,json
from common.HttpUtil import get_html
from setting import clct_resource
from Domain import SnsInfo
import urllib2
import time


'''===================== w56  ===================='''

p_w56 = re.compile('(\{.*\})')

def w56(url,videoType,videoId):
    info = SnsInfo()
    data = get_html('http://vv.56.com/stat/flv.php?id=%s&pct=1'%videoId)
    data = p_w56.search(data).groups()[0].replace("'",'"')
    d = json.loads(data)['data']
    info['up'] = d['ups']
    info['down'] = d['downs']
    info['play'] = d['times']

    data = get_html('http://comment.56.com/trickle/api/commentApi.php?a=flvLatest&vid=%s&pct=1&page=1'%videoId)
    c = json.loads(data)
    info['comment'] = c['ctTotal']

    return info.getInsertDict()

p_youku_up = re.compile(r'upVideoTimes">([\d,]+?)<')
p_youku_down = re.compile(r'downVideoTimes">([\d,]+?)<')


'''===================== youku  ===================='''

def youku(url,videoType,videoId):
    info = SnsInfo()
    html = get_html(url)
    info['up'] = int(p_youku_up.search(html).groups()[0].replace(',',''))
    info['down'] = int(p_youku_down.search(html).groups()[0].replace(',',''))

    data = json.loads(get_html('http://v.youku.com/QVideo/~ajax/getVideoPlayInfo?id=%s&type=vv'%videoId))
    info['play'] = data['vv']
    #TODO:  评论 http://comments.youku.com/comments/~ajax/getStatus.html?__ap=%7B%22videoid%22%3A%22171373670%22%2C%22oldSid%22%3A-1%7D
    #获取 vid http://v.youku.com/player/getPlayList/VideoIDS/XNjg1NDk0Njgw

    return info.getInsertDict()



'''===================== iqiyi  ===================='''

p_iqiyi_play = re.compile(r'"\d+":(\d+?)}')
p_up = re.compile(r'"down":(\d+)')
p_down = re.compile(r'"up":(\d+)')

def iqiyi(url,videoType,videoId):
    info = SnsInfo()
    tvid,videoId = videoId.split('__')
    html = get_html('http://cache.video.qiyi.com/pc/ext/%s/playCount_%s'%(tvid,tvid))
    info['play'] = int(p_iqiyi_play.search(html).groups()[0])

    html = get_html('http://up.video.iqiyi.com/ugc-updown/quud.do?type=2&dataid=%s'%tvid)
    info['up'] = int(p_up.search(html).groups()[0])
    info['down'] = int(p_down.search(html).groups()[0])

    return info.getInsertDict()


'''===================== ifeng  ===================='''
p_createTime = re.compile(u'发布:(\d{4,4}-\d{2,2}-\d{2,2} \d{2,2}:\d{2,2}:\d{2,2})')
extra_num = lambda s:int(re.search('(\d+)',s).groups()[0])

def ifeng(url,videoType,videoId):
    info = SnsInfo()
    html = get_html(url)
    sTime = p_createTime.search(html).groups()[0]
    info['createTime'] = sTime.replace(':','').replace('-','').replace(' ','')
    info['up'] = extra_num(get_html('http://survey.news.ifeng.com/getaccumulator_ext.php?key=%sding&format=json'%videoId))
    info['down'] = extra_num(get_html('http://survey.news.ifeng.com/getaccumulator_ext.php?key=%scai&format=json'%videoId))
    info['play'] = extra_num(get_html('http://survey.news.ifeng.com/getaccumulator_weight.php?format=json&serverid=2&key=%s'%videoId))
    info['comment'] = extra_num(get_html('http://comment.ifeng.com/getv.php?job=3&format=json&docurl=%s'%urllib2.quote(url)))
    return info.getInsertDict()





'''===================== common  ===================='''

handleMap = {
    'www.56.com':w56,
    'v.youku.com':youku,
    'www.iqiyi.com':iqiyi,
    'v.ifeng.com':ifeng,

}
p_site = re.compile('http://([^/]+)/')


def extra_info(url,videoType,videoId):
    m = p_site.search(url)
    if not m:
        print '[ERROR] not available page'
        return None
    site = m.groups()[0]
    if site not in handleMap:
        print '[ERROR] site: %s not support'%site
        return None
    try:
        return handleMap[site](url,videoType,videoId)
    except:
        print '[ERROR]',__file__,'when handle',url
        import traceback
        print traceback.format_exc()
    return None


if __name__ == '__main__':
    #print extra_info('http://www.56.com/u77/v_OTQwMTc1OTQ.html','w56','OTQwMTc1OTQ')
    #print extra_info('http://v.youku.com/v_show/id_XNjg1NDk0Njgw.html?f=22039479','youku','XNjg1NDk0Njgw')
    #print extra_info('http://www.iqiyi.com/v_19rrh50nj0.html','iqiyi','230201200__866c709dbbfa62f873a7bdb9e3f3951f')
    print extra_info('http://v.ifeng.com/ent/mingxing/2014003/0114b6d6-5c85-4362-a731-8f690fb1b444.shtml','ifeng','0114b6d6-5c85-4362-a731-8f690fb1b444')