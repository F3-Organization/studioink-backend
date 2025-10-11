from rest_framework.permissions import BasePermission

from api.models.studio import Studio


class IsStudioSubscription(BasePermission):
    """
    Allows access only to users with a Studio plan.
    """

    def has_permission(self, request, view):
        permission = bool(
            request.user
            and request.user.is_authenticated
            and Studio.objects.filter(
                owner=request.user, subscription_plan=Studio.SubscriptionPlan.STUDIO
            ).exists()
            or request.user.is_staff
        )
        if permission is False:
            view.permission_denied(
                request,
                message="User does not have a Studio subscription plan.",
            )
        return permission
