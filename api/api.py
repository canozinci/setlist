__author__ = 'canozinci'

from django.contrib.auth import login, logout
import datetime
import urlparse
import tldextract
from django.utils.timezone import utc

from actstream import action
from actstream.actions import follow, unfollow
from actstream.models import Action

from social.apps.django_app.utils import strategy, load_backend,load_strategy
from rest_framework.authentication import get_authorization_header
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .permissions import IsBandAdminOrReadOnly, BandDetailIsBandAdminOrReadOnly,IsOwnerOrReadOnly, IsBandMemberOrReadOnly
from .authentication import QuietBasicAuthentication,ExpiringTokenAuthentication

from .serializers import UserSerializer, BandSerializer, BandUserProfileSerializer, SongSerializerNested, BandSerializerNested, SongSerializer, UserInstrumentSerializer, SongPartSerializer, SongPartNestedSerializer, BandUserProfileSerializerNested , ActionSerializer, Setlist, SetlistSection, SetlistSectionSong, SetlistSerializer, SetlistSectionSerializer,SetlistSectionSongSerializer ,SetlistSerializerNested, EventSerializer, EventSerializerNested, VenueSerializer, VenueSerializerNested, AttendaceSerializer
from setlist.models import User, Band, BandUserProfile, Song, UserInstrument,SongPart, Comment, Event, Venue, EventAttendance


@strategy()
def register_by_access_token(request, backend):

    uri = ''
    strategy = load_strategy(request)
    backend = load_backend(strategy, backend, uri)
    # Split by spaces and get the array
    auth = get_authorization_header(request).split()

    if not auth or auth[0].lower() != b'token':
        msg = 'No token header provided.'
        return msg

    if len(auth) == 1:
        msg = 'Invalid token header. No credentials provided.'
        return msg

    access_token = auth[1]

    user = backend.do_auth(access_token)

    return user



class AuthView(APIView):
    authentication_classes = (QuietBasicAuthentication,)

    def post(self, request, *args, **kwargs):

        login(request, request.user)
        return Response(UserSerializer(request.user).data)

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response({})



class ObtainExpiringAuthToken(ObtainAuthToken):
    authentication_classes = ()
    def post(self, request, backend):
        serializer = self.serializer_class(data=request.DATA)
        if backend == 'auth':
            print request.DATA
            if serializer.is_valid():
                token, created = Token.objects.get_or_create(user=serializer.object['user'])

                if not created:
                    # update the created time of the token to keep it valid
                    token.created = datetime.datetime.utcnow().replace(tzinfo=utc)
                    token.save()

                return Response({'token': token.key, 'user': token.user.id})
        else:
            # Here we call PSA to authenticate like we would if we used PSA on server side.
            user = register_by_access_token(request, backend)

            # If user is active we get or create the REST token and send it back with user data
            if user and user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                # pipeline ile profile picure da sace ediyorum
                return Response({'token': token.key, 'user': token.user.id})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()



class BandEventList(generics.ListCreateAPIView):

        model = Event
        serializer_class = EventSerializer
        permission_classes = (permissions.IsAuthenticated,IsBandMemberOrReadOnly)



        def get_queryset(self):
            band_id = self.kwargs['band_id']
            return Event.objects.filter(band_id=band_id)


class AttendaceEventList(generics.ListCreateAPIView):

        model = EventAttendance
        serializer_class = AttendaceSerializer
        #permission_classes = (permissions.IsAuthenticated,IsBandMemberOrReadOnly)



        def get_queryset(self):
            event_id = self.kwargs['event_id']
            return EventAttendance.objects.filter(event_id=event_id)



class BandEventDetail(generics.RetrieveUpdateDestroyAPIView):

        model = Event
        serializer_class = EventSerializerNested
        lookup_field = 'id'
        #permission_classes = (permissions.IsAuthenticated,IsBandMemberOrReadOnly)



        def get_queryset(self):
            band_id = self.kwargs['band_id']
            return Event.objects.filter(band_id=band_id)


