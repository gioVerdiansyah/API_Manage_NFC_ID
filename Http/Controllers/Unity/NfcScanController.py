from flask_restful import Resource
from flask import request
from Helpers.HandleResponseHelper import response
from Http.Requests.NeedIDRequest import NeedIDRequest
from Models.NfcModel import NfcModel


class NfcScanController(Resource):
    def post(self):
        try:
            json_data = request.get_json()
            check_id = NeedIDRequest()
            errors = check_id.validate(json_data)

            if errors:
                return response(message="Error Validation", data=errors, isSuccess=False, statusCode=400)

            nfc_model = NfcModel()
            result = nfc_model.check_nfc_id(json_data['id'])

            return response(result['message'], isSuccess=result['success'], statusCode=result['code'])
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)
