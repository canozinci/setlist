from django.conf.urls import patterns, include, url
from django.contrib import admin
import api.urls
from setlist.views import OnePageAppView,OnePageAppView2,TestIndexView
from django.conf.urls.static import static

from django.conf import settings

admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'setlist.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api.urls)),
    url(r'^$', OnePageAppView.as_view(), name='home'),
    url(r'^test/', OnePageAppView2.as_view(), name='home'),
    url(r'^test1/', TestIndexView.as_view(), name='home')

    )+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )

urlpatterns += patterns('',
                        url('^.*$', OnePageAppView.as_view(), name='index'),
                        )