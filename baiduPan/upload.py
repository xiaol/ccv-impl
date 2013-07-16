from Client import Post
from setting import UPLOAD_URL
import urllib2,urllib,socket

socket.setdefaulttimeout(3000) 

def upload(token,path,data):
    params = []
    params.append({'name':'file','data':data,'filename':'1','type':'application/octet-stream'})
    
    query_string = {'method':'upload', 'access_token':token, 'path':path, 'ondup':'overwrite'}
    query_string = urllib.urlencode(query_string)
    print query_string
    print Post(UPLOAD_URL + '?' + query_string,params)
    
    


if __name__ == '__main__':
    from setting import token
    upload(token,'/apps/pocketvideo/1.jpg',open('1.jpg','rb').read())