class BandActionList(generics.ListAPIView):
    model = Action
    serializer_class = ActionSerializer

    def get_queryset(self):
        band_id = self.kwargs['band_id']
        print band_id
        return Action.objects.filter(target_object_id=band_id)


class UserGenerate(generics.CreateAPIView):

        model = User
        serializer_class = UserSerializer

        def pre_save(self, obj):
            password = self.request.DATA['password']
            obj.set_password(password)

class UserList(generics.ListAPIView):
#        permission_classes = (IsAuthenticated,)
        authentication_classes = (ExpiringTokenAuthentication,)
        permission_classes = (permissions.IsAuthenticated,)

        lookup_field = 'id'
        queryset = User.objects.all()
        model = User
        serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
        authentication_classes = (ExpiringTokenAuthentication,)
        permission_classes = (permissions.IsAuthenticated,)

        lookup_field = 'id'
        model = User
        serializer_class = UserSerializer


class SongPartList(generics.ListCreateAPIView):
        authentication_classes = (ExpiringTokenAuthentication,)
        model = SongPart
        serializer_class = SongPartSerializer

class SongPartDetail(generics.RetrieveUpdateDestroyAPIView):
        authentication_classes = (ExpiringTokenAuthentication,)
        permission_classes = (permissions.IsAuthenticated, IsBandMemberOrReadOnly)
        lookup_field = 'id'
        model = SongPart
        serializer_class = SongPartSerializer

        def post_delete(self, obj, created=False):
            verb = "deleted a member part from song "
            action.send(self.request.user, verb='deleted a member part',
                                            action_object=obj,
                                            target=obj.song.band,
                                            band_id = obj.song.band.id,
                                            song_id = obj.song.id,
                                            song_name=obj.song.name,
                                            performer_first_name= obj.user_instrument.user.first_name,
                                            performer_last_name= obj.user_instrument.user.last_name,
                                            performer_id= obj.user_instrument.user.id,
                                            instrument= obj.user_instrument.Instrument.name,
                                            user_profile_pic = self.request.user.picture.url,
                                            first_name = self.request.user.first_name,
                                            last_name = self.request.user.last_name,
                                            user_name = self.request.user.username)




class BandList(generics.ListCreateAPIView):
    '''


    Returns all the bands in setlist.io. When POST, a band is created with request.user as it's creator and admin.
    BandUserProfile is also created for this band and request.user


    '''
    lookup_field = 'id'
    queryset = Band.objects.all()
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


    model = Band
    serializer_class = BandSerializer

    def pre_save(self, obj):

        user = User.objects.get(id=self.request.user.id)
        obj.owner = user
        #create a band_user_profile
    def post_save(self, obj, created=False):
        obj.add_first_member(obj.owner.id)
class BandDetail(generics.RetrieveUpdateDestroyAPIView):
    '''


    Returns the band with the id in the url. BandAdmins have permissions to make changes in the object. When deleted all
    Profile, Setlist and Song objects are deleted as well.


    '''
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,BandDetailIsBandAdminOrReadOnly)


    model = Band
    serializer_class = BandSerializerNested
    lookup_field = 'id'

class BandUserProfileList(generics.ListAPIView):

        def get_queryset(self):
            band_id = self.kwargs['band_id']
            band_user_profile = BandUserProfile.objects.filter(band_id=band_id)
            return band_user_profile

        model = BandUserProfile
        serializer_class = BandUserProfileSerializerNested




class BandSongList(generics.ListCreateAPIView):

        def get_queryset(self):
            band_id = self.kwargs['band_id']
            return Song.objects.filter(band_id=band_id)

        model = Song
        serializer_class = SongSerializer
        permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsBandMemberOrReadOnly)

        def post_save(self, obj, created=False):
            action.send(self.request.user, verb='created a Song', action_object=obj, target=obj.band, band_id = obj.band.id, song_id = obj.id,song_name=obj.name, user_profile_pic = self.request.user.picture.url, first_name = self.request.user.first_name, last_name = self.request.user.last_name, user_name = self.request.user.username)



