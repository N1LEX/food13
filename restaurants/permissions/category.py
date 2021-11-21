from rest_access_policy import AccessPolicy

from users.models import User


class CategoryManageAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ("<safe_methods>", "create", "update", "destroy"),
            "principal": "admin",
            "effect": "allow",
        },
        {
            "action": ("<safe_methods>", "create", "destroy", "<method:put>", "<method:patch>"),
            "principal": "authenticated",
            "effect": "allow",
            "condition": "is_manager"
        },
    ]

    def is_manager_of_restaurant(self, request, view, action) -> bool:
        """
        Check request user is a manager
        """
        user = request.user
        category = view.get_object()
        return user.restaurants.filter(id=category.restaurant.id).exists() and user.role == User.RoleTypeChoices.MANAGER
