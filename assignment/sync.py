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

    for i in b['objects']:
        if len(User.objects.filter(resource_uri=i['resource_uri']))==0:
            #User does not exist locally
            User.create_from_dic(i)

            
if __name__ == "__main__":
    sync()