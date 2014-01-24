#coding=utf-8
import sys,os

sys.path += [os.path.dirname(os.path.dirname(os.path.dirname(__file__)))]

from pymongo import Connection
import MySQLdb

con = Connection('60.28.29.37:20010')
#clct_channel  = con.iDown.yChannel
#clct_resource = con.iDown.yResource
#clct_tag      = con.iDown.tag
clct_category  = con.tiercel.category
clct_channel  = con.tiercel.channel
clct_user  = con.tiercel.user
clct_resource = con.tiercel.resource
clct_preresource = con.tiercel.preresource
clct_tag      = con.tiercel.tag
clct_cdnSync  = con.tiercel.cdnSync
clct_videoInfoTask = con.tiercel.videoInfoTask
clct_cronJob = con.tiercel.cronJob
clct_cmsMessage = con.tiercel.cmsMessage
clct_topic = con.tiercel.topic
clct_setting = con.tiercel.setting

con39 = Connection('60.28.29.39:20010')
clct_operationLog = con39.tiercel.operationLog
clct_statisticsLog = con39.tiercel.statisticsLog
clct_subscribeLog = con39.tiercel.subscribeLog
clct_searchLog = con39.tiercel.searchLog
clct_playLog = con39.tiercel.playLog

#==================
try:

    pass
except Exception,e:
    import traceback
    print traceback.format_exc()
    mysql_con = None

#=======================  图片
IMG_INTERFACE = 'http://47.weiweimeishi.com/huohua_v2/imageinterfacev2/api/interface/image/disk/get/96/*/'
IMG_INTERFACE_FF = 'http://47.weiweimeishi.com/huohua_v2/imageinterfacev2/api/interface/image/disk/get/%s/%s/%s'


IMAGE_DIR = '/data/img'


CHANNEL_IMAGE_WIDTH = 400
CHANNEL_IMAGE_HEIGHT = 300


#=======================  jpush 推送
from jpush import JPushClient

JPUSH_USERNAME = 'huohuadiandian'
JPUSH_APP_KEY = 'b34412ab2f0a5dc6aad20571'
JPUSH_MASTER_KEY = '7d956e6ac5635c9a604cff88'

jPushClient = JPushClient(JPUSH_USERNAME,JPUSH_MASTER_KEY)


#==========================


#==========================
from videoCMS.common.db import getCategoryList
CHANNEL_TYPE_LIST = getCategoryList()



CATEGORY_TYPE_MAP = {
u'人工':1,
u'强兴趣':2,
u'电影':3,
u'追剧':4,
u'短兴趣':5,
u'长兴趣':6,
}

CATEGORY_VIDEO_CLASS_MAP = {
    u"电影":0,
    u"电视剧":1,
    u"短视频":2,
    u'综艺':3,
    u'游戏':4,
    u"GIF":5
}


userList = [
('admin','huohua123456'),
('editor','123456'),
]


searchHandleListAll = [
'searchYyetsEd2k.yyetsTv',

'search.youkuTv',
'search.funshionTv',
'search.letvTv',
'search.iqiyiTv',
'search.sohuTv',
'search.pptvTv',
'search.qqTv',
'search.wasuTv',

'search.youkuZongyi',
'search.iqiyiZongyi',
'search.sohuZongyi',
'search.funshionZongyi',
'search.pptvZongyi',
'search.qqZongyi',

'search.youkuDongman',
'search.tudouDongman',
'search.sohuDongman',
'search.iqiyiDongman',
'search.funshionDongman',
'search.letvDongman',

'search.youkuJilupian',
'search.sohuJilupian',
'search.iqiyiJilupian',

'search.welfareBaomihua',
'search.weipaiSquare',
'search.chaoku4List',

'search.iqiyiSport',
'search.sinaSport',
'search.aipai',

'search.youkuPlayList',
'search.youkuSoku',
'search.56Album',
'search.tudouAlbum',
'search.tudouNewsIndex',
'search.youkuIndex',
'search.56fun',
'search.56list',
'search.youkuIyouku',
'search.youkuTravel',
'search.youkuLife',
'search.youkuTech',
'search.youkuList',
'search.tudouCate',
'search.tudouLife',
'search.ku6Playlist',
'search.iqiyiSo',
'search.iqiyiList',
'search.56So',
'search.weiboHot',
'search.boosjList',
'search.boosjSubject',
'search.ppsTv',
'search.ifengList',
'search.kankanews',
"search.asmouList",
"search.acfunTag",
"search.56I",
"search.56Opera",
"search.56Town",
"search.56mm",
"search.56Fashion",
"search.sohuSo",
"search.sohuTech",
"search.sohuTrends",
"search.sohuBaby",
"search.ppsIpd",
"search.pptvList",
"search.embed",
"search.petweiboList",
"search.everyshare",
"search.kengdie",
"search.o2gzs",
"search.tingcd",
"search.tom61",
"search.21cnLife",
"search.766",
"search.duowan",
"search.joyList",
"search.baomihuaFunny",
"search.zealer",
"search.qqList",
"search.qqCover",
"search.sinaEntList",
"search.letvEntzt",
"search.letvFashionzt",
"search.letvList",
"search.letvVar",
"search.yinyuetaiMV",
"search.163Open",
"search.163Paike",
"search.youkuTop",
"search.funshionTop",
"search.letvTop",
"search.iqiyiTop",
"search.163Top",
"search.56Top",
"search.ku6Top",
"search.sohuTop",
'search.wasuTop',
'search.wasuSearch',
'search.wasuList',
'search.v1List',
'search.v1Paike',
'search.m1905List',
'search.m1905Top',
'search.m1905Yugao',

"searchGif.onegif",
"searchGif.forgifs",
]