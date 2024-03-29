from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


from django.contrib import admin
from users.models import *

from users.api import UserResource

user_resource = UserResource()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'assignment.views.home', name='home'),
    # url(r'^assignment/', include('assignment.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^api/', include(user_resource.urls)),
    url(r'^search/', include('haystack.urls')),
    
    url(r'^users/',include('users.urls',namespace='users')),
    url(r'^',include('users.urls',namespace='users')),
)
