from flask_restful import Resource
from flask import request
from Models.SceneAndUnitModel import SceneAndUnitModel
from Helpers.HandleResponseHelper import response
from Http.Requests.StoreUserPurchasedRequest import StoreUserPurchasedRequest
from Http.Requests.UpdateUserPurchasedRequest import UpdateUserPurchasedRequest


class UnitsPurchasedController(Resource):
    def __init__(self):
        self.model = SceneAndUnitModel()

    def get(self):
        page = request.args.get('page', default=1, type=int)
        data = self.model.get_all_data_units(page=page)
        return response(data=data)



    def post(self):
        try:
            json_data = request.get_json()
            if 'scene_id' not in json_data and 'unit_id' not in json_data:
                json_data['scene_id'] = json_data['scene_id_after']
                json_data['unit_id'] = json_data['updated_unit_id']
            json_data.pop("scene_id_after", None)
            json_data.pop("updated_unit_id", None)
            need_id = StoreUserPurchasedRequest()
            errors = need_id.validate(json_data)
            if errors:
                return response(message="Error Validation", data=errors, isSuccess=False, statusCode=400)

            model = self.model.add_user_purchased(json_data)
            return response(message=model['message'], isSuccess=model['success'], statusCode=model['code'])
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)

    def put(self):
        try:
            json_data = request.get_json()
            if 'scene_id_before' not in json_data or 'scene_id_after' not in json_data:
                json_data['scene_id_before'] = json_data.get('scene_id')
                json_data['scene_id_after'] = json_data.get('scene_id')

            if 'updated_unit_id' not in json_data:
                json_data['updated_unit_id'] = json_data['unit_id']

            json_data.pop("scene_id", None)
            need_id = UpdateUserPurchasedRequest()
            errors = need_id.validate(json_data)
            if errors:
                return response(message="Error Validation", data=errors, isSuccess=False, statusCode=400)

            model = self.model.update_user_purchased(json_data)
            return response(message=model['message'], isSuccess=model['success'], statusCode=model['code'])
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)

    def delete(self):
        try:
            json_data = request.get_json()
            need_id = StoreUserPurchasedRequest()
            errors = need_id.validate(json_data)
            if errors:
                return response(message="Error Validation", data=errors, isSuccess=False, statusCode=400)

            model = self.model.delete_user_purchased(json_data)
            return response(message=model['message'], isSuccess=model['success'], statusCode=model['code'])
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)


class UnitSearchController(Resource):
    def __init__(self):
        self.model = SceneAndUnitModel()

    def get(self, query):
        try:
            page = request.args.get('page', default=1, type=int)
            data = self.model.search_data_units(search_id=query, page=page)

            return response(data=data)
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)
