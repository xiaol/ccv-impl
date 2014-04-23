#coding=utf-8

__author__ = 'Ivan liu'

import re,os,json
from videoCMS.common.HttpUtil import get_html,HttpUtil,get_raw_data
import base64,Image,StringIO
from videoCMS.views.resource import saveResourceImage
from videoCMS.common.common import getCurTime
from bs4 import BeautifulSoup

headers = [('User-agent','Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19 AppEngine-Google;'), ('Accept-Language', 'zh-TW,zh;q=0.8,en;q=0.6')]
p_1 = re.compile('>(.*)</a>')
def decode(imageUrl):
    httpUtil = HttpUtil({'http': 'http://127.0.0.1:8087'})
    httpUtil.opener.addheaders = headers
    mainRes = {}
    try:
        url = 'http://images.google.com/searchbyimage?image_url=%s&hl=zh-TW&lr=lang_zh-TW'%imageUrl
        print url
        content = httpUtil.Get(url)
        text_file = open("Output.html", "w")
	text_file.write(content)
	text_file.close()
        if content:
            result = content.decode('utf-8','ignore')
        else:
            result = ''
    except Exception,e:
        import traceback
        print traceback.format_exc()
        mainRes['msg'] = ' GET url failed.'

    try:
        soup = BeautifulSoup(result)
        topStuff = soup.find(id="topstuff")
        topStuff.style.decompose()
        topList = topStuff.find_all("a", class_="qb-b")
        if topList is not None and len(topList) != 0:
            topMatch = topList[0].text
            mainRes['topMatch'] = topMatch

        searchResult = soup.find(id="search")
        searchResult.style.decompose()
        searchResult.find(id="imagebox_bigimages").decompose()
        listHtml = searchResult.find_all("li")

        mainRes['list'] = []
        for li in listHtml:
            entity = {}
            entity['title'] = li.h3.a.text
            entity['thImg'] = li.find_all("div",class_="th")[0].img['src']
            entity['url'] = li.cite.text
            spans = li.find_all("span", class_="st")[0]
            spans.span.decompose()
            entity['des'] = spans.text
            mainRes['list'].append(entity)

    except Exception,e:
        import traceback
        print traceback.format_exc()
        mainRes['msg'] = ' Parse failed.'

    return mainRes

def parseMatch(result): #Html result
    start = result.find(u'這個圖片最有可能的推測結果')#'对该图片的最佳猜测')
    if start == -1:
        print '找不到最佳匹配'
        return []
    end = result.find(u'搜尋結果', start)
    bestGuess = result[start:end]
    match = p_1.findall(bestGuess)
    print match[0]
    return match

def reco(request):
    from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
    fileUrl = save(request)
    domain = re.sub(request.path, '', request.build_absolute_uri())
    fileUrl = domain + fileUrl
    print fileUrl
    #fileUrl = 'http://vipbook.sinaedge.com/bookcover/pics/55/cover_21d32033a72eb9902d3eba920258a942.jpg'
    data = decode(fileUrl)
    return HttpResponse(json.dumps(data))

def save(request):
    img = Image.open(parse(request.FILES.get('image')))
    sio = StringIO.StringIO()
    img.save(sio,'jpeg',quality=90)
    imageId = "rainbow"
    fileUrl = saveToDisk(sio.getvalue(), imageId)
    return fileUrl

#IMAGE_DIR = '/Users/liuivan/Workspace/huohua/videocms/videoCMS/static'
IMAGE_DIR = '/root/videocms/videoCMS/static'
def saveToDisk(img, id):
    date = getCurTime()[:8]
    filename = '%s/%s.jpg' % (date, id + getCurTime())

    fullpath = IMAGE_DIR + '/' + filename
    dir = os.path.dirname(fullpath)

    if not os.path.exists(dir):
        os.makedirs(dir)

    with open(fullpath, 'wb') as f:
        f.write(img)
    return '/media/'+filename


def parse(url_or_data):
    image_file = StringIO.StringIO(url_or_data.read())
    return image_file

if __name__ == '__main__':
    fileUrl = 'http://vipbook.sinaedge.com/bookcover/pics/55/cover_21d32033a72eb9902d3eba920258a942.jpg'
    decode(fileUrl)
