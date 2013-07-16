#coding=utf-8
from Domain import Resource
from HttpUtil import get_html

def handleListPage(url):
    item = {'title':'','url':''}
    
    return [item]



def handleDetailPage(itemList,channelId):
    ans = []
    for item in itemList:
        resource = Resource()
        #...
        
        #...
        ans.append(resource.getInsertDict())
    return ans