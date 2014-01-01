nohup /usr/local/python2.6/bin/python /usr/local/apache2/djangoapp/videoCMS/videoCMS/cron/CronJobs.py ResourceGoOnlineCronJob > ResourceGoOnlineCronJob.log&
nohup /usr/local/python2.6/bin/python /usr/local/apache2/djangoapp/videoCMS/videoCMS/cron/CronJobServer.py >CronJobServer.log  2>&1 &
