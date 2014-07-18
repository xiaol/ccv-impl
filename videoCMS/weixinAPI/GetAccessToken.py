import sys
import os

sys.path += [os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))]
import urllib2
import json
from conf import WX_APP_ID,WX_APP_SECRET,WX_ACCESS_TOKEN_URL
from conf import clct_setting
from common.Domain import Setting
from common.common import getCurTime


def GetAccessToken():
    url = WX_ACCESS_TOKEN_URL % (WX_APP_ID, WX_APP_SECRET)
    print url
    data = urllib2.urlopen(url).read()
    data = json.loads(data)
    return data["access_token"]

def refreshToken():
    access_token = GetAccessToken()
    setting = Setting()
    setting['wx_access_token'] = access_token
    setting['wx_access_token_time'] = getCurTime()
    clct_setting.update({}, {'$set': setting.getUpdateDict()})

if __name__ == '__main__':
    #print GetAccessToken()
    refreshToken()

