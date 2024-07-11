from flask_restful import Resource
from flask import request
from Http.Requests.StoreSceneRequest import StoreSceneRequest
from Http.Requests.UpdateSceneRequest import UpdateSceneRequest
from Http.Requests.NeedIDRequest import NeedIDRequest
from Helpers.HandleResponseHelper import response
from Models.SceneAndUnitModel import SceneAndUnitModel
from bson.objectid import ObjectId


class SceneController(Resource):
    def __init__(self):
        self.model = SceneAndUnitModel()

    def get(self):
        page = request.args.get('page', default=1, type=int)
        data = self.model.get_all_data(page=page)
        return response(data=data)

    def post(self):
        try:
            json_data = request.get_json()
            json_data.pop("id", None)
            scene_add_req = StoreSceneRequest()
            errors = scene_add_req.validate(json_data)

            if errors:
                return response(message="Error Validation", data=errors, isSuccess=False, statusCode=400)

            model = self.model.add_scene(data=json_data)
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
            scene_update_req = UpdateSceneRequest()
            errors = scene_update_req.validate(json_data)

            if errors:
                return response(message="Error Validation", data=errors, isSuccess=False, statusCode=400)

            id = json_data['id']

            model = self.model.update_scene(id=ObjectId(id), data=json_data)

            return response(message=model['message'], isSuccess=model['success'], statusCode=model['code'])
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
            model = self.model.delete_scene(id=ObjectId(id))

            return response(message=model['message'], isSuccess=model['success'], statusCode=model['code'])

        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)


class SceneSearchController(Resource):
    def __init__(self):
        self.model = SceneAndUnitModel()

    def get(self, query):
        try:
            page = request.args.get('page', default=1, type=int)
            data = self.model.search_data(query=query, page=page)

            return response(data=data)
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)
