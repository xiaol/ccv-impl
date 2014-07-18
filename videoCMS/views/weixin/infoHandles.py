#coding=utf-8
__author__ = 'ding'
from videoCMS.common.Domain import TextMsg, ImageMsg, NewsMsg
from videoCMS.common.xml_dict import dict2xml,xml_tostring
from videoCMS.common.HttpUtil import get_html
from videoCMS.common.common import getWeixinToken
from videoCMS.views import image
import json, re
from urllib2 import quote
import time

current_milli_time = lambda: int(round(time.time() * 1000))
def text(msg, request):
    openid = msg['FromUserName']
    content = msg['Content']
    myid = msg['ToUserName']

    res = TextMsg()
    res['ToUserName'] = openid
    res['FromUserName'] = myid
    res['Content'] = content
    res = dict2xml('xml', res.getInsertDict())
    res = xml_tostring(res, 'utf-8')

    return res


class FakeRequest(object):
    REQUEST = {}

def news(msg, request):
    openid = msg['FromUserName']
    myid = msg['ToUserName']

    #imageUrl = 'http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s' % (getWeixinToken(), msg['MediaId'])
    imageUrl = msg['PicUrl']
    fakeRequest = FakeRequest()
    fakeRequest.REQUEST['q'] = imageUrl
    print imageUrl
    #apiUrl = 'http://127.0.0.1/image/reco?q=' + quote(imageUrl)
    #print(apiUrl)
    response = image.reco(fakeRequest)
    result = json.loads(response.content)
    count = len(result.get('list',[]))
    if count == 0:
	res = TextMsg()
    	res['ToUserName'] = '![CDATA[' +openid +']]'
    	res['FromUserName'] = '![CDATA[' + myid + ']]'
    	res['Content'] = '![CDATA['+u'是'+result.get('matches',{}).get('match','')+'?' +']]'
        res['MsgType'] = '![CDATA[text]]'
        res['CreateTime'] = str(current_milli_time())
        #res['Content'] = res['Content'].encode('UTF-8')
    	res = dict2xml('xml', res.getInsertDict())
    	res = xml_tostring(res, 'utf-8')	
    else:
    	res = NewsMsg()
    	res['ToUserName'] = '![CDATA['+openid +']]'
    	res['FromUserName'] = '![CDATA[' +myid +']]'
        res['MsgType'] = '![CDATA[news]]'
        res['CreateTime'] = str(current_milli_time())
        if count >10: count = 10    
    	res['ArticleCount'] = str(count)
        Articles = ''
        for i in range(0,count):
            item = {}
            item['Title'] = '![CDATA['+result['list'][i]['title']+']]'
            #item['Title'] = result['list'][i]['title'].encode('UTF-8')
            item['Description'] = '![CDATA['+result['list'][i]['des'] +']]'
            #item['Description'] = result['list'][i]['des'].encode('UTF-8')
            item['PicUrl'] = '![CDATA['+result['list'][i]['thImg'] +']]'
            item['Url'] = '![CDATA['+result['list'][i]['url'] +']]'
            Articles += xml_tostring(dict2xml('item', item), 'utf-8')	
        print Articles
    	res = dict2xml('xml', res.getInsertDict())
    	res = xml_tostring(res, 'utf-8')
        res = res[:-6] + '<Articles>'+Articles + '</Articles>'+res[-6:]
        res = re.sub(r'!\[CD', '<![CD', res)
        res = re.sub(r'\]\]', ']]>', res)
    print res
    return res
