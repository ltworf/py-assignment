#!/usr/bin/env python
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "assignment.settings")
import json

from users.models import *
from django.conf import settings


from remote import Remote

remote_db = Remote(settings.REMOTE_API_USERNAME,settings.REMOTE_API_PASSWORD,settings.REMOTE_API_BASE_URL)

def sync():
    r='v1/account_lead/'

    b=remote_db.request(r)
    b=json.loads(b)
    
    #Sets are hashed, the "in" operator is O(1), it would be O(n) on a list
    uri_set = set()

    #Add remote users locally
    added=0
    for i in b['objects']:
        uri_set.add(i['resource_uri'])
        if len(User.objects.filter(resource_uri=i['resource_uri']))==0:
            #User does not exist locally
            User.create_from_dic(i)
            added+=1
    print 'Downloaded %d objects, added %d' % (len(b['objects']),added)
    
    #Remove remote users locally
    to_delete = []
    for i in User.objects.iterator(): #Using iterator because "all" would load the entire table in memory
        if i.resource_uri not in uri_set:
            to_delete.append(i) #I don't know how the iterator is implemented, i delete the objects later for safety
    print "Removing %d local users who don't exist remotely" % len(to_delete)
    map(User.delete,to_delete)
            
if __name__ == "__main__":
    sync()