from flask_restful import Resource
from flask import request
from Http.Requests.NeedIDRequest import NeedIDRequest
from Helpers.HandleResponseHelper import response
from Models.SceneAndUnitModel import SceneAndUnitModel


class SceneLogoutController(Resource):
    def post(self):
        try:
            json_data = request.get_json()
            check_id = NeedIDRequest()
            errors = check_id.validate(json_data)

            if errors:
                return response(message="Error Validation", data=errors, isSuccess=False, statusCode=400)

            nfc_model = SceneAndUnitModel()
            nfc_logout = nfc_model.nfc_logout(json_data['id'])

            return response(nfc_logout['message'], isSuccess=nfc_logout['success'], statusCode=nfc_logout['code'])
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)
