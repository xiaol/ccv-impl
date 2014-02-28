#/bin/bash
#svn up
git pull origin
#/usr/local/apache2/bin/httpd -k restart
pkill -9 -f "/videoCMS/videoCMS/wsgi.py"
sleep 3
/usr/local/python2.7/bin/uwsgi --http :8013 -M  --processes 4 --wsgi-file /usr/local/apache2/djangoapp/videoCMS/videoCMS/wsgi.py -d log.log --stats stats.socket
