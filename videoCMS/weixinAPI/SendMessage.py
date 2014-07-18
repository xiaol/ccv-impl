#coding=utf-8
__author__ = 'ding'
import urllib2
import json
from videoCMS.conf import WX_MESSAGE_CUSTOM_SEND
from videoCMS.common.common import getWeixinToken

def SendMessage(msg):
    token = getWeixinToken()
    url = WX_MESSAGE_CUSTOM_SEND % token
    post = json.dumps(msg, encoding='utf-8', ensure_ascii=False)
    post = post.encode()
    data = json.loads(urllib2.urlopen(url, post ).read())
    return data


def SendTextMessage(openid, text):
    data = {
        "touser": openid,
        "msgtype":"text",
        "text":
        {
             "content": text
        }
    }
    return SendMessage(data)


if __name__ == '__main__':
    print SendTextMessage('o_OYHt9WRe2PdluJFxrCjx8q2pyQ',u'Carl吴国鸿点击了你的推广~<a href="http://baidu.com">dd</a>')