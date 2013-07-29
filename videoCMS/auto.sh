#/bin/bash
#svn up
git pull origin
/usr/local/apache2/bin/httpd -k restart
