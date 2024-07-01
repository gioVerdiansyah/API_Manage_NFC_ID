from flask_restful import Resource
from flask import request
from Http.Requests.AddNFCRequest import AddNFCRequest
from Helpers.HandleResponseHelper import response
from Models.NfcModel import NfcModel
from bson.objectid import ObjectId


class AddNFCData(Resource):
    def __init__(self):
        self.model = NfcModel()

    def post(self):
        try:
            json_data = request.get_json()
            nfc_add_req = AddNFCRequest()
            errors = nfc_add_req.validate(json_data)

            if errors:
                return response(message="Error Validation", data=errors, isSuccess=False, statusCode=400)

            model = self.model.add_nfc(data=json_data)
            if model['success']:
                return response(message=model['message'])
            else:
                return response(message=model['message'], data="Try check your data again", isSuccess=False,
                                statusCode=403)
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)


class UpdateNFCData(Resource):
    def __init__(self):
        self.model = NfcModel()

    def put(self, id):
        try:
            json_data = request.get_json()
            nfc_add_req = AddNFCRequest()
            errors = nfc_add_req.validate(json_data)

            if errors:
                return response(message="Error Validation", data=errors, isSuccess=False, statusCode=400)

            model = self.model.update_nfc(id=ObjectId(id), data=json_data)

            if model['success']:
                return response(message=model['message'])
            else:
                return response(message=model['message'], data="Try check your data again", isSuccess=False,
                                statusCode=403)
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)


class DeleteNFCData(Resource):
    def __init__(self):
        self.model = NfcModel()

    def delete(self, id):
        try:
            model = self.model.delete_nfc(id=ObjectId(id))

            if model['success']:
                return response(message=model['message'])
            else:
                return response(message=model['message'], data="Try check your data again", isSuccess=False,
                                statusCode=403)

        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)
