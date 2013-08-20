import os,sys
import urllib2
import hashlib
import time
##########################################################
user_key = 'D9h3tEDAVHMP8rUX'
user_code = '6sU^mhMr+Rk5ixx'
user_site= 'test.weiweimeishi.com'
user_user_id = '50407'
user_file=''
##########################################################
server = 'userapi.anquanbao.com'


def ha_md5(my_api_key,my_site,my_code,my_id,my_file):
        result = 0
        my_tm = int(time.time() * 1000)
        #print my_tm
        paralist = [my_api_key,my_site,my_id,my_file]
        paralist.sort()
        param01 = paralist[0]
        param02 = paralist[1]
        param03 = paralist[2]
        param04 = paralist[3]
        #print "param01= " + param01
        #print "param02= " + param02
        src = "%s%s%s%s%s%s"%(param01,param02,param03,param04,my_tm,my_code)
        #print "src= " + src
        myMD5 = hashlib.md5() 
        myMD5.update(src)
        myMd5_Digest = myMD5.hexdigest()
        return myMd5_Digest

def prefetch_cache(my_server,my_api_key,my_site,my_id,my_file,my_ha):
        result = 0
        my_tm = int(time.time() * 1000)
        url = "https://%s/prefetch_cache" % (my_server)
        #print (url)
        data = "api_key=%s&tm=%s&website=%s&user_id=%s&file=%s&ha=%s" % (my_api_key,my_tm,my_site,my_id,my_file,my_ha)
        #print (data)
        req = urllib2.Request(url,data)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95')
        try:
                res = urllib2.urlopen(req,timeout=60)
                result = res.read()
                if len(result)==0:
                        print "We've got a NULL prefetch cache!Failed!"
                        exit(21)
        except urllib2.HTTPError,e:
                print "We have an error in getting prefetch cache!Failed!"
                print e
                exit(-1)
        return result


def get_progress(my_server,my_api_key,my_site,my_id,my_file,my_ha):
        result = 0
        my_tm = int(time.time() * 1000)
        url = "https://%s/get_prefetch_cache_progess" % (my_server)
     
        #print (url)
        data = "api_key=%s&tm=%s&website=%s&user_id=%s&file=%s&ha=%s" % (my_api_key,my_tm,my_site,my_id,my_file,my_ha)
        #print (data)
        req = urllib2.Request(url,data)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95')
        try:
                res = urllib2.urlopen(req,timeout=60)
                result = res.read()
                if len(result)==0:
                        print "We've got a NULL in geting prefetch progress!Failed!"
                        exit(21)
        except urllib2.HTTPError,e:
                print "We have an error in getting prefetch progress!Failed!"
                print e
                exit(-1)
        return result

def call_user():
        md5 = ha_md5(user_key,user_site,user_code,user_user_id,user_file)
        pre_cache = prefetch_cache(server,user_key,user_site,user_user_id,user_file,md5)
        print  pre_cache


def PrefetchCache(filename):
        md5 = ha_md5(user_key,user_site,user_code,user_user_id,filename)
        pre_cache = prefetch_cache(server,user_key,user_site,user_user_id,filename,md5)
        return pre_cache

def GetProgress(filename):
        md5 = ha_md5(user_key,user_site,user_code,user_user_id,filename)
        get_pro = get_progress(server,user_key,user_site,user_user_id,filename,md5)
        return get_pro

if __name__ == "__main__":
        print "start"
        #call_user()
        #PrefetchCache("/huohua/shortvideo/rrtt4.mp4")
        print GetProgress("/huohua/shortvideo/rrtt4.mp4")
