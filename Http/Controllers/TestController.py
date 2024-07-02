from flask_restful import Resource

class TestController(Resource):
    def post(self):
        return "Tested"