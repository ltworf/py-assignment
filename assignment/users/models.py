from django.db import models

class MailingList(models.Model):
    name = models.CharField(max_length=200,default='')
    resource_uri = models.CharField(max_length=200,default='')
class Referral(models.Model):
    name = models.CharField(max_length=200,default='')
    resource_uri = models.CharField(max_length=200,default='')
    
class User(models.Model):
    birth_date = models.DateField(null=True)
    city = models.CharField(max_length=200,default='')
    country = models.CharField(max_length=4,default='')
    email = models.EmailField(max_length=254,default='')
    first_name = models.CharField(max_length=200,default='')
    gender = models.CharField(max_length=1,default='',choices=('m','f','','o'))
    last_name = models.CharField(max_length=200,default='')
    lead = models.BooleanField(default=False)
    phone = models.CharField(max_length=60,default='')
    street_number = models.CharField(max_length=10,default='')
    mailing_lists = models.ManyToManyField(MailingList)
    resource_uri = models.CharField(max_length=200,readonly=True) #remote url to the resource
    tr_input_method = models.CharField(max_length=200,default='')
    tr_ip_address = models.CharField(max_length=45,null=True) #TODO expand charfield model to represent an ip address
    tr_language = models.CharField(max_length=10,default='')
    tr_referral = models.ForeignKey(Referral,null=True,on_delete=models.PROTECT)
    utm_campaign = models.CharField(max_length=200,default='')
    utm_medium = models.CharField(max_length=200,default='')
    utm_source = models.CharField(max_length=200,default='')
    #TODO filtering = u'filtering': {u'email': 1, u'first_name': 1, u'last_name': 1}}
    zipcode = models.CharField(max_length=10)
    