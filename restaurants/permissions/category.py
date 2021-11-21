from rest_access_policy import AccessPolicy


class CategoryManageAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ("<safe_methods>", "create", "update", "destroy"),
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
