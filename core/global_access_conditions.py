""""
Global reusable permissions
"""
from users.models import User


def is_manager(request, view, action) -> bool:
    """
    Check request user is a manager
    """
    return request.user.role == User.RoleTypeChoices.MANAGER
