#!/usr/bin/env python
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "assignment.settings")
import json

from users.models import *
from django.conf import settings

from color import message
from remote import get_remote

remote_db = get_remote()

def sync():
    r='v1/account_lead/'
    message('Requesting remote data...',1)
    b=remote_db.request(r)
    message('done!')
    
    #Sets are hashed, the "in" operator is O(1), it would be O(n) on a list
    uri_set = set()

    #Add remote users locally
    added=0
    merged=0
    for i in b['objects']:
        uri_set.add(i['resource_uri'])
        if len(User.objects.filter(resource_uri=i['resource_uri']))==0:
            #Tries to merge with local object using the email
            
            local_user=User.objects.filter(email=i['email'])
            
            if len(local_user)==1:
                message('Merging remote and local User %s'%i['email'])
                local_user[0].resource_uri=i['resource_uri']
                local_user[0].save()
                merged+=1
            else:
                #User does not exist locally
                User.create_from_dic(i)
                added+=1
    message('Downloaded %d objects, added %d, merged %d' % (len(b['objects']),added,merged))
    
    #Remove remote users locally
    to_delete = []
    for i in User.objects.iterator(): #Using iterator because "all" would load the entire table in memory
        if i.resource_uri not in uri_set:
            to_delete.append(i) #I don't know how the iterator is implemented, i delete the objects later for safety
    message("Removing %d local users who don't exist remotely" % len(to_delete),1)
    map(lambda x: x.delete(force=True),to_delete)
            
if __name__ == "__main__":
    sync()