#coding=utf-8
import sys,os

sys.path += [os.path.dirname(os.path.dirname(os.path.dirname(__file__)))]

from pymongo import Connection
#import MySQLdb

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
clct_cmsEditor = con.tiercel.cmsEditor
clct_danmu = con.tiercel.danmu

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
IMG_INTERFACE = 'http://47.weiweimeishi.com/huohua_v2/imageinterfacev2/api/interface/image/disk/get/96/96/'
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
# ==================电视剧================
(r'http://www.youku.com/show_page/id_\\w+.html','search.youkuTv'),
(r'http://www.funshion.com/subject/\\d+','search.funshionTv'),
(r'http://www.letv.com/tv/\\d+.html','search.letvTv'),
(r'http://www.iqiyi.com/dianshiju/\\w+.html','search.iqiyiTv'),
#
(r'http://tv.sohu.com/s\\d{4}/\\w+/','search.sohuTv'),
(r'http://tv.sohu.com/s\\d{4}/\\d+/s\\d+','search.sohuTv'),
#
(r'http://www.pptv.com/page/\\d+.html','search.pptvTv'),
(r'http://v.qq.com/detail/\\w/\\w+.html','search.qqTv'),
(r'http://v.pps.tv/splay_\\d+.html','search.ppsTv'),
(r'http://www.wasu.cn/Tele/index/id/\\d+','search.wasuTv'),
#
# ==================综艺================
(r'http://www.youku.com/show_page/id_\\w+.html','search.youkuZongyi'),
(r'http://www.iqiyi.com/zongyi/\\w+.html','search.iqiyiZongyi'),
(r'http://tv.sohu.com/\\w+/','search.sohuZongyi'),
(r'http://www.funshion.com/subject/\\d+','search.funshionZongyi'),
(r'http://www.pptv.com/page/\\d+.html','search.pptvZongyi'),
(r'http://v.qq.com/variety/column/column_\\d+.html','search.qqZongyi'),
#
# ==================动漫================
(r'http://www.youku.com/show_page/id_\\w+.html','search.youkuDongman'),
(r'http://www.tudou.com/albumcover/[^/]+.html','search.tudouDongman'),
#
(r'http://tv.sohu.com/s\\d{4}/\\w+/','search.sohuDongman'),
(r'http://tv.sohu.com/s\\d{4}/\\d+/s\\d+','search.sohuDongman'),
#
(r'http://www.iqiyi.com/dongman/\\w+.html','search.iqiyiDongman'),
(r'http://www.funshion.com/subject/\\d+','search.funshionDongman'),
(r'http://www.letv.com/tv/\\d+.html','search.letvDongman'),
#
# ============ HOT ====================
(r'http://www.mtime.com/trailer/','search.mtimeTrailer'),
(r'http://www.youku.com/show_page/id_\\w+.html','search.youkuNews'),
# Todo
# search.jimu
# search.weibo
(r'http://\\w+.youku.com', 'search.youkuTop'),
(r'http://www.funshion.com/list/.*', 'search.funshionTop'),
(r'http://top.letv.com/\\w+.html', 'search.letvTop'),
(r'http://top.iqiyi.com/\\w+.html', 'search.iqiyiTop'),
(r'http://v.163.com/zixun', 'search.163Top'),
(r'http://\\w+.56.com', 'search.56Top'),
(r'http://\\w+.ku6.com', 'search.ku6Top'),
(r'http://tv.sohu.com/hotyule', 'search.sohuTop'),
(r'http://tops.wasu.cn/show/cid/\\d+','search.wasuTop'),
(r'http://hot.weibo.com/.*?v=\\d+','search.weiboHot'),
(r'http://www.m1905.com/rank/top/\\d+','search.m1905Top'),
#
# ============ 纪录片 ====================
(r'http://www.youku.com/show_page/id_\\w+.html','search.youkuJilupian'),
(r'http://tv.sohu.com/s\\d{4}/\\w+/','search.sohuJilupian'),
(r'http://www.iqiyi.com/jilupian/\\w+.html','search.iqiyiJilupian'),
#
# ============== 福利 =======================
(r'http://app.baomihua.com/u/\\d+','search.welfareBaomihua'),
(r'http://www.weipai.cn/icheck-square','search.weipaiSquare'),
(r'http://www.chaoku4.com/list/index\\d+.html','search.chaoku4List'),
(r'http://wo.poco.cn/alluregirls','search.PocoWo'),
#
# ==============  体育 =======================
(r'http://list.iqiyi.com/www/\\d+/[\\d-]+.html','search.iqiyiSport'),
(r'http://sports.sina.com.cn/.*','search.sinaSport'),
(r'http://cctv.cntv.cn/lm/tianxiazuqiu','search.cntvLM'),
#
#
# ==============  游戏 =======================
(r'http://www.aipai.com/game_gameid-\\d+.html','search.aipai'),
(r'http://kan.duowan.com/1212/m_\\d+.html','search.duowan'),
(r'http://v.qq.com/games/list/.*','search.qqList'),
#
# ============== 专辑 List =======================
(r'http://www.youku.com/playlist_show/id_\\d+.html','search.youkuPlayList'),
(r'http://www.56.com/w\\d+/album-aid-\\d+.html','search.56Album'),
(r'http://www.tudou.com/albumplay/\\w+.html','search.tudouAlbum'),
(r'http://fun.56.com/\\w+/','search.56list'),
(r'http://i.youku.com/u/\\w+/videos','search.youkuIyouku'),
(r'http://\\w+.youku.com/\\w+','search.youkuList'),
(r'http://www.tudou.com/cate/[\\w-]+.html','search.tudouCate'),
(r'http://v.ku6.com/playlist/index_\\d+.html','search.ku6Playlist'),
(r'http://list.iqiyi.com/www/\\d+/[\\d-]+.html','search.iqiyiList'),
(r'http://type.boosj.com/list/\\d+/','search.boosjList'),
(r'http://subject.boosj.com/subject_\\d+.html','search.boosjSubject'),
(r'http://v.ifeng.com/vlist/nav/\\w+/update/1/list.shtml','search.ifengList'),
(r'http://www.asmou.cn/videolist-do-tag-id-\\d+.html','search.asmouList'),
(r'http://www.acfun.tv/tag/\\d+.aspx','search.acfunTag'),
(r'http://i.56.com/\\w+/videos/.*','search.56I'),
(r'http://video.56.com/opera/\\d+.html','search.56Opera'),
(r'http://z.56.com/\\d+','search.56Town'),
(r'http://fashion.56.com/\\w+/','search.56Fashion'),
(r'http://ipd.pps.tv/\\d+','search.ppsIpd'),
(r'http://list.pptv.com/sort_list/[\\d-]+.html','search.pptvList'),
# embed
(r'http://www.pet-weibo.com/video/list-\\d+.html','search.petweiboList'),
(r'http://\\w+.joy.cn/videolist/[\\d_]+/1.htm','search.joyList'),
(r'http://v.qq.com/cover/\\d+/\\w+.html','search.qqCover'),
(r'http://ent.sina.com.cn/bn/.*','search.sinaEntList'),
(r'http://list.letv.com/list/.*.html','search.letvList'),
(r'http://so.letv.com/variety/\\d+.html','search.letvVar'),
(r'http://www.wasu.cn/Column/show/column/\\d+','search.wasuList'),
(r'http://www.wasu.cn/list/index/cid/\\d+','search.wasuList'),
(r'http://www.v1.cn/roll/1001/1.shtml','search.v1Paike'),
(r'http://www.v1.cn/roll/\\d+/1.shtml','search.v1List'),
(r'http://www.m1905.com/video/list/c\\d+.html','search.m1905List'),
#
#
# ============== 主页视频 =======================
(r'http://www.youku.com/','search.youkuIndex'),
(r'http://news.tudou.com/','search.tudouNewsIndex'),
(r'http://fun.56.com/','search.56fun'),
(r'http://travel.youku.com/food/','search.youkuTravel'),
(r'http://life.youku.com/cooking','search.youkuLife'),
(r'http://tech.youku.com/tansuo','search.youkuTech'),
(r'http://life.tudou.com/labeltop/zcal2rvv1oindwyq_s0p1.html','search.tudouLife'),
(r'http://domestic.kankanews.com/','search.kankanews'),
(r'http://mm.56.com/','search.56mm'),
(r'http://tv.sohu.com/tech/','search.sohuTech'),
(r'http://tv.sohu.com/baby/','search.sohuBaby'),
(r'http://tv.sohu.com/trends/\\w+/','search.sohuTrends'),
(r'http://www.everyshare.cn/category/wei/fun','search.everyshare'),
(r'http://kengdie.com/category/fun/','search.kengdie'),
(r'http://www.o2gzs.com/category/o2video','search.o2gzs'),
(r'http://g.tingcd.com/xiangsheng.html','search.tingcd'),
(r'http://www.tom61.com/xsxpfj/xssp/','search.tom61'),
(r'http://life.21cn.com/tv/list1.shtml','search.21cnLife'),
(r'http://v.766.com/other','search.766'),
(r'http://www.baomihua.com/funny_212','search.baomihuaFunny'),
(r'http://www.zealer.com/','search.zealer'),
(r'http://ent.letv.com/zt/scene/index.shtml','search.letvEntzt'),
(r'http://fashion.letv.com/zt/mfkt/index.shtml','search.letvFashionzt'),
(r'http://mv.yinyuetai.com/all','search.yinyuetaiMV'),
(r'http://v.163.com/special/.*.html','search.163Open'),
(r'http://v.163.com/paike/','search.163Paike'),
(r'http://www.m1905.com/video/prevues/','search.m1905Yugao'),
#
# ============== 视频搜索 =======================
(r'http://www.soku.com/search_video/.*','search.youkuSoku'),
(r'http://so.iqiyi.com/so/q_.*','search.iqiyiSo'),
(r'http://so.56.com/video/.*','search.56So'),
(r'http://so.tv.sohu.com/mts?.*','search.sohuSo'),
(r'http://www.wasu.cn/Search/show\\?k\\=.*','search.wasuSearch'),
#

]