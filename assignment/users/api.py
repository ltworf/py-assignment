from tastypie.resources import ModelResource
from users.models import User


from tastypie.authentication import Authentication
from tastypie.authorization import Authorization

from django.conf import settings


class MyAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        return True

    def get_identifier(self, request):
        return request.user.username

class MyAuthorization(Authorization):
    def is_authorized(self, request, object=None):
        if not (request.GET['username']==settings.PUBLIC_API_USERNAME and
           request.GET['api_key'] == settings.PUBLIC_API_PASSWORD):
               raise Exception('Unauthorized')
        return True


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        
        #TODO yes this is not very evolved but i don't have a user database now
        authentication = MyAuthentication()
        authorization = MyAuthorization()
