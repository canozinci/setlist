__author__ = 'canozinci'

import datetime
from django.utils.timezone import utc

from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework import exceptions

class QuietBasicAuthentication(BasicAuthentication):

    # disclaimer: once the user is logged in, this should NOT be used as a
    # substitute for SessionAuthentication, which uses the django session cookie,
    # rather it can check credentials before a session cookie has been granted.
    def authenticate_header(self, request):
        return 'xBasic realm="%s"' % self.www_authenticate_realm



class ExpiringTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):

        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        utc_now = datetime.datetime.utcnow().replace(tzinfo=utc)

        if token.created < utc_now - datetime.timedelta(days=30):
            raise exceptions.AuthenticationFailed('Token has expired')

        return (token.user, token)