import datetime

from Models.main import ModelMain
from Helpers.HandlePaginationHelper import get_paginated_data


class NfcModel(ModelMain):
    def __init__(self):
        super().__init__()
        self.collection = self.mongo_client[self.main_db_name][self.col_2_name]
        self.__setup__()

    def get_all_data(self, page):
        collection = self.collection
        data = get_paginated_data(cursor=collection.find(), page=page)
        return data

    def search_data(self, query, page):
        collection = self.collection
        data = collection.find({"$or": [{"machine": {"$regex": f".*{query}.*"}}, {"nfc_id": {"$regex": f".*{query}.*"}}]})
        return get_paginated_data(cursor=data, page=page)

    def add_nfc(self, data):
        collection = self.collection

        if 'isUsed' not in data:
            data['isUsed'] = False

        data['latest_used'] = None
        data['total_used'] = 0

        if collection.find_one({"nfc_id": data['nfc_id']}):
            return {"success": False, "message": "NFC ID is already taken", "code": 409}

        collection.insert_one(data)
        return {"success": True, "message": "Successfully insert new NFC data", "code": 200}

    def update_nfc(self, id, data):
        collection = self.collection
        del data['id']

        if 'isUsed' not in data:
            data['isUsed'] = False

        nfc_data = collection.find_one({"_id": id})
        if not nfc_data:
            return {"success": False, "message": "ID is not found!", "code": 404}

        if collection.find_one({"nfc_id": data['nfc_id'], "_id": {"$ne": id}}):
            return {"success": False, "message": "NFC ID is already taken", "code": 409}

        collection.find_one_and_update({"_id": id}, {"$set": data})
        return {"success": True, "message": "Successfully update NFC data", "code": 200}

    def delete_nfc(self, id):
        collection = self.collection

        if not collection.find_one({"_id": id}):
            return {"success": False, "message": "ID is not found!", "code": 404}

        collection.find_one_and_delete({"_id": id})
        return {"success": True, "message": "Successfully delete NFC data", "code": 200}

    # Unity
    def check_nfc_id(self, id):
        collection = self.collection

        data = collection.find_one({"nfc_id": id})

        if not data:
            return {"success": False, "message": "NFC ID is not found!", "code": 404}

        if data['isUsed']:
            return {"success": False, "message": "NFC ID is being used", "code": 409}

        struct = {
            'isUsed': True,
            'latest_used': datetime.datetime.now(),
            'total_used': data['total_used'] + 1
        }

        collection.find_one_and_update({"nfc_id": id}, {"$set": struct})
        return {"success": True, "message": "Successfully scan NFC", "code": 200}

    def nfc_logout(self, id):
        collection = self.collection

        nfc_data = collection.find_one({"nfc_id": id})

        if not nfc_data:
            return {"success": False, "message": "NFC ID is not found!", "code": 404}

        if not nfc_data['isUsed']:
            return {"success": False, "message": "NFC has not logged in", "code": 409}

        collection.find_one_and_update({"nfc_id": id}, {"$set": {'isUsed': False}})
        return {"success": True, "message": "Successfully NCF logout", "code": 200}