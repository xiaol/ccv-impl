import time
from videoCMS.conf import clct_resource


class CronJobBase():
    RUN_EVERY_MINS = 60

    def run(self):
        while True:
            self.do()
            time.sleep(self.RUN_EVERY_MINS * 60)


class ResourceGoOnlineCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 

    def do(self):
        print 'cron..'






if __name__ == '__main__':
    job1 = ResourceGoOnlineCronJob()
    job1.run()