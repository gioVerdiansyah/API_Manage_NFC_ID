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
            return {"success": False, "message": "NFC ID is already taken"}

        collection.insert_one(data)
        return {"success": True, "message": "Successfully insert new NFC data"}

    def update_nfc(self, id, data):
        collection = self.collection
        del data['id']

        if 'isUsed' not in data:
            data['isUsed'] = False

        if not collection.find_one({"_id": id}):
            return {"success": False, "message": "ID is not found!"}

        if collection.find_one({"nfc_id": data['nfc_id'], "_id": {"$ne": id}}):
            return {"success": False, "message": "NFC ID is already taken"}

        collection.find_one_and_update({"_id": id}, {"$set": data})
        return {"success": True, "message": "Successfully update NFC data"}

    def delete_nfc(self, id):
        collection = self.collection

        if not collection.find_one({"_id": id}):
            return {"success": False, "message": "ID is not found!"}

        collection.find_one_and_delete({"_id": id})
        return {"success": True, "message": "Successfully delete NFC data"}

    # Unity
    def check_nfc_id(self, id):
        collection = self.collection

        if not collection.find_one({"nfc_id": id}):
            return {"success": False, "message": "NFC ID is not found!"}

        collection.find_one_and_update({"nfc_id": id}, {"$set": {'isUsed': True}})
        return {"success": True, "message": "Successfully scan NFC"}

    def nfc_logout(self, id):
        collection = self.collection

        if not collection.find_one({"nfc_id": id}):
            return {"success": False, "message": "NFC ID is not found!"}

        collection.find_one_and_update({"nfc_id": id}, {"$set": {'isUsed': False}})
        return {"success": True, "message": "Successfully NCF logout"}