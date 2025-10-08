def get_client_ip(request):
    """Retrieve the client's IP address from the request object."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_current_user(request):
    """Retrieve the current authenticated user from the request object."""
    if request.user and request.user.is_authenticated:
        return request.user
    return None
