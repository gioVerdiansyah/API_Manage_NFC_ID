import datetime
from Helpers.HandleGenerateJWTToken import jwt_generate, check_token_valid
from Models.main import ModelMain
from bson.objectid import ObjectId

class AuthModel(ModelMain):
    def __init__(self):
        super().__init__()
        self.collection = self.mongo_client[self.main_db_name][self.col_1_name]
        self.__setup__()

    def login_record(self):
        collection = self.collection
        _id = ObjectId()
        data = {
            '_id': _id,
            "login_date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
            'token': jwt_generate(str(_id))
        }
        collection.insert_one(data)

        return {"success": True, "message": "Successfully login!", "data": str(data['token'])}

    def logout_delete(self, token):
        collection = self.collection
        jwt_process = self.check_token(token)
        if not jwt_process['success']:
            return {"success": False, "message": jwt_process['message']}

        data = jwt_process['data']
        collection.delete_one({"_id": data['_id']})
        return {"success": True, "message": "Successfully logout"}

    def check_token(self, token):
        collection = self.collection

        jwt_token = check_token_valid(token)
        if not jwt_token['success']:
            return {"success": False, "message": jwt_token['message']}

        data = collection.find_one({"token": token})
        if not data:
            return {"success": False, "message": "Invalid token!"}

        return {"success": True, "message": "Token is valid!", "data": data}
