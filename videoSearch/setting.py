from pymongo import Connection

debug = False

if not debug:
    con = Connection('h37:20010')
else:
    con = Connection('60.28.29.37:20010')

clct_category  = con.tiercel.category
clct_channel  = con.tiercel.channel
clct_resource = con.tiercel.resource
clct_preresource = con.tiercel.preresource
clct_videoInfoTask = con.tiercel.videoInfoTask
clct_userWeibo = con.tiercel.userWeibo
clct_userRecommend = con.tiercel.userRecommend
clct_user = con.tiercel.user


if not debug:
    logCon = Connection('h39:20010')
else:
    logCon = Connection('60.28.29.39:20010')

clct_playLog = logCon.tiercel.playLog
clct_searchLog = logCon.tiercel.searchLog

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
