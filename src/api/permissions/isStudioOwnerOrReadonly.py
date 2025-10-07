from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

from ..models.studio import Studio

User = get_user_model()


class IsStudioOwnerOrReadOnly(BasePermission):
    """Allow read-only methods to anyone, but restrict write methods to the studio owner.

    The permission works for two kinds of objects:
    - Studio instances: only the `owner` can edit the Studio.
    - Objects linked to a studio through a `studio` attribute (e.g. Client): only
      the owner of that related `studio` can edit the object.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if isinstance(obj, Studio):
            return obj.owner_id == getattr(request.user, "id", None)

        studio = getattr(obj, "studio", None)
        if studio is not None:
            if isinstance(studio, Studio):
                return studio.owner_id == getattr(request.user, "id", None)
            owner = getattr(studio, "owner_id", None) or getattr(studio, "owner", None)
            if owner is not None:
                if hasattr(owner, "id"):
                    return owner.id == getattr(request.user, "id", None)
                return owner == getattr(request.user, "id", None)

        return False
