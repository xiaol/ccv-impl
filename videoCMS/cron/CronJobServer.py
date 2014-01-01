#coding=utf-8
import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))]

import time,json,threading,traceback
from videoCMS.conf import clct_resource,clct_channel,clct_cronJob,jPushClient,JPUSH_APP_KEY
from videoCMS.common.common import getCurTime
from videoCMS.common.anquanbao import PrefetchCache,GetProgress

class CronJobServer():
    RUN_EVERY_MINS = 1
    taskMap = {}

    def register(self,type,handle):
        self.taskMap[type] = handle

    def run(self,asyn = False):
        while True:
            curTime = getCurTime()
            print curTime,'live'
            task = clct_cronJob.find_one({'cronTime':{'$lte':curTime},'error':{'$exists':False}})
            if not task:
                time.sleep(self.RUN_EVERY_MINS * 60)
                continue
            try:
                print 'Get Task:',str(task)
                if asyn:
                    t = threading.Thread(target=self.taskMap[task['type']],args=(task,))
                    t.start()
                else:
                    self.taskMap[task['type']](task)
            except:
                print traceback.format_exc()

            time.sleep(self.RUN_EVERY_MINS * 60)



def handleAndroidPush(task):
    pushType = task['pushType']
    channelId = task['pushChannelId']
    title = task['pushTitle']
    content = task['pushContent']
    extras = task['extras']

    try:
        if pushType ==  'AppKey':
            print '向APPKEY:%s 的Android设备Push：title: %s content: %s'%(JPUSH_APP_KEY,title,content)
            jPushClient.send_notification_by_appkey(JPUSH_APP_KEY, int(time.time()), 'des',title,content, 'android',extras=extras)
    except:
        clct_cronJob.update({'_id':task['_id']},{'$set':{'error':traceback.format_exc()}})
    else:
        clct_cronJob.remove({'_id':task['_id']})

def handleCheckResouceAvailable(task):
    pass


if __name__ == '__main__':
    cronJobServer = CronJobServer()
    cronJobServer.register('AndroidPush',handleAndroidPush)
    cronJobServer.register('CheckResouceAvailable',handleCheckResouceAvailable)
    cronJobServer.run()


    #t1.join()
    #t2.join()