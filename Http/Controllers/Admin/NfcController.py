from flask_restful import Resource
from flask import request
from Http.Requests.StoreNFCRequest import StoreNFCRequest
from Http.Requests.UpdateNFCRequest import UpdateNFCRequest
from Http.Requests.NeedIDRequest import NeedIDRequest
from Helpers.HandleResponseHelper import response
from Models.NfcModel import NfcModel
from bson.objectid import ObjectId


class NfcController(Resource):
    def __init__(self):
        self.model = NfcModel()

    def get(self):
        page = request.args.get('page', default=1, type=int)
        data = self.model.get_all_data(page=page)
        return response(data=data)

    def post(self):
        try:
            json_data = request.get_json()
            nfc_add_req = StoreNFCRequest()
            errors = nfc_add_req.validate(json_data)

            if errors:
                return response(message="Error Validation", data=errors, isSuccess=False, statusCode=400)

            model = self.model.add_nfc(data=json_data)
            if model['success']:
                return response(message=model['message'])
            else:
                return response(message=model['message'], isSuccess=False,
                                statusCode=422)
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)

    def put(self):
        try:
            json_data = request.get_json()
            nfc_update_req = UpdateNFCRequest()
            errors = nfc_update_req.validate(json_data)

            if errors:
                return response(message="Error Validation", data=errors, isSuccess=False, statusCode=400)

            id = json_data['id']

            model = self.model.update_nfc(id=ObjectId(id), data=json_data)

            return response(message=model['message'],isSuccess=model['success'], statusCode=model['code'])
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)

    def delete(self):
        try:
            json_data = request.get_json()
            need_id = NeedIDRequest()
            errors = need_id.validate(json_data)
            if errors:
                return response(message="Error Validation", data=errors, isSuccess=False, statusCode=400)
            id = json_data['id']
            model = self.model.delete_nfc(id=ObjectId(id))

            return response(message=model['message'],isSuccess=model['success'], statusCode=model['code'])

        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)
