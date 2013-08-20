import sys,os
sys.path += [os.path.dirname(os.path.dirname(os.path.dirname(__file__)))]

import time
from videoCMS.conf import clct_resource
from videoCMS.common.common import getCurTime


class CronJobBase():
    RUN_EVERY_MINS = 60

    def run(self):
        while True:
            self.do()
            time.sleep(self.RUN_EVERY_MINS * 60)


class ResourceGoOnlineCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 

    def do(self):
        for one in clct_resource.find({'scheduleGoOnline':{'$ne':''}},{'scheduleGoOnline':1},timeout=False):
            curTime = getCurTime()
            print one
            if curTime > one['scheduleGoOnline']:
                print one['_id'],'goOnline'
                clct_resource.update({'_id':one['_id']},{'$set':\
                    {'scheduleGoOnline':'','createTime':curTime,'isOnline':True}})







if __name__ == '__main__':
    job1 = ResourceGoOnlineCronJob()
    job1.run()