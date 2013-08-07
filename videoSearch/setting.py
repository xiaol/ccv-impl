from pymongo import Connection

#con = Connection('60.28.29.37:20010')
con = Connection('192.168.0.37:20010')

clct_category  = con.tiercel.category
clct_channel  = con.tiercel.channel
clct_resource = con.tiercel.resource
clct_preresource = con.tiercel.preresource
clct_videoInfoTask = con.tiercel.videoInfoTask

APP_KEY = '3421733539'
TOKEN = '2.004t5RdCMuAbED17969f330diAZbaC'

FFMEPG = '/home/download/ffmpeg-1.1/ffmpeg'

MLDONKEY_DIR = '/root/.mldonkey/incoming/files'
MLDONKEY_D_DIR = '/root/.mldonkey/incoming/directories'
STORE_DIR = '/data/tiercel'
