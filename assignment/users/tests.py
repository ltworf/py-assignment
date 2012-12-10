"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from users.models import *
from django.test import TestCase, Client
import unittest

from time import time,sleep

from color import message

class UsersTest(TestCase):
    def getSeq(self):
        '''Returns a different int every time it is called'''
        try:
            self.seq+=1
        except:
            self.seq=0
        return self.seq
    def setUp(self):
        #Create event since the db is empty
        u=User(first_name='test',last_name='test',email='%d@test.com' % self.getSeq())
        u.save()
        self.client=Client()
    
    def get_non_existing_id(self):
        u=User.objects.create(email='%d@test.com' % self.getSeq())
        r=u.id
        u.delete(force=True)
        return r
    
    @staticmethod
    def get_standard_user():
        return {'first_name':'saro','last_name':'falsaperla','email':'saro.falsaperla@sicilia.it','birth_date':'05/12/2012'}
        
    def post_user(self,d):
        '''Adds an user with the form'''
        return self.client.post('/users/add/',d) 
    
    def test_not_add_user(self):
        '''Uses the form with invalid data and checks if the user is added or not'''
        message('Posting invalid users',1)
        c=User.objects.count()
        
        for k in UsersTest.get_standard_user().keys():
            d=UsersTest.get_standard_user()
            d[k]=''
            message('Nulling field %s' %k)
        
            response=self.post_user(d)
            self.assertEqual(response.status_code,200)
        
            nc=User.objects.count()
            self.assertEqual(nc,c,response.content)
    
    def test_add_user(self):
        '''Tries to add a new user using the add form'''
        c=User.objects.count()
        
        
        d=UsersTest.get_standard_user()
        response=self.post_user(d)
        self.assertTrue(response.status_code!=200)
        
        nc=User.objects.count()
        if nc != c+1:
            message(response.content,2)
        self.assertEqual(nc,c+1,'User post failed')
        
    def test_view(self):
        '''Tests that view don't return errors'''
        u=User.objects.iterator().next()
        
        response=self.client.get('/users/')
        self.assertTrue(response.status_code/100 in (2,3))
        response=self.client.get('/users/detail/%d'%u.id)
        self.assertTrue(response.status_code/100 in (2,3))
        response=self.client.get('/users/%d'%u.id)
        self.assertTrue(response.status_code/100 in (2,3))
    def test_error_view(self):
        '''Tests that 404 is returned when prompting non existing users'''
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
        sleep(2)
        u=User()
        u.first_name='test1'
        u.save()
        
        t=LastModified.objects.get(pk='User')
        message('Timestamps %d >= %d' %(t.timestamp,ct))
        self.assertGreaterEqual(t.timestamp,ct,'Timestamp not updated')
