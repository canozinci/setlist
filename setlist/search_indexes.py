'''

HAYSTACK ICIN VARDI ARTIK GEREK YOK


from haystack import indexes
from django.utils import timezone

from .models import Song,Band

class SongIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    bandid  = indexes.IntegerField(model_attr='band_id')
    bandname  = indexes.CharField(model_attr='band')
    original_artist  = indexes.CharField(model_attr='original_artist')
    created = indexes.DateTimeField(model_attr='created')
    last_updated = indexes.DateTimeField(model_attr='last_updated')

    def get_model(self):
        return Song

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(last_updated__lte=timezone.now())

class BandIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True,model_attr='name')
    name = indexes.CharField(model_attr='name')
    owner = indexes.CharField(model_attr='owner')

    def get_model(self):
        return Band

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(last_updated__lte=timezone.now())

        '''