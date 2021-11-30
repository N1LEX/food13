from rest_access_policy import AccessPolicy


class ProductPortionManageAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ("<safe_methods>", "create", "<method:put>", "<method:patch>", "destroy", "hide", "activate"),
            "principal": "admin",
            "effect": "allow",
        },
        {
            "action": ("<safe_methods>", "create", "destroy", "<method:put>", "<method:patch>", "hide", "activate"),
            "principal": "authenticated",
            "effect": "allow",
            "condition": "is_manager"
        },
    ]
