from rest_access_policy import AccessPolicy

from users.models import User


class RestaurantManageAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ("create", "destroy", "update"),
            "principal": "admin",
            "effect": "allow",
        },
        {
            "action": "<safe_methods>",
            "principal": "authenticated",
            "effect": "allow",
        },
        {
            "action": ("<method:put>", "<method:patch>", "add_user", "remove_user"),
            "principal": "authenticated",
            "effect": "allow",
            "condition": "is_manager_of_restaurant",
        },
    ]

    def is_manager_of_restaurant(self, request, view, action) -> bool:
        """
        Check request user is a manager
        """
        user = request.user
        restaurant = view.get_object()
        return user.restaurants.filter(id=restaurant.id).exists() and user.role == User.RoleTypeChoices.MANAGER
