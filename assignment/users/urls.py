from django.conf.urls import patterns, url

from users import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<uid>\d+)/$', views.ajaxdetail, name='ajaxdetail'),
    url(r'^detail/(?P<uid>\d+)/$', views.detail, name='detail'),
    url(r'^add/$', views.add, name='add'),
)