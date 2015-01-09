from django.contrib import admin

from .models import Instrument,Band,User,Song,Setlist,BandUserProfile,UserInstrument,SongPart, SetlistSection,SetlistSectionSong, Comment, Media, Venue, Event, EventAttendance


class BandUserProfileInline(admin.TabularInline):
    model = BandUserProfile
    extra = 1

class BandEventInline(admin.TabularInline):
    model = Event
    extra = 1


class SongPartInline(admin.TabularInline):
    model = SongPart
    extra = 1

class UserInstrumentInline (admin.TabularInline):
    model = UserInstrument
    extra = 1

class BandAdmin(admin.ModelAdmin):
    inlines = [
        BandUserProfileInline, BandEventInline
    ]
#    exclude = ('user','user_instrument',)

class SongPartAdmin(admin.ModelAdmin):
    inlines = [
        SongPartInline
    ]

class UserAdmin(admin.ModelAdmin):
    inlines = [
        UserInstrumentInline
    ]

class SetlistSectionAdmin(admin.ModelAdmin):
    readonly_fields = ('section_length','song_count',)

class SetlistSectionSongAdmin(admin.ModelAdmin):
    readonly_fields = ['song_number']


admin.site.register(Instrument)
admin.site.register(Comment)
admin.site.register(Media)
admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(EventAttendance)
admin.site.register(Song,SongPartAdmin)
admin.site.register(Band,BandAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Setlist)
admin.site.register(SetlistSection, SetlistSectionAdmin)
admin.site.register(SetlistSectionSong,SetlistSectionSongAdmin)