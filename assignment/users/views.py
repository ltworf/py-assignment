from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import etag

from users.models import *
from users.forms import *


def latest_entry(table):
    '''Returns the last time a table was modified (only works
    if events are set to watch on that table'''
    try:
        return str(LastModified.objects.get(pk=table).timestamp)
    except:
        return '0'

@etag(lambda x:latest_entry('User'))
def index(request):
    user_list = User.objects.all()
    context = {'user_list': user_list}
    return render(request, 'users/index.html', context)

    
@etag(lambda x:latest_entry('User'))
def detail(request, uid):
    u = get_object_or_404(User,id=uid)
    return HttpResponse(u)

def add(request):
    if request.method == 'POST': # If the form has been submitted...
        form = UserForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            u=User()
            u.email=form.cleaned_data['email']
            u.first_name=form.cleaned_data['first_name']
            u.last_name=form.cleaned_data['last_name']
            u.birth_date=form.cleaned_data['birth_date']
            u.tr_ip_address = request.META['REMOTE_ADDR']
            u.save()
            u.mailing_lists.add(MailingList.objects.all()[0])
            return HttpResponseRedirect('/users/') # Redirect after POST
    else:
        form = UserForm() # An unbound form

    return render(request, 'users/add.html', {'form': form,})

@etag(lambda x:latest_entry('User'))
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