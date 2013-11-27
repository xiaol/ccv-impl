__author__ = 'ding'
import json,urllib2


def writeLargePostData():
    with open('post.data','wb') as f:
        data = [{"121321312312":312312312312}]*30000
        s = {"request-body":{"uploadLog":{"datas":data,"uuid":""}},"request-head":{"platform":"android","uuid":"356979059552716","store":"","channel":"m91","deviceId":"356979059552716","version":"26"}}

        f.write(json.dumps(s))


def post():
    data = open('post.data').read()
    print data
    result = urllib2.urlopen('http://127.0.0.1:8080/system/system.do',data).read()
    print result

writeLargePostData()
post()