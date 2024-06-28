import os
import json

from pymongo import MongoClient
from dotenv import load_dotenv


class ModelMain:
    def __init__(self):
        load_dotenv()
        self.mongo_client = MongoClient(os.getenv("MONGO_URL"))
        self.main_db_name = os.getenv("MAIN_DB")
        self.col_1_name = "login_histories"
        self.col_2_name = "3d_machine"

    def __setup__(self):
        db = self.mongo_client[self.main_db_name]

        if self.col_1_name not in db.list_collection_names():
            with open("Models/Schemas/login_histories.json", 'r') as f:
                schema = json.load(f)
            db.create_collection(self.col_1_name, validator=schema)

        if self.col_2_name not in db.list_collection_names():
            with open("Models/Schemas/3d_machine.json", 'r') as f:
                schema = json.load(f)
            db.create_collection(self.col_2_name, validator=schema)
