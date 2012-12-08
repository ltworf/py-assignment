from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from users.models import *

def index(request):
    user_list = User.objects.all()
    context = {'user_list': user_list}
    return render(request, 'users/index.html', context)
    
    
    
    
def detail(request, uid):
    u = get_object_or_404(User,id=uid)
    return HttpResponse(u)

def add(request):
    return HttpResponse('suca')
def ajaxdetail(request, uid):
    u = get_object_or_404(User,id=uid)
    
    t = (u.email,
         u.first_name,
         u.last_name,
         str(u.birth_date),
         u.city,
         u.country,
         
         
    #gender    
    #lead = models.BooleanField(default=False)
    #phone = models.CharField(max_length=60,default='',blank=True)
    #street_number = models.CharField(max_length=10,default='',blank=True)
    #mailing_lists = models.ManyToManyField(MailingList,validators=[ml_count])
    #resource_uri = models.CharField(max_length=200,editable=False,blank=True,db_index=True) #remote url to the resource
    #tr_input_method = models.CharField(max_length=200,default='',blank=True)
    #tr_ip_address = models.CharField(max_length=45,null=True,validators=[validate_ip])
    #tr_language = models.CharField(max_length=10,default='',blank=True)
    #tr_referral = models.ForeignKey(Referral,null=True,on_delete=models.PROTECT)
    #utm_campaign = models.CharField(max_length=200,default='',blank=True)
    #utm_medium = models.CharField(max_length=200,default='',blank=True)
    #utm_source = models.CharField(max_length=200,default='',blank=True)
    ##TODO filtering = u'filtering': {u'email': 1, u'first_name': 1, u'last_name': 1}}
    #zipcode = models.CharField(max_length=10,default='',blank=True)
        )
    
    s='<a href="mailto:%s">%s %s</a><br>Birthdate: %s<br>%s (%s)'%t
       
    
    return HttpResponse(s)