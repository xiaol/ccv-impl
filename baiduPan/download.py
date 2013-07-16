from Client import Get
from setting import UPLOAD_URL
import urllib2,urllib,socket

socket.setdefaulttimeout(3000) 

def download(token,path):
    query_string = {'method':'download', 'access_token':token, 'path':path}
    query_string = urllib.urlencode(query_string)
    print query_string
    return Get(UPLOAD_URL + '?' + query_string)
    
    


if __name__ == '__main__':
    from setting import token
    print download(token,'/apps/pocketvideo/1.txt')