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
        "duration":str(queuer['duration']) +" hour(s)",
        "rate":"₦ "+ str(queuer['rate']),
        "created_at":queuer['created_at'],
    }
    
    
def queue_request_serializer(request) -> dict:
    return {
        "id":str(request['_id']),
        "zip_code":request['zip_code'],
        "address":request['address'],
        "duration":str(request['duration']) +" minutes",
        "status":request['status'],
        "client_id":str(request['client_id']),
        "created_at":request['created_at'],
    }
    
def applied_request_serializer(request) -> dict:
    return {
        "id":str(request['_id']),
        "request_id": str(request["request_id"]),
        "client_id": str(request["client_id"]),
        "queuer_id": str(request["queuer_id"]),
        "duration": str(round((request["duration"] / 60), 1)),
        "address": request["address"] ,
        "total": "₦ "+ str(request["total"]),
        "zip_code": request["zip_code"],
        "status":request["status"],
        "created_at":request["created_at"],
        }

def auth_serializer(auth) -> dict:
    return {

    }



def list_serializer(result, serializer) -> list:
    return [serializer(data) for data in result]