import datetime

from Models.main import ModelMain

class AuthModel(ModelMain):
    def __init__(self):
        super().__init__()
        self.collection = self.mongo_client[self.main_db_name][self.col_1_name]
        self.__setup__()

    def login_record(self):

        collection = self.collection
        collection.insert_one({
            "login_date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
            "logout_date": "00/00/0000 00:00"
        })