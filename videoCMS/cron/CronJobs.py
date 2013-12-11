import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))]

import time,json,threading
from videoCMS.conf import clct_resource,clct_channel,clct_cronJob
from videoCMS.common.common import getCurTime
from videoCMS.common.anquanbao import PrefetchCache,GetProgress

class CronJobBase():
    RUN_EVERY_MINS = 60

    def run(self):
        while True:
            #print '.'
            try:
                self.do()
            except:
                import traceback
                print traceback.format_exc()
            time.sleep(self.RUN_EVERY_MINS * 60)

    def runAsyn(self):
        t = threading.Thread(target=self.run)
        t.start()
        return t

class ResourceGoOnlineCronJob(CronJobBase):
    RUN_EVERY_MINS = 0.5

    def do(self):
        curTime = getCurTime()
        for one in clct_resource.find({'scheduleGoOnline':{'$ne':'','$lte':curTime}},{'scheduleGoOnline':1,'channelId':1},timeout=False):
            print one
            clct_resource.update({'_id':one['_id']},{'$set':\
                {'scheduleGoOnline':'','updateTime':curTime,'modifyTime':curTime,'isOnline':True}})
            clct_channel.update({'channelId':one['channelId']},{'$set':{'updateTime':getCurTime()}})
        print 'scaned'



class PushCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    def do(self):
        for one in clct_resource.find({'cdn':'waiting'},{'_id':1, 'videoId':1},timeout=False):
            ret = GetProgress('/'+one['videoId'])
            print ret
            ret = json.loads(ret)
            if ret['prefetch_status'].find('hit') != -1 and  ret['prefetch_status'].find('miss') == -1:
                print one['_id'],'goOnline'
                clct_resource.update({'_id':one['_id']},{'$unset':{'cdn':1},'$set':{'isOnline':True}})



if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'ResourceGoOnlineCronJob':
            job = ResourceGoOnlineCronJob()
            print 'start ResourceGoOnlineCronJob'
            job.run()
        elif sys.argv[1] == 'PushCronJob':
            job = PushCronJob()
            print 'start PushCronJob'
            job.run()

    print 'usage: python CronJobs.py [ ResourceGoOnlineCronJob | PushCronJob ]'

    #t1.join()
    #t2.join()