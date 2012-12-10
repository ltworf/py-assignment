from time import time

from django.db.models.signals import post_save, post_delete
from django.conf import settings

import logging
logger = logging.getLogger(__name__)

from users.models import User,LastModified
from remote import get_remote,DeleteException


def post_save_user(sender, **kwargs):
    user=kwargs['instance']
    print("Save %s '%s'" % (str(user), user.resource_uri))
    if user.resource_uri!='' or user.mailing_lists.count()==0:
        return
    print('Saving remotely')
    #It goes here when the resource is just being created BUT, on the 2nd save(),
    #when the mailing_lists are being added and the user has an id on the db.
    
    remote_db = get_remote()
    d=user.to_dict()
    try:
        remote_db.add(d)
    except:
        logger.error('Could not create the resource remotely')
    
    user.resource_uri='committed'
    user.save()
    
def post_delete_user(sender,**kwargs):
    user=kwargs['instance']

    print("Delete %s '%s'" % (str(user), user.resource_uri))
    if user.resource_uri not in ('','committed'):
        print('Deleting remotely')
        remote_db=get_remote()
        try:
            remote_db.delete(user.resource_uri)
        except DeleteException as e:
            print('Not present remotely')
            if e.status==404:
                pass
            else:
                raise e
            
def update_last_modified(sender,**kwargs):
    if sender.__name__ == 'LastModified':
        return
    try:
        d=LastModified.objects.get(pk=sender.__name__)
    except:
        d=LastModified()
        d.pk = sender.__name__
    d.timestamp = int(time())
    d.save()        
    
        
post_save.connect(post_save_user,sender=User)
post_delete.connect(post_delete_user,sender=User)
post_save.connect(update_last_modified)
post_delete.connect(update_last_modified)