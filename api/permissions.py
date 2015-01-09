
__author__ = 'canozinci'

from rest_framework import permissions
from setlist.models import User, Band, BandUserProfile


class IsBandAdminOrReadOnly(permissions.BasePermission):

    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
           return True

        # Write permissions are only allowed to band_admins


        try:
            band_user_profile = BandUserProfile.objects.get(user=request.user, band=obj.band)
        except BandUserProfile.DoesNotExist:
            band_user_profile = None
        if band_user_profile:
            return band_user_profile.is_band_admin
        return False


class BandDetailIsBandAdminOrReadOnly(permissions.BasePermission):

    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        print "here"
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
           return True

        # Write permissions are only allowed to band_admins

        user = User.objects.get(id=request.user.id)

        try:
            band_user_profile = BandUserProfile.objects.get(user=user, band=obj)
        except BandUserProfile.DoesNotExist:
            band_user_profile = None
        if band_user_profile:
            return band_user_profile.is_band_admin
        return False
    #return obj.owner == user_profile











class IsOwnerOrReadOnly(permissions.BasePermission):


    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
           return True
        return obj.id == request.user.id


    #return obj.owner == user_profile


class IsBandMemberOrReadOnly(permissions.BasePermission):

    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):


        if request.method in permissions.SAFE_METHODS:
           return True


        band_id = view.kwargs['band_id']
        user = request.user

        try:
            band_user_profile = BandUserProfile.objects.get(user=user, band_id=band_id)
        except BandUserProfile.DoesNotExist:
            band_user_profile = None
        return band_user_profile

    def has_permission(self, request, view):


        if request.method in permissions.SAFE_METHODS:
           return True


        band_id = view.kwargs['band_id']
        user = request.user

        try:
            band_user_profile = BandUserProfile.objects.get(user=user, band_id=band_id)
        except BandUserProfile.DoesNotExist:
            band_user_profile = None
        return band_user_profile