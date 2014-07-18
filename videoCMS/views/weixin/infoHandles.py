#coding=utf-8
__author__ = 'ding'
from videoCMS.common.Domain import TextMsg, ImageMsg
from videoCMS.common.xml_dict import dict2xml,xml_tostring
from videoCMS.common.HttpUtil import get_html
from videoCMS.common.common import getWeixinToken
import json
from urllib2 import quote

def text(msg):
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




def image(msg):
    openid = msg['FromUserName']
    myid = msg['ToUserName']

    imageUrl = 'http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s' % (getWeixinToken(), msg['MediaId'])
    print imageUrl
    apiUrl = 'http://127.0.0.1/image/reco?q=' + quote(imageUrl)
    print(apiUrl)
    result = json.loads(get_html(apiUrl))
    res = TextMsg()
    res['ToUserName'] = openid
    res['FromUserName'] = myid
    res['Content'] = result['list'][0]['title']
    res = dict2xml('xml', res.getInsertDict())
    res = xml_tostring(res, 'utf-8')

    return res