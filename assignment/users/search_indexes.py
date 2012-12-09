import datetime
from haystack import indexes
from users.models import User


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)
    country = indexes.CharField(model_attr='country')
    city = indexes.CharField(model_attr='city')
    phone = indexes.CharField(model_attr='phone')
    street_number = indexes.CharField(model_attr='street_number')
    first_name = indexes.CharField(model_attr='first_name')
    last_name = indexes.CharField(model_attr='last_name')
    email = indexes.CharField(model_attr='email')
    
    birth_date = indexes.DateTimeField(model_attr='birth_date')

    def get_model(self):
        return User

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()