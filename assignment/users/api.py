from tastypie.resources import ModelResource
from users.models import User


from tastypie.authentication import Authentication
from tastypie.authorization import Authorization


class MyAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        return True
        if 'salvo' in request.user.username:
          return True

        return False

    # Optional but recommended
    def get_identifier(self, request):
        return request.user.username

class MyAuthorization(Authorization):
    def is_authorized(self, request, object=None):
        return True
        if request.user.date_joined.year == 2010:
            return True
        else:
            return False

    # Optional but useful for advanced limiting, such as per user.
    #def apply_limits(self, request, object_list):
    #    if request and hasattr(request, 'user'):
    #        return object_list.filter(author__username=request.user.username)

    #    return object_list.none()


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        
        authentication = MyAuthentication()
        authorization = MyAuthorization()
