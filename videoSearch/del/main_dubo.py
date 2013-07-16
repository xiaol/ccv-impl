#coding=utf-8
# 更新主控脚本
# 从channel表读取配更新配置，进行更新

from common.SingletonProcessDecoration import SingletonProcessDecoration
from setting import clct_channel
import sys,time,json
from common.common import getCurTime



def process_channel(channel):
    handleName = channel['handleName']
    __import__(handleName)
    module = sys.modules[handleName]
    args = channel['handleArgs']
    if type(args) == str or type(args) == unicode:
        args = json.loads(args)
    print args
    print SingletonProcessDecoration(handleName+'.lock')(module.startSearch)(*args)
    '''
    #更新下次更新时间
    t = time.strftime('%Y%m%d%H%M%S',time.localtime(time.mktime(time.strptime(channel['nextSearchTime'],'%Y%m%d%H%M%S')) + int(channel['handleFrequents'])))
    print t
    clct_channel.update({'_id':channel['_id']},{'$set':{'nextSearchTime': t}})
    '''

def main():
    while True:
        channels = clct_channel.find({'nextSearchTime':{'$lte':getCurTime(),"$ne":""}})
        for channel in channels:
            print channel
            process_channel(channel)
        print 'loop'
        time.sleep(60)
        
def main_once():
    channels = clct_channel.find({'handleName':{"$ne":""},"processed":True,"channelType":23},timeout=False)
    for channel in channels:
        print channel
        try:
            process_channel(channel)
        except:
            import traceback
            print traceback.format_exc()
'''
def test():
    channel = {}
    channel['handleName'] = 'search_zongyi'
    channel['handleArgs'] = ['handles.handle_youku_showPage', 'http://www.youku.com/show_page/id_zd18a7caa2d4311e29498.html',100022]
    process_channel(channel)
'''

if __name__ == '__main__':
    #main()
    main_once()
    #test()
    

