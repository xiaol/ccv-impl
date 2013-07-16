import urllib2,json,traceback

def Post(URI,params):  
        ''''' 
            params =[{'name':'pic','filename':'shell.png','type':'image/png','data':'xxx'},...] 
             
            if 'error' in return dict,thus the request was failed! 
        '''  
        header  = {}
        header['Content-type'] ='multipart/form-data; boundary=huohua'  
          
        data = ''  
        for param in params:  
            data += '--huohua\r\n'  
            data += 'Content-Disposition: form-data; name="%s"; '%param['name']  
            if 'filename' in param:  
                data += 'filename="%s"'%param['filename']  
            if 'type' in param:  
                data += '\r\nContent-Type: %s'%param['type']  
            data +='\r\n\r\n'  
            data += param['data']  
            data +='\r\n'  
        data += '--huohua--'  
        #print data  
        try:  
            request = urllib2.Request(URI,data=data, headers=header)  
            result = urllib2.urlopen(request).read().decode('utf-8')  
            result = json.loads(result)  
        except urllib2.HTTPError,e:
            
            result = {'error':str(e.code)+' ' + e.msg}
            #print e.read()
        except:  
            result = {'error':'get respose from sina error: request error |'+traceback.format_exc()}  
          
        return result
    
    
def Get(url):
    return  urllib2.urlopen(url).read()