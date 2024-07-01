from Models.main import ModelMain


class NfcModel(ModelMain):
    def __init__(self):
        super().__init__()
        self.collection = self.mongo_client[self.main_db_name][self.col_2_name]
        self.__setup__()

    def add_nfc(self, data):
        collection = self.collection

        if 'isUsed' not in data:
            data['isUsed'] = False

        if collection.find_one({"nfc_id": data['nfc_id']}):
            return {"success": False, "message": "NFC ID is already used"}

        collection.insert_one(data)
        return {"success": True, "message": "Successfully insert new NFC data"}