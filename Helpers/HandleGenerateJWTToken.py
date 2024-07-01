import os

import jwt
from datetime import datetime, timedelta
from flask import jsonify


def jwt_generate(id):
    payload = {
        'id': id,
        'username': 'Akihiko_Kayaba',
        'exp': datetime.utcnow() + timedelta(days=3)
    }

    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM")
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    return token


def check_token_valid(token):
    try:
        secret_key = os.getenv("SECRET_KEY")
        algorithm = os.getenv("ALGORITHM")
        decoded_data = jwt.decode(token, secret_key, algorithms=[algorithm])
        return {"success": True, "message": "token is valid!", "data": jsonify(decoded_data)}
    except jwt.ExpiredSignatureError:
        return {"success": False, "message": "token is expired!"}
    except jwt.InvalidTokenError:
        return {"success": False, "message": "token is invalid!"}