class SongPartCreate(generics.CreateAPIView):
        authentication_classes = (ExpiringTokenAuthentication,)
        permission_classes = (permissions.IsAuthenticated, IsBandMemberOrReadOnly)

        model = SongPart
        serializer_class = SongPartSerializer

        def post_save(self, obj, created=False):
            verb = "added a member part to song "
            action.send(self.request.user, verb= verb,
                                            action_object=obj,
                                            target=obj.song.band,
                                            band_id = obj.song.band.id,
                                            song_id = obj.song.id,
                                            song_name=obj.song.name,
                                            performer_first_name= obj.user_instrument.user.first_name,
                                            performer_last_name= obj.user_instrument.user.last_name,
                                            performer_profile_pic = obj.user_instrument.user.picture.url,
                                            performer_id= obj.user_instrument.user.id,
                                            instrument= obj.user_instrument.Instrument.name,
                                            user_profile_pic = self.request.user.picture.url,
                                            first_name = self.request.user.first_name,
                                            last_name = self.request.user.last_name,
                                            user_name = self.request.user.username)


class SongDetail(generics.RetrieveUpdateDestroyAPIView):
        #authentication_classes = (ExpiringTokenAuthentication,)
        #permission_classes = (permissions.IsAuthenticated,IsBandMemberOrReadOnly)

        lookup_field = 'id'
        model = Song
        serializer_class = SongSerializerNested

class SongDetailUnnested(generics.RetrieveUpdateDestroyAPIView):
        #authentication_classes = (ExpiringTokenAuthentication,)
        #permission_classes = (permissions.IsAuthenticated,IsBandMemberOrReadOnly)

        lookup_field = 'id'
        model = Song
        serializer_class = SongSerializer


class UserInstrumentList(generics.ListCreateAPIView):
    model = UserInstrument
    serializer_class = UserInstrumentSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return UserInstrument.objects.filter(user_id=user_id)

class UserInstrumentDetail(generics.RetrieveUpdateDestroyAPIView):

    #def get_queryset(self):
    #    user_id = self.kwargs['user_id']
    #    return UserInstrument.objects.filter(user_id=user_id)

    lookup_field = 'id'
    model = UserInstrument
    serializer_class = UserInstrumentSerializer

class CreateSongComment(generics.CreateAPIView):

    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,IsBandMemberOrReadOnly)

    def post(self, request, format=None,*args,**kwargs):


        song_id = request.DATA['song']
        author = request.user
        body = request.DATA['body']

        song = Song.objects.get(id=song_id)

        song.comments.create(author=author, body=body)
        song.save()
        #content_type 18 is song
        comment = Comment.objects.filter(author = request.user.id, content_type = 18).latest('created')
        action.send(request.user, verb='added a comment to', action_object=comment, target=song.band, comment_type= "song_comment",  comment_body = body, song_id = song.id, song_name = song.name, band_id= song.band.id, user_profile_pic = self.request.user.picture.url,first_name = self.request.user.first_name, last_name = self.request.user.last_name, user_name = self.request.user.username)
        return Response(SongSerializer(song).data, status=status.HTTP_201_CREATED)

class CreateSetlistComment(generics.CreateAPIView):

    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,IsBandMemberOrReadOnly)

    def post(self, request, format=None,*args,**kwargs):


        setlist_id = request.DATA['setlist']
        author = request.user
        body = request.DATA['body']

        setlist = Setlist.objects.get(id=setlist_id)

        setlist.comments.create(author=author, body=body)
        setlist.save()
        #content_type 20 is setlist
        comment = Comment.objects.filter(author = request.user.id, content_type = 20).latest('created')
        action.send(request.user, verb='added a comment to', action_object=comment, target=setlist.band, comment_type= "setlist_comment",  comment_body = body, setlist_id = setlist.id, setlist_name = setlist.name, band_id= setlist.band.id, user_profile_pic = self.request.user.picture.url,first_name = self.request.user.first_name, last_name = self.request.user.last_name, user_name = self.request.user.username)
        return Response(SetlistSerializer(setlist).data, status=status.HTTP_201_CREATED)



