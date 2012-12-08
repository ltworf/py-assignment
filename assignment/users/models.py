from django.db import models
from django.core.exceptions import ValidationError

def ml_count(value):
    if value.count < 1 or value.count > 5:
        raise ValidationError('Number of mailing lists should be between 1 and 5')

def validate_ip(value):
    #TODO validate ip address, it can be ipv4/6/4-to-6-tunnel
    pass
        
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
    country = models.CharField(max_length=4,default='',blank=True)
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=200,default='')
    gender = models.CharField(max_length=1,default='',choices=(('m','Male'),('f','Female'),('o','Other')),blank=True)
    last_name = models.CharField(max_length=200,default='')
    lead = models.BooleanField(default=False)
    phone = models.CharField(max_length=60,default='',blank=True)
    street_number = models.CharField(max_length=10,default='',blank=True)
    mailing_lists = models.ManyToManyField(MailingList,validators=[ml_count],default=[MailingList.objects.iterator().next()])
    resource_uri = models.CharField(max_length=200,editable=False,unique=True) #remote url to the resource
    tr_input_method = models.CharField(max_length=200,default='',blank=True)
    tr_ip_address = models.CharField(max_length=45,null=True,validators=[validate_ip])
    tr_language = models.CharField(max_length=10,default='',blank=True)
    tr_referral = models.ForeignKey(Referral,null=True,on_delete=models.PROTECT,default=Referral.return_from_dic({'name':'Salvatore','resource_uri':''}))
    utm_campaign = models.CharField(max_length=200,default='',blank=True)
    utm_medium = models.CharField(max_length=200,default='',blank=True)
    utm_source = models.CharField(max_length=200,default='',blank=True)
    #TODO filtering = u'filtering': {u'email': 1, u'first_name': 1, u'last_name': 1}}
    zipcode = models.CharField(max_length=10,default='',blank=True)
    
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
        new_user.tr_referral = referral
        map(new_user.mailing_lists.add,ml)
        new_user.save()
        
        pass