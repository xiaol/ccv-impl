#coding=utf-8 
__author__ = 'Ivan liu'

import re,os,json, urllib2
from videoCMS.common.HttpUtil import get_html,HttpUtil,get_raw_data
import base64,Image,StringIO
from videoCMS.common.common import getCurTime
from bs4 import BeautifulSoup
from textblob import TextBlob
headers = [('User-agent','Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19 AppEngine-Google;'),
           ('Accept-Language', 'zh-TW,zh;q=0.8,en;q=0.6'), ("Accept-Encoding", "gzip")]
p_1 = re.compile('>(.*)</a>')
import gzip

IMAGE_DIR = '/home/azureuser/ccv-impl/videoCMS/static'
httpUtils = []
def decode(imageUrl, queryStr=''):
    httpUtil = HttpUtil()
    #httpUtil = HttpUtil({'https': 'https://127.0.0.1:8087'})
    #httpUtil1 = HttpUtil({'https': 'https://213.184.97.221:56745'})
    httpUtil1 = HttpUtil({'https': 'https://xiao:green423TREE@hongkong.wonderproxy.com:11000'})
    httpUtils.append(httpUtil)
    httpUtils.append(httpUtil1)
    #httpUtil = HttpUtil({'https': 'https://94.205.49.41:80'})
    httpUtil.opener.addheaders = headers
    mainRes = {}
    try:
        if queryStr == '':
            queryStr = urllib2.quote(queryStr)#+ urllib2.quote('site:taobao.com')
        else:
            queryStr = urllib2.quote(queryStr)#+ urllib2.quote(' OR site:taobao.com')
        imageUrl = urllib2.quote(imageUrl)
        url = 'https://images.google.com/searchbyimage?image_url=%s&hl=zh-CN&lr=lang_zh-CN&cr=countryCN&q=%s&oq=%s'%(imageUrl, queryStr, queryStr)
	print url
        for i in range(2):
            for util in httpUtils:
       	        content = util.Get(url)
                if content is not None:
                    break
            if content is not None:
		break
        
        buf = StringIO.StringIO(content)
        f = gzip.GzipFile(fileobj=buf)
        content = f.read()
        if content:
            result = content.decode('utf-8','ignore')
        else:
            result = ''
        text_file = open("Output.html", "w")
        text_file.write(content)
        text_file.close()

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
        similarContent = searchResult.find(id="imagebox_bigimages")
 	similarList = []
        if similarContent is not None:
            similarContent.extract()
            similarList = similarContent.find_all("li")

        listHtml = searchResult.find_all("li")
        mainRes['list'] = []
	import re
        for li in listHtml:
            entity = {}
            entity['title'] = li.h3.a.text
            tmp = li.find_all("div", class_="th")
            if not tmp:
	        continue
            import urlparse
          
            parsed = urlparse.urlparse(tmp[0].a['href'])
            entity['thImg'] = urlparse.parse_qs(parsed.query)['imgurl'][0]#re.sub(r'https://encrypted-tbn\d','https://t3', tmp[0].img['src'])
            print entity['thImg']

            entity['url'] = li.h3.a['href']
            spans = li.find_all("span", class_="st")[0	]
            if spans.span is not None:
            	spans.span.decompose()
            entity['des'] = spans.text
            mainRes['list'].append(entity)
          
       
        mainRes['similar'] = []
        for li in similarList:
            entity = {}
            entity['url'] = li.img['title']
            divList = li.find_all('div')
            detail = json.loads(divList[-1].text)
            #entity['thImg'] = re.sub(r'https://encrypted-tbn\d','https://t3', detail['tu'])
            entity['thImg'] = detail['ou']
            print entity['thImg']
            entity['title'] = detail['pt']
            if 'MB' in detail['os']:
		continue
	    elif 'KB' in detail['os']:
                detail['os'] = detail['os'].replace('KB','')
		if float(detail['os']) > 100.0 or float(detail['os']) < 5.0:
                   continue
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
    words = open("data/ilsvrc12/synset_words.txt")
    i = 0
    for line in words.readlines():
	wordList = line.split(',')
        #blob = TextBlob(line[10:])
        #zh_blob = blob.translate(to="zh") 
        #print zh_blob
	#wordsDict[i] = str(zh_blob)
	wordsDict[i] = line[10:]
	i += 1

import caffe

caffe_root = '../'  # this file is expected to be in {caffe_root}/examples

# Set the right path to your model definition file, pretrained model weights,
# and the image you would like to classify.
MODEL_FILE = 'imagenet/imagenet_deploy.prototxt'
PRETRAINED = 'imagenet/caffe_reference_imagenet_model'
IMAGE_FILE = 'images/cat.jpg'

from initNet import net
def reco(request):
    from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
    import timeit
    if request.REQUEST.get('q', '') != '':
        print 'q:'+request.REQUEST.get('q', '')
        date = getCurTime()[:8]
    	filename = '%s/%s.jpg' % (date, 'rainbow' + getCurTime())
    	fullpath = IMAGE_DIR + '/' + filename
        fileUrl = request.REQUEST['q']
        import urllib
        try:
            urllib.urlretrieve(fileUrl, fullpath)
        except Exception,e:
            print e
            return
    else:
    	if not hasattr(request, 'FILES') or request.FILES.get('image',None) is None: 
            return 
    #import cnnclassify
    	fileUrl, fullpath = save(request)
    	absoluteUrl = re.sub('http://','',request.build_absolute_uri())
    	domain = re.sub(request.path, '', absoluteUrl)
    	print request.path, ' ', request.build_absolute_uri()
    	print domain
    	fileUrl = 'http://'+domain + fileUrl
    print fileUrl
   
    start = timeit.default_timer()
    input_image = caffe.io.load_image(fullpath.encode('utf8'))
    prediction = net.predict([input_image]) 
    print 'prediction shape:', prediction[0].shape
    maxScore = -1
    maxIndice = -1
    for i in range(0,len(prediction[0])-1):
        entity = prediction[0][i]
        if maxScore < entity:
            maxScore = entity
            maxIndice = i
    print maxIndice, maxScore
    results =  {str(maxScore):maxIndice}#cnnclassify.cnnclassify(fullpath.encode('utf8'), "videoCMS/samples/image-net-2012.sqlite3".encode('utf8'))
    #cnnclassify.end()
    stop = timeit.default_timer()
    print stop - start 
    if not wordsDict:
	initWords()
    matches = []
    sortedKeys = sorted(results.keys(), reverse=True)
    for key in sortedKeys:
        matches.append(wordsDict[results[key]]) 
    start = timeit.default_timer()
    queryStr = ''
    print sortedKeys
    for i in range(0,len(sortedKeys)):
        if float(sortedKeys[i]) > 0.3 and i == 0:
            if i != 0:
                queryStr = queryStr+' OR '  
            queryStr = queryStr + '('+' OR'.join(matches[i].replace('\n','').split(',')) + ')'
    print 'query ',queryStr
    if float(sortedKeys[0]) > 0.6:  
    	data = decode(fileUrl,queryStr)
    else: data = decode(fileUrl)
    stop = timeit.default_timer()
    print stop - start
    data['matches'] = [] 
    for j in range(0, len(matches)):
	data['matches'].append({'match':matches[j], 'confidence':sortedKeys[j]})
    #data['matchConfidences'] = sortedKeys
    data['imageUrl'] = fileUrl
    return HttpResponse(json.dumps(data))

def save(request):
    #print request.body
    #print request
    #print request.REQUEST
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
#IMAGE_DIR = '/root/videocms/videoCMS/static'
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