class CreateSongMedia(generics.CreateAPIView):

    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,IsBandMemberOrReadOnly)

    def post(self, request, format=None,*args,**kwargs):

        song_id = request.DATA['song']
        file_creator = request.user
        description = request.DATA['description']
        pasted_link = request.DATA['link']


        extracted= tldextract.extract(pasted_link)
        print pasted_link

        if extracted.domain == "youtube":

            url_data = urlparse.urlparse(pasted_link)
            query = urlparse.parse_qs(url_data.query)
            video = query["v"][0]

        elif extracted.domain == "vimeo":

            url_data = urlparse.urlparse(pasted_link)
            video = url_data.path
        # bunu daha sonra bu linkteki mantiga gore edit etmem lazim track id icin
        # http://stackoverflow.com/questions/26289927/how-to-get-track-id-from-url-in-soundcloud-using-api
        elif extracted.domain == 'soundcloud':

            url_data = urlparse.urlparse(pasted_link)
            video = url_data.path

        else:
            return Response({"Source not allowed. Only setlist, Youtube, Vimoe, Soundcloud and Dropbox links are allowed"}, status=status.HTTP_400_BAD_REQUEST)



        song = Song.objects.get(id=song_id)

        song.media.create(file_creator=file_creator, link=video, description=description, domain= extracted.domain  )
        song.save()
        return Response(SongSerializer(song).data, status=status.HTTP_201_CREATED)

    def post_save(self, obj, created=False):

            action.send(self.request.user, verb='added a file', action_object=obj, target=obj.band, song_name =obj.name, band_id=obj.band.id, user_profile_pic = self.request.user.picture.url, first_name = self.request.user.first_name, last_name = self.request.user.last_name, user_name = self.request.user.username)


class SetlistNested(generics.RetrieveAPIView):
        def get_queryset(self):
            band_id = self.kwargs['band_id']
            return Setlist.objects.filter(band_id=band_id)

        lookup_field = 'id'
        model = Setlist
        serializer_class = SetlistSerializerNested
        permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsBandMemberOrReadOnly)

class SetlistList(generics.ListCreateAPIView):
        def get_queryset(self):
            band_id = self.kwargs['band_id']
            return Setlist.objects.filter(band_id=band_id)
        model = Setlist
        serializer_class = SetlistSerializer
        permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsBandMemberOrReadOnly)

class SetlistDetail(generics.RetrieveUpdateDestroyAPIView):
        lookup_field = 'id'
        model = Setlist
        serializer_class = SetlistSerializer
        permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsBandMemberOrReadOnly)

class SetlistSectionList(generics.ListCreateAPIView):
        def get_queryset(self):
            setlist_id = self.kwargs['setlist_id']
            return SetlistSection.objects.filter(setlist_id = setlist_id)
        model = SetlistSection
        serializer_class = SetlistSectionSerializer
        permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsBandMemberOrReadOnly)

class SetlistSectionDetail(generics.RetrieveUpdateDestroyAPIView):
        lookup_field = 'id'
        model = SetlistSection
        serializer_class = SetlistSectionSerializer
        permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsBandMemberOrReadOnly)

class SetlistSectionSongList(generics.ListCreateAPIView):
        def get_queryset(self):
            section_id = self.kwargs['section_id']
            setlist_id = self.kwargs['setlist_id']
            return SetlistSectionSong.objects.filter( section_id = section_id, setlist_id= setlist_id)
        model = SetlistSectionSong
        serializer_class = SetlistSectionSongSerializer
        permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsBandMemberOrReadOnly)

class SetlistSectionSongDetail(generics.RetrieveUpdateDestroyAPIView):
        lookup_field = 'id'
        model = SetlistSectionSong
        serializer_class = SetlistSectionSongSerializer
        permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsBandMemberOrReadOnly)