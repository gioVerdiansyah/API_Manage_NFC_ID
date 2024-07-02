import os

from flask_restful import Resource
from flask import request
from Http.Requests.LoginRequest import LoginRequest
from Helpers.HandleResponseHelper import response
from Models.AuthModel import AuthModel


class Login(Resource):
    def post(self):
        try:
            json_data = request.get_json()
            login_request = LoginRequest()
            errors = login_request.validate(json_data)

            if errors:
                return response(message="Error Validation", data=errors, isSuccess=False, statusCode=400)

            if (json_data['email'] == os.getenv("ADMIN_EMAIL")) and (
                    json_data['password'] == os.getenv("ADMIN_PASSWORD")):
                rec = AuthModel()
                data_rec = rec.login_record()
                return response(message=data_rec['message'], data=data_rec['data'])

            return response(message="Email or password is incorrect", data="Email or password is incorrect",
                            isSuccess=False, statusCode=403)
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)
