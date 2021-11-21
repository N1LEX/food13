from rest_access_policy import AccessPolicy


class KitchenAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ("create", "destroy", "<method:put>", "<method:patch>"),
            "principal": "admin",
            "effect": "allow",
        },
        {
            "action": "<safe_methods>",
            "principal": "*",
            "effect": "allow",
        },
    ]
