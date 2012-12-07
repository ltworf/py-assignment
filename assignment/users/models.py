from django.db import models

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
    birth_date = models.DateField(null=True)
    city = models.CharField(max_length=200,default='')
    country = models.CharField(max_length=4,default='')
    email = models.EmailField(max_length=254,default='')
    first_name = models.CharField(max_length=200,default='')
    gender = models.CharField(max_length=1,default='',choices=(('m','Male'),('f','Female'),('','Unspecified'),('o','Other')))
    last_name = models.CharField(max_length=200,default='')
    lead = models.BooleanField(default=False)
    phone = models.CharField(max_length=60,default='')
    street_number = models.CharField(max_length=10,default='')
    mailing_lists = models.ManyToManyField(MailingList)
    resource_uri = models.CharField(max_length=200,editable=False,unique=True,primary_key=True) #remote url to the resource
    tr_input_method = models.CharField(max_length=200,default='')
    tr_ip_address = models.CharField(max_length=45,null=True) #TODO expand charfield model to represent an ip address
    tr_language = models.CharField(max_length=10,default='')
    tr_referral = models.ForeignKey(Referral,null=True,on_delete=models.PROTECT)
    utm_campaign = models.CharField(max_length=200,default='')
    utm_medium = models.CharField(max_length=200,default='')
    utm_source = models.CharField(max_length=200,default='')
    #TODO filtering = u'filtering': {u'email': 1, u'first_name': 1, u'last_name': 1}}
    zipcode = models.CharField(max_length=10)
    
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