__author__ = 'ding'

import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.abspath(__file__)))]

from lxml import etree
import re,pprint,json
from common.HttpUtil import get_html
from setting import clct_resource
from Domain import SnsInfo

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





'''==================================='''


handleMap = {
    'www.56.com':w56
}
p_site = re.compile('http://([^/]+)/')


def extra_info(url,videoType,videoId):
    m = p_site.search(url)
    if not m:
        print '[ERROR] not available url'
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
    print extra_info('http://www.56.com/u77/v_OTQwMTc1OTQ.html','w56','OTQwMTc1OTQ')