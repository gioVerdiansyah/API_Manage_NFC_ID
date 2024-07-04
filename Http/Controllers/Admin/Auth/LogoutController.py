from flask_restful import Resource
from flask import request
from Http.Requests.LoginRequest import LoginRequest
from Helpers.HandleResponseHelper import response
from Models.AuthModel import AuthModel


class Logout(Resource):
    def post(self):
        try:
            token = request.headers.get("Authorization").split("Bearer ")[1]
            rec = AuthModel()
            data_rec = rec.logout_delete(token=token)

            return response(message=data_rec['message'], isSuccess=data_rec['success'], statusCode=data_rec['code'])
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)