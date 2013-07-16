#coding=utf-8
import re
from lxml import etree
from HttpUtil import get_html
from Domain import Channel

def extraInfos(url):
    tree = etree.HTML(get_html(url))
    channel = Channel()
    channel['detailDoubanUrl'] = url
    
    docString =  etree.tostring(tree.xpath('//div[@id="info"]')[0],encoding='utf-8')
    content = re.sub('<.*?>','',re.sub('<br/>','\n',docString))
    content = content.decode('utf-8')
    for line in  content.split('\n'):
        line = line.strip()
        if len(line) == 0:
            continue
        key = line[:line.find(':')].strip()
        value = line[line.find(':') + 1:].strip()
        print key,value
        if key == u'导演':
            channel['detailDirecter'] = value
        elif key == u'主演':
            channel['detailLeadingRole'] = [one.strip() for one in value.split('/')]
        elif key == u'类型':
            channel['detailMovieCategory'] = [one.strip() for one in value.split('/')]
        elif key == u'制片国家/地区':
            channel['detailDistrict'] = value
        elif key == u'语言':
            channel['detailLanguage'] = value
        elif key == u'上映日期' or key == u'首播':
            channel['detailReleaseDate'] = value
        elif key == u'片长' or key == u'单集片长':
            channel['detailDuration'] = value
        else:
            print 'unrecongnize key:',key
    
    try:
        channel['detaildoubanScore'] = float(tree.xpath('//div[@id="interest_sectl"]//p/strong/text()')[0])
    except:
        pass
    try:
        channel['detailDescription'] = tree.xpath('//span[@property="v:summary"]')[0].text.strip()
    except:
        pass
    
    return channel.getUpdateDict()

if __name__ == '__main__':
    #print extraInfos('http://movie.douban.com/subject/6872273/')
    print extraInfos('http://movie.douban.com/subject/24849863/')
    