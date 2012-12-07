import urllib2
import urllib
import json

class Remote:
    def __init__(self,username,key,api):
        '''
        username and key authenticate
        api is the URL to use.
        '''
        self.username = username
        self.key = key
        self.api = api
        
    def request(self,service,param={}):
        param['username'] = self.username
        param['key'] = self.key
        param['format'] = 'json'

        url = '%s%s?%s' % (self.api, service, urllib.urlencode(param)) 
        print url
        f = urllib2.urlopen(url,timeout=10)
        r= ""
        while True:
            l = f.read()
            if len(l)==0:
                break
            r+=l
        f.close()
        return r