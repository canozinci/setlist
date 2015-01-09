import os
import datetime
from django.conf import settings
import json, requests

from django.db import models
from django.db.models.signals import pre_save, post_delete,post_save
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


from actstream import action


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



def _image_upload_path(instance, filename):
    f, ext = os.path.splitext(filename)
    f ="image"
    filename = os.path.join(f + ext)
    if (os.path.exists(settings.MEDIA_ROOT+ instance.get_upload_path(filename))):
        dt = str(datetime.datetime.now())
        newname = 'file_'+dt+ext
        os.rename(settings.MEDIA_ROOT+ instance.get_upload_path(filename), settings.MEDIA_ROOT+ instance.get_upload_path(newname))

    return instance.get_upload_path(filename)

class User(AbstractUser):
    picture = models.ImageField(upload_to=_image_upload_path, max_length=500, blank=True, null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def get_upload_path(instance, filename):
        return "avatars/%s" % os.path.join(str(instance.username),filename)

    def __unicode__(self):
        return self.username

class Band(models.Model):

    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.CharField(max_length=200, blank=True, null=True)
    hometown = models.CharField(max_length=200, blank=True, null=True)
    established_year = models.IntegerField(max_length=4, default=datetime.datetime.now().year)
    logo = models.ImageField(upload_to=_image_upload_path, blank=True, null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    owner = models.ForeignKey(User)
    comments = generic.GenericRelation('Comment')

    def get_upload_path(instance, filename):
        return "bandlogos/%s" % os.path.join(str(instance.name), filename)

    def __unicode__(self):
        return self.name

    def comment_count(self) :
        ct = ContentType.objects.get_for_model(Band)
        obj_pk = self.id
        return Comment.objects.filter(content_type=ct, object_pk=obj_pk).count()

    def add_first_member(self, user_id):
        band_user_profile = BandUserProfile(band_id=self.id,
                                            user_id=user_id,
                                            band_creator=True,
                                            joined=True,
                                            date_invited=datetime.datetime.now(),
                                            date_joined=datetime.datetime.now(),
                                            created=datetime.datetime.now(),
                                            is_band_admin=True)
        band_user_profile.save()
        return band_user_profile

class BandUserProfile(models.Model):
    band = models.ForeignKey(Band, related_name="band_member")
    user = models.ForeignKey(User, related_name="band_user_profile")
    band_creator = models.BooleanField(default=False)
    date_invited = models.DateField(auto_now=False,auto_now_add=False)
    joined = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now=False,auto_now_add=False, blank=True,null=True)
    invited_by = models.ForeignKey(User, related_name="invited_by", blank=True,null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    is_band_admin = models.BooleanField(default=False)

    @property
    def band_user_profile_string(self):
        return "%s %s" % (self.band, self.user)

    def __unicode__(self):
        return self.band_user_profile_string

# -- INSTRUMENT MODELS
class Instrument(models.Model):

    name = models.CharField(max_length=200, blank=False, null=False)
    category = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)


    def __unicode__(self):
        return self.name
class UserInstrument(models.Model):
    user = models.ForeignKey(User, related_name="user_playing") #bunun ismini user_profile olarak degistirmek lazim
    Instrument = models.ForeignKey(Instrument, related_name="instrument")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    @property
    def user_instrument_string(self):
        return "%s %s" % (self.user.first_name, self.Instrument.name)

    def __unicode__(self):
        return self.user_instrument_string

# -- SONG MODELS
class Song(models.Model):
    band = models.ForeignKey(Band, related_name='songs')
    name = models.CharField(max_length=200, blank=False, null=False)
    length = models.IntegerField(blank=True, null=True,default=0)
    is_original = models.BooleanField(default=False)
    original_album_name = models.CharField(max_length=200, blank=True, null=True)
    original_artist = models.CharField(max_length=200, default='')
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    comments = generic.GenericRelation('Comment')
    media = generic.GenericRelation('Media')
    lyrics = models.TextField(blank=True, null=True)

    __original_length = 0

    def __init__(self, *args, **kwargs):
        super(Song, self).__init__(*args, **kwargs)
        self.__original_length = self.length
    def __unicode__(self):
        return self.name

    def comment_count(self) :
        ct = ContentType.objects.get_for_model(Song)
        obj_pk = self.id
        return Comment.objects.filter(content_type=ct, object_pk=obj_pk).count()






class SongPart(models.Model):
    song = models.ForeignKey(Song, related_name='song_parts')
    user_instrument = models.ForeignKey(UserInstrument, related_name="user_instrument")
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return '%s: %s' % (self.user_instrument.Instrument.name, self.user_instrument.user.first_name)
    def get_user(self):
        return self.user_instrument.user

## -- SETLIST MODELS
class Setlist(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    band = models.ForeignKey(Band, related_name='setlists')
    total_length = models.IntegerField(default=0)
    song_count = models.IntegerField(default=0)
    is_final = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    comments = generic.GenericRelation('Comment')
    def comment_count(self) :
        ct = ContentType.objects.get_for_model(Setlist)
        obj_pk = self.id
        return Comment.objects.filter(content_type=ct, object_pk=obj_pk).count()
    def __unicode__(self):
        return self.name
class SetlistSection(models.Model):
    setlist = models.ForeignKey(Setlist, related_name="sections")
    name = models.CharField(max_length=200, blank=False, null=False)
    length = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    @property
    def section_length(self):
        song_list = SetlistSectionSong.objects.filter(section=self)
        total_length = 0
        for song in song_list:
            total_length += song.song.length
        return total_length

    @property
    def song_count(self):
        song_list = SetlistSectionSong.objects.filter(section=self)
        songs = 0
        for song in song_list:
            songs += 1
        return songs



    def __unicode__(self):
        return self.setlist.name + " " + self.name
class SetlistSectionSong(models.Model):
    setlist = models.ForeignKey(Setlist, related_name="setlist_section_songs")
    section = models.ForeignKey(SetlistSection, related_name="section_songs")
    song = models.ForeignKey(Song, related_name="setlist_sections")
    song_number = models.IntegerField(max_length=3)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)



    def set_song_number(self):

        a = SetlistSectionSong.objects.filter(section=self.section)

        if self.song_number:
            return

        elif a:
            b = a.order_by('-song_number')[0]
            self.song_number = b.song_number + 1
        else:
            self.song_number = 1
        return

    def save(self, **kwargs):
        self.set_song_number()
        super(SetlistSectionSong, self).save()

    def __unicode__(self):
        return self.section.name + " " + self.song.name



class Venue(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.CharField(max_length=1000, blank=True, null=True)
    adress = models.CharField(max_length=400, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    contact_person_name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    homepage = models.CharField(max_length=200, blank=True, null=True)
    twitter_username = models.CharField(max_length=200, blank=True, null=True)
    instagram_username = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    comments = generic.GenericRelation('Comment')
    media = generic.GenericRelation('Media')

    def __unicode__(self):
        return self.name + " " + self.city

PRACTICE = 'PT'
CONCERT = 'CT'
RECORDING ='RC'
PR = 'PR'
OTHER = 'OR'


EVENTTYPES = (
    (PRACTICE, 'PRACTICE'),
    (CONCERT, 'CONCERT'),
    (RECORDING, 'RECORDING'),
    (PR, 'PR'),
    (OTHER, 'OTHER'),
)

class Event(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    date = models.DateTimeField(blank=False, null=False)
    band = models.ForeignKey(Band, related_name='events')
    venue = models.ForeignKey(Venue, related_name='events')
    type = models.CharField(max_length=2, choices=EVENTTYPES)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.band.name + " " + self.name

class EventAttendance(models.Model):
    event = models.ForeignKey(Event, related_name='attending')
    bandmember = models.ForeignKey(User,related_name='attending')
    status = models.NullBooleanField(default=None, null=True, blank=True)

    def __unicode__(self):
        return self.event.name + " " + self.bandmember.first_name+" " + self.bandmember.last_name + " " + str(self.status)




class Comment(models.Model):
    author = models.ForeignKey(User)
    is_flagged = models.BooleanField(default=False)
    body = models.TextField(blank=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    def __unicode__(self):
        return self.body

MEDIATYPES = (
    (0, 'VIDEO'),
    (1, 'AUDIO'),
    (2, 'HTML'),
    (2, 'IMAGE'),
)

SOURCETYPES = (
    (0, 'OWN'),
    (1, 'EXTERNAL'),
)

STORAGETYPES = (
    (0, 'OWN'),
    (1, 'EXTERNAL'),
)


class Media(models.Model):
    file_creator = models.ForeignKey(User)
    link = models.TextField()
    description = models.TextField(blank=True, null=True)
    domain = models.TextField(blank=True, null=True)
    #source_type = models.CharField(max_length=1, choices=SOURCETYPES)
    #media_type = models.CharField(max_length=1, choices=MEDIATYPES)
    #storage_type = models.CharField(max_length=1, choices=STORAGETYPES)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    comments = generic.GenericRelation('Comment')

    def __unicode__(self):
        return self.content_object.name


class UploadMedia(models.Model):
    pass

@receiver(models.signals.post_delete, sender=Setlist)
def handle_deleted_setlist(sender, instance, **kwargs):
    if instance.sections:
        instance.sections.all().delete()

@receiver(models.signals.post_delete, sender=SetlistSection)
def handle_deleted_setlistsection(sender, instance, **kwargs):
    if instance.section_songs:
        instance.section_songs.all().delete()


@receiver(models.signals.post_save, sender=Event)
def handle_event_attendace(sender, instance, **kwargs):
    set = instance.band.band_member.all()
    for member in set:
        a = EventAttendance(event_id=instance.id, bandmember_id = member.user.id,status= None)
        a.save()

'''

SEARCH INDEX UPDATES

'''
#her savede search indexe gonder
@receiver(models.signals.post_save, sender = Song)
def register_song_to_search(sender, instance, ** kwargs):

    data =''

    data = data + '{"index": {"_id": "%s"}}\n' % instance.pk
    data = data + json.dumps({
    "name": instance.name,
    "band": instance.band.name,
    "original_artist":instance.original_artist
    })+'\n'


    response = requests.put('http://127.0.0.1:9200/setlist_index/song/_bulk', data=data)

    return response.text

#her deletede search indexe gonder
@receiver(models.signals.post_delete, sender = Song)
def delete_song_from_search(sender, instance, ** kwargs):
    response = requests.delete('http://127.0.0.1:9200/setlist_index/song/'+ str(instance.id))
    return response.text
