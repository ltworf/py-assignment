import urllib2
import urllib
import json
import httplib

from django.conf import settings

def get_remote():
    return Remote(settings.REMOTE_API_USERNAME,settings.REMOTE_API_PASSWORD,settings.REMOTE_API_BASE_URL,settings.REMOTE_API_HOSTNAME)
class DeleteException(Exception):
    def __init__(self,status):
        self.status=status
        
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
        head = {'Authorization': ('ApiKey %s:%s' % (self.username,self.key))}
        connection = self._get_connection()
        connection.connect()
        
        param = {}
        param['username'] = self.username
        param['api_key'] = self.key
        param['format'] = 'json'
        resource_uri = resource_uri + '?' + urllib.urlencode(param)
        
        connection.request('DELETE',resource_uri,headers=head)
        r = connection.getresponse()
        a = r.read()
        connection.close()
        if r.status != 204:
            raise DeleteException(r.status)
        return r
    def _get_connection(self):
        if self.protocol=='http':
            return httplib.HTTPConnection(self.host,self.port,False,10)
    def add(self,d,url='/v1/account_lead/?'):
        '''Adds a user to the remote database'''

        post = json.dumps(d)
        head = {'Content-Type':'application/json'}
        
        param = {}
        param['username'] = self.username
        param['api_key'] = self.key
        param['format'] = 'json'
        url = url + urllib.urlencode(param)
        
        connection = self._get_connection()
        connection.connect()
        connection.request('POST',url,post,head)
        r=connection.getresponse()
        error = (r.status != 201)
        a=r.read()
        connection.close()
        if error:
            raise Exception(a)
        return
        
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