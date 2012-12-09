from time import time

from django.db.models.signals import post_save, post_delete
from django.conf import settings

from users.models import User,LastModified
from remote import get_remote,DeleteException

def post_save_user(sender, **kwargs):
    user=kwargs['instance']
    if user.resource_uri!='':
        return
    
    #FIXME add resource remotely
    remote_db = get_remote()
    print "Request finished!",kwargs
    
def post_delete_user(sender,**kwargs):
    user=kwargs['instance']

    if user.resource_uri!='':
        remote_db=get_remote()
        try:
            remote_db.delete(user.resource_uri)
        except DeleteException as e:
            if e.status==404:
                pass
            else:
                raise e
            
        print "-->",user
        
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