from django.db.models.signals import post_save, post_delete
from django.conf import settings

from users.models import User
from remote import get_remote

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
        remote_db.delete(user.resource_uri)
        print "-->",user

post_save.connect(post_save_user,sender=User)
post_delete.connect(post_delete_user,sender=User)