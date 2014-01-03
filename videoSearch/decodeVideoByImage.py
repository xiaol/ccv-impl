#coding=utf-8
__author__ = 'Ivan liu'
from common.HttpUtil import get_html,HttpUtil
import re

p_1 = re.compile('>(.*)</a>')
def searchImage(imageUrl):
    result = get_html('http://images.google.com/searchbyimage?image_url=%s'%imageUrl)
    start = result.find('对该图片的最佳猜测')
    if start == -1:
        return
    end = result.find('搜索结果', start)
    bestGuess = result[start:end]
    match = p_1.findall(bestGuess)
    print bestGuess

if __name__ == '__main__':
   searchImage('http://47.weiweimeishi.com/huohua_v2/imageinterfacev2/api/interface/image/disk/get/96/96/videoCMS_resource_101641_20140103_52c64868cf99d664bd7e7a9d.jpg')
