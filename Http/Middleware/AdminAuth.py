import os
from functools import wraps
from flask import request
from Helpers.HandleResponseHelper import response
from Models.AuthModel import AuthModel


def require_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method == 'OPTIONS':
            return
        try:
            token = request.headers.get('Authorization')
            if not token or not token.startswith('Bearer '):
                return response(message='Missing token', isSuccess=False, statusCode=401)
            auth_model = AuthModel()
            check_token = auth_model.check_token(token=token.split('Bearer ')[1])

            if not check_token['success']:
                return response(message="Invalid token!", isSuccess=False, statusCode=401)

            return func(*args, **kwargs)
        except Exception as e:
            return response(message=str(e), isSuccess=False, statusCode=500)

    return wrapper
