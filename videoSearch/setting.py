from pymongo import Connection,MongoClient

con = MongoClient('60.28.29.37:20010', replicaset='huohuaSet')

clct_category  = con.tiercel.category
clct_channel  = con.tiercel.channel
clct_resource = con.tiercel.resource
clct_preresource = con.tiercel.preresource
clct_videoInfoTask = con.tiercel.videoInfoTask
clct_userWeibo = con.tiercel.userWeibo
clct_userRecommend = con.tiercel.userRecommend
clct_user = con.tiercel.user
clct_tag = con.tiercel.tag
clct_userDiscard = con.tiercel.UserDiscard
clct_tagCloud = con.tiercel.tagCloud


logCon = MongoClient('60.28.29.39:20010')


clct_playLog = logCon.tiercel.playLog
clct_searchLog = logCon.tiercel.searchLog
clct_playViewRateLog = logCon.tiercel.playViewRateLog
clct_netspeed = logCon.tiercel.netspeed

APP_KEY = '3421733539'
TOKEN = '2.004t5RdCMuAbED17969f330diAZbaC'

FFMEPG = '/home/download/ffmpeg-1.1/ffmpeg'

MLDONKEY_DIR = '/root/.mldonkey/incoming/files'
MLDONKEY_D_DIR = '/root/.mldonkey/incoming/directories'
STORE_DIR = '/data/tiercel'

GIF_TEMP_DIR = '/data/img'
GIF_SERVER_DIR = '/data/img/videoCMS/gifResource'
GIF_SERVER = 'root@60.28.29.47'
GIF_SERVER_PORT = 33470


if __name__ == '__main__':
    clct_channel.update(
    {'channelId': 101742},
    {'$set':
         {'tvNumber': u'12-30\u671f', 'updateTime': '20131111122447', 'subtitle': '12-30\xe6\x9c\x9f'}
    }
    )
