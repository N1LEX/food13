from rest_access_policy import AccessPolicy


class RestaurantManageAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ("<safe_methods>", "create", "destroy", "update", "hide", "activate"),
            "principal": "admin",
            "effect": "allow",
        },
        {
            "action": ("<safe_methods>", "<method:put>", "<method:patch>", "hide", "activate"),
            "principal": "authenticated",
            "effect": "allow",
            "condition": "is_manager",
        },
    ]
