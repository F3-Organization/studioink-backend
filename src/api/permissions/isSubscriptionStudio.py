from rest_framework.permissions import BasePermission

from api.models.studio import Studio


class IsStudioSubscription(BasePermission):
    """
    Allows access only to users with a Studio plan.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and Studio.objects.filter(
                owner=request.user, subscription_plan=Studio.SubscriptionPlan.STUDIO
            ).exists()
        )
