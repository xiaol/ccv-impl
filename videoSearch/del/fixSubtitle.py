#coding=utf-8
from setting import clct_channel


for channel in clct_channel.find():
    print channel['tvNumber']
    if channel['tvNumber'] == 0:
        continue
    subtitle = '已更新至:%s'%channel['tvNumber']

    clct_channel.update({'_id':channel['_id']} , {'$set':{'subtitle':subtitle}})