from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict

def ml_count(value):
    if value.count < 1 or value.count > 5:
        raise ValidationError('Number of mailing lists should be between 1 and 5')

def validate_ip(value):
    #TODO validate ip address, it can be ipv4/6/4-to-6-tunnel
    pass

class LastModified(models.Model):
    '''This class represents when a certain resource was last modified'''
    name = models.CharField(max_length=20,unique=True,primary_key=True)
    timestamp = models.DecimalField(max_digits=22,decimal_places=1)
    
    def __unicode__(self):
        return '%s: %d' % (self.name,self.timestamp)
    
class MailingList(models.Model):
    name = models.CharField(max_length=200,default='',unique=True)
    resource_uri = models.CharField(max_length=200,default='')
    
    def __unicode__(self):
        return self.name
    
    @staticmethod
    def return_from_dic(d):
        '''Creates the object from a dictionary and returns it.
        If the object already exists, returns it without creating anything.'''
        search = MailingList.objects.filter(name=d['name'])
        
        if len(search) == 1:
            return search[0]
        newml = MailingList(**d)
        newml.save()
        return newml
        
class Referral(models.Model):
    name = models.CharField(max_length=200,default='')
    resource_uri = models.CharField(max_length=200,default='')
    
    def __unicode__(self):
        return self.name
    
    @staticmethod
    def return_from_dic(d):
        '''Creates the object from a dictionary and returns it.'''
        search = Referral.objects.filter(**d)
        
        if len(search) == 1:
            return search[0]
        newr = Referral(**d)
        newr.save()
        return newr
        pass
class User(models.Model):
    birth_date = models.DateField(null=True,blank=True)
    city = models.CharField(max_length=200,default='',blank=True)
    country = models.CharField(max_length=4,default='',blank=True,choices=(('nl','NL'),('be','BE'),('de','DE'),('fr','FR'),('other','Other')))
    email = models.EmailField(max_length=254, unique=True,db_index=True)
    first_name = models.CharField(max_length=200,default='')
    gender = models.CharField(max_length=1,default='',choices=(('m','Male'),('f','Female')),blank=True)
    last_name = models.CharField(max_length=200,default='')
    lead = models.BooleanField(default=False)
    phone = models.CharField(max_length=60,default='',blank=True)
    street_number = models.CharField(max_length=10,default='',blank=True)
    mailing_lists = models.ManyToManyField(MailingList,validators=[ml_count])
    resource_uri = models.CharField(max_length=200,editable=False,blank=True,db_index=True) #remote url to the resource
    tr_input_method = models.CharField(max_length=200,default='',blank=True)
    tr_ip_address = models.CharField(max_length=45,null=True,validators=[validate_ip])
    tr_language = models.CharField(max_length=10,default='',blank=True,choices=(('nl_NL','Dutch (nl_NL)'),('nl_BE','Dutch (nl_BE)'),('de_DE','German'),('fr_FR','French'),('en_EN','English')))
    tr_referral = models.ForeignKey(Referral,null=True,on_delete=models.PROTECT)
    utm_campaign = models.CharField(max_length=200,default='',blank=True)
    utm_medium = models.CharField(max_length=200,default='',blank=True)
    utm_source = models.CharField(max_length=200,default='',blank=True)
    zipcode = models.CharField(max_length=10,default='',blank=True)
    def to_dict(self):
        d=model_to_dict(self)
        #When sending and receiving the remote field is called differently...
        d['ip_address'] = d['tr_ip_address']
        del(d['tr_ip_address'])
    
    
        for i in d.keys():
            if d[i] == '' or d[i]==None:
                del(d[i])
        d['tr_referral'] = 'Salvatore'
        d['mailing_lists'] = self.mailing_lists.count()
        
        if 'birth_date' in d:
            d['birth_date'] = str(d['birth_date'])
        return d
    
    def get_absolute_url(self):
        return reverse('users:detail', args=[self.id])
    def delete(self, using=None,force=False):
        if self.resource_uri in ('committed','') and force==False:
            raise Exception('Can\'t delete unsynchronized item. Synchronize the database first!')
        super(User,self).delete(using)
    def save(self, force_insert=False, force_update=False, using=None):
        validate_ip(self.tr_ip_address)
        try:
            if self.tr_referral==None:
                self.tr_referral = Referral.return_from_dic({'name':'Salvatore','resource_uri':''})
        except:
            pass
           
        super(User,self).save(force_insert,force_update,using)
    def __unicode__(self):
        return '%s %s <%s>' % (self.first_name,self.last_name,self.email)
    
    @staticmethod
    def create_from_dic(d):
        '''Creates the object from a dictionary and returns it.'''
        referral = Referral.return_from_dic(d['tr_referral'])
        del(d['tr_referral'])
        ml = map(MailingList.return_from_dic, d['mailing_lists'])
        del(d['mailing_lists'])
        
        new_user = User(**d)
        new_user.save()
        
        new_user.tr_referral = referral
        map(new_user.mailing_lists.add,ml)
        new_user.save()
        
        pass

import users.events