def get_struct(message="", data=None, code=400, success=False):
    return {
        "meta": {
            "message": message,
            "isSuccess": success,
            "statusCode": code
        },
        "data": data
    }


errors = {
    'MethodNotAllowed': get_struct(message="API method not allowed", code=405),
    'NotFound': get_struct(message="API path is not found", code=404),
    'Forbidden': get_struct(message="The request is Bad", code=403),
    'BadRequest': get_struct(message="The request is Bad", code=400),
    'InternalServerError': get_struct(message="Internal server error", code=500),
    'Unauthorized': get_struct(message="Unauthorized access", code=401),
    'Conflict': get_struct(message="Conflict occurred", code=409),
}