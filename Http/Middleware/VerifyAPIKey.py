import os
from functools import wraps
from flask import request
from Helpers.HandleResponseHelper import response


def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        if not api_key:
            return response(message='Missing or invalid API key', isSuccess=False, statusCode=401)

        if api_key != os.getenv("APP_API_KEY"):
            return response(message='Invalid API key!', isSuccess=False, statusCode=401)

        return func(*args, **kwargs)

    return wrapper