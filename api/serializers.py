__author__ = 'canozinci'

from rest_framework import serializers
from setlist.models import User, Band, BandUserProfile, Song, Setlist, SongPart, UserInstrument,Instrument, Comment, Media, SetlistSection, SetlistSectionSong, Venue, Event ,EventAttendance

from actstream.models import Action


class UserShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'id','picture','username')
class CommentSerializer(serializers.ModelSerializer):
    author = UserShortSerializer()
    class Meta:
        model=Comment


class MediaSerializer(serializers.ModelSerializer):
    file_creator = UserShortSerializer()
    class Meta:
        model=Media
class VenueSerializer(serializers.ModelSerializer):
        class Meta:
            model = Venue

class VenueSerializerNested(serializers.ModelSerializer):
        comments = CommentSerializer()
        media = MediaSerializer()

        class Meta:
            model = Venue


class EventSerializer(serializers.ModelSerializer):

        class Meta:
            model = Event

class AttendaceSerializer(serializers.ModelSerializer):
    class Meta:
        model= EventAttendance

class AttendaceSerializerNested(serializers.ModelSerializer):

    bandmember = UserShortSerializer()

    class Meta:
        model= EventAttendance


class EventSerializerNested(serializers.ModelSerializer):

        venue = VenueSerializer()
        attending = AttendaceSerializerNested()

        class Meta:
            model = Event




class ActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action




class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = ('id', 'name', 'category',)

class UserInstrumentSerializer(serializers.ModelSerializer):

    Instrument = InstrumentSerializer(many=False)
    user = UserShortSerializer()


    class Meta:
        model = UserInstrument
        fields = ('id', 'user', 'Instrument',)

class UserUserInstrumentShortSerializer(serializers.ModelSerializer):
    user_playing = UserInstrumentSerializer(many=True)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'id','picture','username','user_playing')





class SongPartSerializer(serializers.ModelSerializer):

    class Meta:
        model = SongPart

class SongPartNestedSerializer(serializers.ModelSerializer):
    user_instrument = UserInstrumentSerializer()

    class Meta:
        model = SongPart
        fields = ('id','user_instrument',)

class SongSerializerNested(serializers.ModelSerializer):
    song_parts = SongPartNestedSerializer(many=True)
    comments = CommentSerializer(many=True)
    media = MediaSerializer(many=True)
    class Meta:
        model = Song

class SongSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        write_only_fields = ('password',)
        read_only_fields = ('is_superuser','is_staff','last_login','is_active','date_joined','last_updated')
        exclude=('groups','user_permissions')

class BandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Band
        read_only_fields = ('owner',)

class BandUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BandUserProfile
        read_only_fields = ('id','band','user','date_invited', 'date_joined', 'invited_by', )

class BandUserProfileSerializerNested(serializers.ModelSerializer):
    user = UserUserInstrumentShortSerializer()
    class Meta:
        model = BandUserProfile


class SetlistSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SetlistSection

class SetlistSectionSongSerializer(serializers.ModelSerializer):

    class Meta:
        model = SetlistSectionSong
        #read_only_fields = ('song_number',)

class SetlistSerializer(serializers.ModelSerializer):
        class Meta:
            model = Setlist

class SetlistSectionSongNestedSerializer(serializers.ModelSerializer):
    song = SongSerializer()
    class Meta:
        model = SetlistSectionSong


class SetlistSectionNestedSerializer(serializers.ModelSerializer):
    section_songs = SetlistSectionSongNestedSerializer()
    class Meta:
        model = SetlistSection


class SetlistSerializerNested(serializers.ModelSerializer):
    sections = SetlistSectionNestedSerializer()
    comments = CommentSerializer()

    class Meta:
        model = Setlist


class BandSerializerNested(serializers.ModelSerializer):

    band_member = BandUserProfileSerializer(many=True)
    songs = SongSerializer(many=True)
    setlists = SetlistSerializer(many=True)
    events = EventSerializerNested(many=True)


    class Meta:
        model = Band
        read_only_fields = ('owner',)


