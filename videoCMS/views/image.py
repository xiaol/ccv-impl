#coding=utf-8

__author__ = 'Ivan liu'

import re,os,json, urllib2
from videoCMS.common.HttpUtil import get_html,HttpUtil,get_raw_data
import base64,Image,StringIO
from videoCMS.common.common import getCurTime
from bs4 import BeautifulSoup

headers = [('User-agent','Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19 AppEngine-Google;'),
           ('Accept-Language', 'zh-TW,zh;q=0.8,en;q=0.6'), ("Accept-Encoding", "gzip")]
p_1 = re.compile('>(.*)</a>')
import gzip

def decode(imageUrl, queryStr=''):
    #httpUtil = HttpUtil({'https': 'https://127.0.0.1:8087'})
    #httpUtil = HttpUtil({'https': 'https://213.184.97.221:56745'})
    httpUtil = HttpUtil({'https': 'https://xiao:green423TREE@hongkong.wonderproxy.com:11000'})
    #httpUtil = HttpUtil({'https': 'https://94.205.49.41:80'})
    httpUtil.opener.addheaders = headers
    mainRes = {}
    try:
        if queryStr == '':
            queryStr = urllib2.quote(queryStr)+ urllib2.quote('site:taobao.com')
        else:
            queryStr = urllib2.quote(queryStr)+ urllib2.quote(' OR  site:taobao.com')
        imageUrl = urllib2.quote(imageUrl)
        url = 'https://images.google.com/searchbyimage?image_url=%s&hl=zh-CN&lr=lang_zh-CN&cr=countryCN&oq=%s'%(imageUrl, queryStr)
	print url
        content = httpUtil.Get(url)
        text_file = open("Output.html", "w")
        text_file.write(content)
        text_file.close()

        buf = StringIO.StringIO(content)
        f = gzip.GzipFile(fileobj=buf)
        content = f.read()
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
        if topStuff.sytle is not None:
            topStuff.style.decompose()
        topList = topStuff.find_all("a", class_="qb-b")
        if topList is not None and len(topList) != 0:
            topMatch = topList[0].text
            mainRes['topMatch'] = topMatch

        searchResult = soup.find(id="search")
        if searchResult.style is not None:
       	    searchResult.style.decompose()
        similarContent = searchResult.find(id="imagebox_bigimages").extract()
        listHtml = searchResult.find_all("li")

        mainRes['list'] = []
        for li in listHtml:
            entity = {}
            entity['title'] = li.h3.a.text
            tmp = li.find_all("div", class_="th")
            if not tmp:
		continue
            entity['thImg'] = tmp[0].img['src']
            entity['url'] = li.h3.a['href']
            spans = li.find_all("span", class_="st")[0]
            if spans.span is not None:
            	spans.span.decompose()
            entity['des'] = spans.text
            mainRes['list'].append(entity)

        similarList = similarContent.find_all("li")
        mainRes['similar'] = []
        for li in similarList:
            entity = {}
            entity['url'] = li.img['title']
            divList = li.find_all('div')
            detail = json.loads(divList[-1].text)
            entity['thImg'] = detail['ou']
            entity['title'] = detail['pt']
            mainRes['similar'].append(entity)


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

wordsDict = {}
def initWords():
    words = open("videoCMS/samples/image-net-2012.words")
    i = 0
    for line in words.readlines():
	wordList = line.split(',')
	wordsDict[i] = line
	i += 1


def reco(request):
    from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
    import cnnclassify
    import timeit
    fileUrl, fullpath = save(request)
    domain = re.sub(request.path, '', request.build_absolute_uri())
    fileUrl = domain + fileUrl
    print fileUrl
    start = timeit.default_timer()
    #fileUrl = 'http://vipbook.sinaedge.com/bookcover/pics/55/cover_21d32033a72eb9902d3eba920258a942.jpg'
    results =  cnnclassify.cnnclassify(fullpath.encode('utf8'), "videoCMS/samples/image-net-2012.sqlite3".encode('utf8'))
    #cnnclassify.end()
    stop = timeit.default_timer()
    print stop - start 
    if not wordsDict:
	initWords()
    matches = []
    sortedKeys = sorted(results.keys(), reverse=True)
    for key in sortedKeys:
        matches.append(wordsDict[results[key]])# "%.6f" % v
    start = timeit.default_timer()
    queryStr = ''
    for i in range(0,len(sortedKeys)-1):
        if sortedKeys[i] > 0.1:
            if i != 0:
                queryStr = queryStr+' OR '  
            queryStr = queryStr + '('+' OR'.join(matches[i].replace('\n','').split(',')) + ')'
    print queryStr
    if sortedKeys[0] > 0.1:  
    	data = decode(fileUrl,queryStr)
    else: data = decode(fileUrl)
    stop = timeit.default_timer()
    print stop - start
    data['matches'] = matches
    data['matchConfidences'] = sortedKeys
    return HttpResponse(json.dumps(data))

def save(request):
    print request.body
    print request
    print request.REQUEST
    if request.META.get('HTTP_ACCEPT', None) == 'gzip':
        buf = parse(request.FILES.get('image'))
        f = gzip.GzipFile(fileobj=buf)
        content = f
    else: content = parse(request.FILES.get('image'))
    img = Image.open(content)
    sio = StringIO.StringIO()
    img.save(sio,'jpeg',quality=90)
    imageId = "rainbow"
    fileUrl,fullpath = saveToDisk(sio.getvalue(), imageId)
    return fileUrl, fullpath

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
    f.close()
    return '/media/'+filename, fullpath


def parse(url_or_data):
    print url_or_data
    image_file = StringIO.StringIO(url_or_data.read())
    return image_file

if __name__ == '__main__':
    fileUrl = 'http://vipbook.sinaedge.com/bookcover/pics/55/cover_21d32033a72eb9902d3eba920258a942.jpg'
    print decode(fileUrl)
