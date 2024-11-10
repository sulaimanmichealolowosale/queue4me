def collection_serializer(collection)-> dict:
    return {
        "id": str(collection['_id']),
        "title":collection['title'],
        "name":collection['name'],
        "description":collection['description'],
        "created_at":collection['created_at']
    }

def user_serializer(user) -> dict:
    return {
        "id":str(user['_id']),
        "username":user['username'],
        "email":user['email'],
        "role":user['role'],
        "created_at":user['created_at'],
    }


def queuer_profile_serializer(queuer) -> dict:
    return {
        "id":str(queuer['_id']),
        "zip_code":queuer['zip_code'],
        "duration":queuer['duration'],
        "rate":queuer['rate'],
        "created_at":queuer['created_at'],
    }

def auth_serializer(auth) -> dict:
    return {

    }



def list_serializer(result, serializer) -> list:
    return [serializer(data) for data in result]