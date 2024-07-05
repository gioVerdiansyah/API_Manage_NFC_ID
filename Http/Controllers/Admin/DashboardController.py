from flask_restful import Resource
from Helpers.HandleResponseHelper import response
from Models.DashboardModel import DashboardModel


class DashboardController(Resource):
    def __init__(self):
        self.model = DashboardModel()

    def get(self):
        try:
            data = self.model.get_data_dashboard()

            return response(data=data['data'], isSuccess=data['success'], statusCode=data['code'])
        except Exception as e:
            return response(message="There is a server error!", data=str(e), isSuccess=False, statusCode=500)