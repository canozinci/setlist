__author__ = 'canozinci'
from django.apps import AppConfig
from actstream import registry

class MyAppConfig(AppConfig):
    name = 'setlist'

    def ready(self):
        registry.register(self.get_model('Song'))
        registry.register(self.get_model('Band'))
        registry.register(self.get_model('Comment'))
        registry.register(self.get_model('Media'))
        registry.register(self.get_model('User'))
        registry.register(self.get_model('SongPart'))
        registry.register(self.get_model('Setlist'))
        registry.register(self.get_model('Event'))
        registry.register(self.get_model('Venue'))
