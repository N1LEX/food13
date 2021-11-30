from rest_access_policy import AccessPolicy


class KitchenManageAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": "*",
            "principal": "admin",
            "effect": "allow",
        },
    ]
