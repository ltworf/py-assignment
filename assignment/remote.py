import urllib2
import urllib
import json
import httplib

from django.conf import settings

def get_remote():
    return Remote(settings.REMOTE_API_USERNAME,settings.REMOTE_API_PASSWORD,settings.REMOTE_API_BASE_URL,settings.REMOTE_API_HOSTNAME)

class Remote:
    def __init__(self,username,key,api,host,protocol='http',port=80):
        '''
        username and key authenticate
        api is the URL to use.
        '''
        self.username = username
        self.key = key
        self.port = port
        self.host = host
        self.protocol = protocol
        self.api = '%s://%s:%d/%s' % (protocol,host,port,api)
    def delete(self,resource_uri):
        if self.protocol=='http':
            connection = httplib.HTTPConnection(self.host,self.port,False,10)
        connection.connect()
        connection.request('DELETE',resource_uri)
        r = connection.getresponse()
        connection.close()
        return r
    def add(self,d):
        '''Adds a user to the remote database'''
        #post = urllib.urlencode(d)
        post = json.dumps(d)
        print post
        return self.request('v1/account_lead/',{},post)
        
    def request(self,service,param={},post=None):
        param['username'] = self.username
        param['api_key'] = self.key
        param['format'] = 'json'

        url = '%s%s?%s' % (self.api, service, urllib.urlencode(param)) 
        print url
        f = urllib2.urlopen(url,data=post,timeout=10)
        
        print post
        
        #f = requests.post(url,
        #                 post,
        #                 headers={'content-type': 'application/json'})
        r= ""
        while True:
            l = f.read()
            if len(l)==0:
                break
            r+=l
        f.close()
        return json.loads(r)