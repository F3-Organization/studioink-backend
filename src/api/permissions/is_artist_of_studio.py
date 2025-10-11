from rest_framework import permissions

from api.models.artist import ArtistProfile


class IsArtistOfStudio(permissions.BasePermission):
    def has_permission(self, request, view):
        return ArtistProfile.objects.filter(user=request.user).exists() or bool(
            request.user.is_staff
        )
