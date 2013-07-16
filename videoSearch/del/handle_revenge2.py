#coding=utf-8
from common.Domain import Resource
from common.HttpUtil import get_html
from lxml import etree
from pprint import pprint
from common.common import getCurTime
import re
from setting import clct_channel

p_vid = re.compile('"videoId":"(\w+?)",')


def handle(url,channelId):
    detailPageList = handleListPage(url)
    return handleDetailPage(detailPageList,channelId)


def handleListPage(url):
    item = {'title':'','url':''}
    tree = etree.HTML(get_html(url))
    nodes = tree.xpath('//div[@class="list_block1 align_c"]//li/a')
    ans = []
    for node in nodes:
        item = {}
        item['title'] = node.xpath('./img/@title')[0]
        item['url'] = node.xpath('./@href')[0]
        ans.append(item)
        pprint(ans)
    return ans



def handleDetailPage(itemList,channelId):
    ans = []
    for item in itemList:
        resource = Resource()
        #...
        resource['resourceName'] = item['title']
        resource['resourceUrl'] = item['url']
        resource['channelId'] = channelId
        resource['categoryId'] = clct_channel.find_one({'channelId':resource['channelId']})['channelType']
        resource['videoId'] = p_vid.search(get_html(item['url'])).groups()[0]
        resource['videoType'] = 'iqiyi'
        resource['createTime'] = getCurTime()

        #...
        ans.append(resource.getInsertDict())
        pprint(resource.getInsertDict())
    return ans