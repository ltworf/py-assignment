"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from users.models import *
from django.test import TestCase, Client
import unittest

from time import time,sleep

try:
    from xtermcolor import colorize
except:
    colorize=lambda string, rgb=None, ansi=None, bg=None, ansi_bg=None, fd=1:string

def message(m,l=0):
    d= (0x00ff00,
        0xffff00,
        0xff0000)
    print colorize(m,d[l])
    
class UsersTest(TestCase):
    
    def setUp(self):
        #Create event since the db is empty
        u=User(first_name='test',last_name='test')
        u.save()
        self.client=Client()
    
    def get_non_existing_id(self):
        u=User.objects.create()
        r=u.id
        u.delete(force=True)
        return r
    def test_view(self):
        '''Checks on view'''
        u=User.objects.iterator().next()
        
        self.client.get('/user/')
        self.client.get('/user/detail/%d'%u.id)
        self.client.get('/user/%d'%u.id)
    def test_error_view(self):
        nid=self.get_non_existing_id()
        message('Not existing id %d on User' %nid)
        
        r=self.client.get('/user/detail/%d'%nid)
        self.assertTrue(r.status_code, 404)
        r=self.client.get('/user/%d'%nid)
        self.assertTrue(r.status_code, 404)
        
    def test_timestamp(self):
        '''Checks that the timestamp is correctly updated'''
        ct = time()
        t=LastModified.objects.get(pk='User')
        
        message('Timestamps: %d >= %d' %(ct,t.timestamp))
        self.assertGreaterEqual(ct,t.timestamp,'Table has timestamp in the future')
        
        #modify
        sleep(0.5)
        u=User()
        u.first_name='test1'
        u.save()
        
        t=LastModified.objects.get(pk='User')
        message('Timestamps %d >= %d' %(t.timestamp,ct))
        self.assertGreaterEqual(t.timestamp,ct,'Timestamp not updated')
