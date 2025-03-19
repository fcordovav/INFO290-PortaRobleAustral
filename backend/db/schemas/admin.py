def admin_schema(admin) -> dict:
    return {
        "id": str(admin["_id"]),
        "username": admin["username"],
        "password": admin["password"],
        "nickname": admin["nickname"],
        "correo": admin["correo"]
    }

def admins_schema(admins) -> list:
    return [admin_schema(admin) for admin in admins]

