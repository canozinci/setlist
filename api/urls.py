__author__ = 'canozinci'

from django.conf.urls import patterns, include, url
from .api import BandList, BandDetail, BandUserProfileList,UserList,UserDetail, AuthView,ObtainExpiringAuthToken, UserGenerate, BandSongList, SongDetail, UserInstrumentList, UserInstrumentDetail, SongPartDetail, SongPartList, SongPartCreate,CreateSongComment,CreateSongMedia ,BandActionList, SetlistList, SetlistDetail, SetlistSectionList, SetlistSectionDetail, SetlistSectionSongList, SetlistSectionSongDetail, SetlistNested, CreateSetlistComment, BandEventList, BandEventDetail, AttendaceEventList, SongDetailUnnested
from actstream import urls



band_urls = patterns('',
    url(r'^/$', BandList.as_view(), name='band-list'),
    url(r'^/(?P<id>\d+)$', BandDetail.as_view(), name='band-detail'),
    url(r'^/(?P<band_id>\d+)/members/$', BandUserProfileList.as_view(), name='band-userprofile-list'),
    url(r'^/(?P<band_id>\d+)/events/$', BandEventList.as_view(), name='band-events-list'),
    url(r'^/(?P<band_id>\d+)/events/(?P<id>\d+)/$', BandEventDetail.as_view(), name='band-evet-detail'),

    url(r'^/(?P<band_id>\d+)/events/(?P<event_id>\d+)/attendance/$', AttendaceEventList.as_view(), name='band-evet-attendace-list'),

    url(r'^/(?P<band_id>\d+)/actions/$', BandActionList.as_view(), name='band-detail'),
    url(r'^/(?P<band_id>\d+)/songs/$', BandSongList.as_view(), name='band-song-list'),


    url(r'^/(?P<band_id>\d+)/setlists/$', SetlistList.as_view(), name='band-setlist-list'),
    url(r'^/(?P<band_id>\d+)/setlists/(?P<id>\d+)/$', SetlistDetail.as_view(), name='band-setlist-detail'),
    url(r'^/(?P<band_id>\d+)/setlists/(?P<id>\d+)/createcomments/$', CreateSetlistComment.as_view(), name='create-setlist-comments'),
    url(r'^/(?P<band_id>\d+)/setlists/(?P<id>\d+)/nested/$', SetlistNested.as_view(), name='band-setlist-nested-detail'),

    url(r'^/(?P<band_id>\d+)/setlists/(?P<setlist_id>\d+)/sections/$', SetlistSectionList.as_view(), name='band-setlistsection-list'),
    url(r'^/(?P<band_id>\d+)/setlists/(?P<setlist_id>\d+)/sections/(?P<id>\d+)/$', SetlistSectionDetail.as_view(), name='band-setlistsection-detail'),

    url(r'^/(?P<band_id>\d+)/setlists/(?P<setlist_id>\d+)/sections/(?P<section_id>\d+)/songs/$', SetlistSectionSongList.as_view(), name='band-setlistsection-list'),
    url(r'^/(?P<band_id>\d+)/setlists/(?P<setlist_id>\d+)/sections/(?P<section_id>\d+)/songs/(?P<id>\d+)/$', SetlistSectionSongDetail.as_view(), name='band-setlistsection-detail'),

    url(r'^/(?P<band_id>\d+)/songs/(?P<song_id>\d+)/$', SongPartList.as_view(), name='song-part-detail'),
    url(r'^/(?P<band_id>\d+)/songs/(?P<song_id>\d+)/createcomments/$', CreateSongComment.as_view(), name='create-comments'),
    url(r'^/(?P<band_id>\d+)/songs/(?P<song_id>\d+)/createmedia/$', CreateSongMedia.as_view(), name='create-comments'),
    url(r'^/(?P<band_id>\d+)/songs/(?P<song_id>\d+)/parts/$', SongPartCreate.as_view(), name='song-part-create'),
    url(r'^/(?P<band_id>\d+)/songs/(?P<song_id>\d+)/parts/(?P<id>\d+)/$', SongPartDetail.as_view(), name='song-part-detail'),
)

user_urls = patterns('',
    url(r'^/$', UserList.as_view(), name='userprofile-list'),
    url(r'^/(?P<id>\d+)$', UserDetail.as_view(), name='userprofile-detail'),
    #url(r'^/(?P<user_id>\d+)/instruments/(?P<id>\d+)$', UserInstrumentDetail.as_view(), name='userinstrument-detail-specific-user'),
    url(r'^/instruments/(?P<id>\d+)$', UserInstrumentDetail.as_view(), name='userinstrument-detail'),
    url(r'^/(?P<user_id>\d+)/instruments/$', UserInstrumentList.as_view(), name='userinstrument-list'),


    url(r'^usergenerate/$', UserGenerate.as_view(), name='user-generate'),
)

song_urls = patterns('',
    url(r'^/(?P<id>\d+)$', SongDetail.as_view(), name='song-detail'),
    url(r'^/(?P<id>\d+)/songedit/$', SongDetailUnnested.as_view(), name='song-detail-unnested'),

)



urlpatterns = patterns('',
    url(r'^bands', include(band_urls)),
    url(r'^songs', include(song_urls)),
    url(r'^users', include(user_urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^auth', AuthView.as_view(), name='authenticate'),
    url(r'^token-auth/(?P<backend>\S+)$', ObtainExpiringAuthToken.as_view(),name='token-authenticate'),
    url(r'^activity/', include('actstream.urls')),
)

