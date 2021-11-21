from rest_access_policy import AccessPolicy


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
            "condition": "is_manager",
        },
    ]
