from Models.main import ModelMain
from Helpers.HandlePaginationHelper import get_paginated_data


class NfcModel(ModelMain):
    def __init__(self):
        super().__init__()
        self.collection = self.mongo_client[self.main_db_name][self.col_2_name]
        self.__setup__()

    def get_all_data(self, page):
        collection = self.collection
        data = get_paginated_data(collection=collection, page=page)
        return data
    def add_nfc(self, data):
        collection = self.collection

        if 'isUsed' not in data:
            data['isUsed'] = False

        if collection.find_one({"nfc_id": data['nfc_id']}):
            return {"success": False, "message": "NFC ID is already taken", "code": 409}

        collection.insert_one(data)
        return {"success": True, "message": "Successfully insert new NFC data", "code": 200}

    def update_nfc(self, id, data):
        collection = self.collection
        del data['id']

        if 'isUsed' not in data:
            data['isUsed'] = False

        if not collection.find_one({"_id": id}):
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

        collection.find_one_and_update({"nfc_id": id}, {"$set": {'isUsed': True}})
        return {"success": True, "message": "Successfully scan NFC", "code": 200}

    def nfc_logout(self, id):
        collection = self.collection

        if not collection.find_one({"nfc_id": id}):
            return {"success": False, "message": "NFC ID is not found!", "code": 404}

        collection.find_one_and_update({"nfc_id": id}, {"$set": {'isUsed': False}})
        return {"success": True, "message": "Successfully NCF logout", "code": 200}