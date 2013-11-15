#coding=utf-8
import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))]

import time,json,threading,traceback
from videoCMS.conf import clct_resource,clct_channel,clct_cronJob,JPushClient,JPUSH_APP_KEY
from videoCMS.common.common import getCurTime
from videoCMS.common.anquanbao import PrefetchCache,GetProgress

class CronJobServer():
    RUN_EVERY_MINS = 60
    taskMap = {}

    def register(self,type,handle):
        self.taskMap[type] = handle

    def run(self,asyn = False):
        while True:
            curTime = getCurTime()
            print curTime,'live'
            task = clct_cronJob.find_one({'cronTime':{'$lte':curTime}})
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



def handleAndroidPush(task):
    pushType = task['pushType']
    channelId = task.get['pushChannelId']
    title = task['pushTitle']
    content = task['pushContent']
    extras = task['extras']
    if pushType ==  'AppKey':
        print '向APPKEY%s的Android设备Push：title:%s,content:%s'%(JPUSH_APP_KEY,title,content)
        JPushClient.send_notification_by_appkey(JPUSH_APP_KEY, time.time(), 'des',title,content, 'android',extras=extras)



if __name__ == '__main__':
    cronJobServer = CronJobServer()
    cronJobServer.register('AndroidPush',handleAndroidPush)
    cronJobServer.run()


    #t1.join()
    #t2.join()