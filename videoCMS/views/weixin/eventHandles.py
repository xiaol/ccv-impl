#coding=utf-8
__author__ = 'ding'

from videoCMS.common.xml_dict import dict2xml,xml_tostring
from videoCMS.common.Domain import TextMsg

def subscribe(msg):
    openid = msg['FromUserName']
    myid = msg['ToUserName']

    res = TextMsg()
    res['ToUserName'] = openid
    res['FromUserName'] = myid
    res['Content'] = u"欢迎来到微猜，在这可以和好友一起猜世界杯比赛，看谁胜谁败，谁是预测帝"
    res = dict2xml('xml', res.getInsertDict())
    res = xml_tostring(res, 'utf-8')

    return res


def unsubscribe(msg):
    openid = msg['FromUserName']
    myid = msg['ToUserName']

    return ''

def default(msg):
    return ''