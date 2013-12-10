#coding=utf-8
import urllib2
import cookielib
import HTMLParser
import time
import traceback
import gzip
import StringIO
import json
import os
import sys
from PIL import Image
from setting import GIF_TEMP_DIR, clct_resource


class HttpUtil():
    def __init__(self,proxy = None):
        #proxy = {'http': 'http://210.14.143.53:7620'}
        if proxy != None:
            proxy_handler = urllib2.ProxyHandler(proxy)
            self.opener = urllib2.build_opener(proxy_handler,urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
        else:
            self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))

        self.opener.addheaders=[('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'),\
                                ]


    def Get(self,url,times=1,timeout=30):
        for i in range(times):
            try:
                resp = self.opener.open(url,timeout=timeout)
                return resp.read()
            except:
                time.sleep(1)
                print traceback.format_exc()
                continue
        
        return None
    
    def Post(self,url,data,times=1, timeout=30):
        for i in range(times):
            try:
                resp = self.opener.open(url,data,timeout=timeout)
                return resp.read()
            except:
                time.sleep(1)
                print traceback.format_exc()
                continue
        return None
    
    def real_url(self,url,times=1,timeout=30):
        for i in range(times):
            try:
                return self.opener.open(url,timeout=timeout).geturl()
            except:
                time.sleep(1)
                print traceback.format_exc()
                continue
        return None
    
    def unzip(self,data):
        import gzip
        import StringIO
        data = StringIO.StringIO(data)
        gz = gzip.GzipFile(fileobj=data)
        data = gz.read()
        gz.close()
        return data


def get_html(url,encoding='utf-8'):
    httpUtil = HttpUtil()
    content = httpUtil.Get(url)
    if content:
        print url
        return content.decode(encoding,'ignore')
    else:
        return ""

def get_gzip_html(url, encoding='utf-8'):
    httpUtil = HttpUtil()
    content = httpUtil.Get(url)
    try:
        data = StringIO.StringIO(content)
        gz = gzip.GzipFile(fileobj=data, mode="r")
        content = gz.read()
        gz.close()
    except:
        content = gz.extrabuf
        gz.close()

    if content:
        return content.decode(encoding)
    else:
        return ""

def getVideoIdByUrl(url):
    httpUtil = HttpUtil()
    data = {'url':url}
    data = json.dumps(data)
    ret = httpUtil.Post('http://60.28.29.38:9090/api/getVideoId', data)
    
    return json.loads(ret)["videoId"]

def getVideoInfoByUrl(url):
    httpUtil = HttpUtil()
    data = {'url':url}
    data = json.dumps(data)
    ret = httpUtil.Post('http://60.28.29.38:9090/api/getVideoId', data)

    return json.loads(ret)


def getFrameFromGif(gif_path):
    try:
        im = Image.open(gif_path)
        im.seek(0)
        frame = im.copy()
        png_path = gif_path.rstrip('gif') + 'png'
        frame.save(png_path, **frame.info)
        return png_path
    except Exception, e:
        print(e)
        return None


def downloadGif(url, channelId):
    #跳过已经存在的gif
    cursor = clct_resource.find({'resourceUrl': url})
    if cursor.count() > 0:
        return None, None

    relative_dir = 'videoCMS/gifResource/' + str(channelId)
    gif_dir = os.path.join(GIF_TEMP_DIR, relative_dir)
    if not os.path.exists(gif_dir):
        os.makedirs(gif_dir)
    filename = url.split('/')[-1].replace('_', '-')
    # filename = str(time.time()).replace('.', '_') + url.split('/')[-1]
    gif_path = os.path.join(gif_dir, filename)
    httpUtil = HttpUtil()
    gif = httpUtil.Get(url, times=3)
    if gif:
        f = file(gif_path, "wb")
        f.write(gif)
        f.close()
        relative_path = os.path.join(relative_dir, filename)
        #get first image of gif
        png_path = getFrameFromGif(gif_path)
        if png_path:
            relative_image_path = relative_path.rstrip('gif') + 'png'
            return relative_path.replace('/', '_'), relative_image_path.replace('/', '_')
        else:
            return relative_path.replace('/', '_'), None
    else:
        return None, None


if __name__ =='__main__':
    httpUtil = HttpUtil()
    content = httpUtil.Get('http://lol.duowan.com/1108/m_178050471525.html')
    print httpUtil.unzip(content)
    print len(content)