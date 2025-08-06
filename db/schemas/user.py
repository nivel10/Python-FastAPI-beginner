def user_schema(user) -> dict:
    return {
        'id': str(user['_id']),
        'username': user['username'],
        'first_name': user['first_name'],
        'last_name': user['last_name'],
        'age': user['age'],
        'email': user['email'],
    }