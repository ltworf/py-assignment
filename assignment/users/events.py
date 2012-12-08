from django.db.models.signals import post_save, post_delete
from django.conf import settings

from users.models import User
from remote import Remote

def post_save_user(sender, **kwargs):
    user=kwargs['instance']
    if user.resource_uri!='':
        return
    remote_db = Remote(settings.REMOTE_API_USERNAME,settings.REMOTE_API_PASSWORD,settings.REMOTE_API_BASE_URL)
    
    
    print "Request finished!",kwargs
    
def post_delete_user(sender,**kwargs):
    user=kwargs['instance']
    
    print "-->",user.resource_uri
        
    #TODO remove entity remotely

post_save.connect(post_save_user,sender=User)
post_delete.connect(post_delete_user,sender=User)