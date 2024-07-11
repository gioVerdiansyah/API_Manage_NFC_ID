import datetime

from Models.main import ModelMain
from Helpers.HandlePaginationHelper import get_paginated_data


class SceneAndUnitModel(ModelMain):
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
        data = collection.find(
            {"$or": [{"machine": {"$regex": f".*{query}.*"}}, {"scene_id": {"$regex": f".*{query}.*"}}]})
        return get_paginated_data(cursor=data, page=page)

    def add_scene(self, data):
        collection = self.collection

        data['total_used'] = 0
        data['was_purchased'] = []

        if collection.find_one({"scene_id": data['scene_id']}):
            return {"success": False, "message": "Scene ID is already taken", "code": 409}

        collection.insert_one(data)
        return {"success": True, "message": "Successfully insert new Scene data", "code": 200}

    def update_scene(self, id, data):
        collection = self.collection
        del data['id']

        scene_data = collection.find_one({"_id": id})
        if not scene_data:
            return {"success": False, "message": "ID is not found!", "code": 404}

        if collection.find_one({"scene_id": data['scene_id'], "_id": {"$ne": id}}):
            return {"success": False, "message": "Scene ID is already taken", "code": 409}

        collection.find_one_and_update({"_id": id}, {"$set": data})
        return {"success": True, "message": "Successfully update Scene data", "code": 200}

    def delete_scene(self, id):
        collection = self.collection

        if not collection.find_one({"_id": id}):
            return {"success": False, "message": "ID is not found!", "code": 404}

        collection.find_one_and_delete({"_id": id})
        return {"success": True, "message": "Successfully delete Scene data", "code": 200}

    # Unity
    def check_scene_id(self, id):
        collection = self.collection

        data = collection.find_one({"scene_id": id})

        if not data:
            return {"success": False, "message": "Scene ID is not found!", "code": 404}

        if data['isUsed']:
            return {"success": False, "message": "Scene ID is being used", "code": 409}

        struct = {
            'isUsed': True,
            'latest_used': datetime.datetime.now(),
            'total_used': data['total_used'] + 1
        }

        collection.find_one_and_update({"scene_id": id}, {"$set": struct})
        return {"success": True, "message": "Successfully scan scene", "code": 200}

    def scene_logout(self, id):
        collection = self.collection

        scene_data = collection.find_one({"scene_id": id})

        if not scene_data:
            return {"success": False, "message": "Scene ID is not found!", "code": 404}

        if not scene_data['isUsed']:
            return {"success": False, "message": "Scene has not logged in", "code": 409}

        collection.find_one_and_update({"scene_id": id}, {"$set": {'isUsed': False}})
        return {"success": True, "message": "Successfully Scene logout", "code": 200}

    # User Purchased

    def get_all_data_units(self, page):
        collection = self.collection
        data = get_paginated_data(cursor=collection.find({"was_purchased": {"$exists": True}}), page=page)
        return data

    def add_user_purchased(self, data):
        collection = self.collection
        scene_id = data['scene_id']

        scene_data = collection.find_one({"scene_id": scene_id})

        if not scene_data:
            return {"success": False, "message": "Scene ID is not found!", "code": 404}

        hasExist = collection.find_one({
            "was_purchased": {
                "$elemMatch": {"id": data['unit_id']}
            }
        })

        if hasExist:
            return {"success": False, "message": "Unit ID already taken!", "code": 409}

        payload = {
            "id": data['unit_id'],
            "isUsed": False,
            "last_used": None,
            "buy_at": datetime.datetime.now(),
            "total_used": 0
        }

        collection.update_one(
            {"scene_id": scene_id},
            {"$push": {"was_purchased": payload}}
        )

        return {"success": True, "message": "Successfully add user purchased", "code": 200}

    def update_user_purchased(self, data):
        collection = self.collection
        scene_id = data['scene_id']
        unit_id = data['unit_id']

        scene_data = collection.find_one({"scene_id": scene_id})

        if not scene_data:
            return {"success": False, "message": "Scene ID is not found!", "code": 404}

        hasExist = collection.find_one({
            "scene_id": scene_id,
            "was_purchased": {
                "$elemMatch": {"id": unit_id}
            }
        })

        if not hasExist:
            return {"success": False, "message": "Unit ID not found!", "code": 404}

        index_to_update = next((i for i, item in enumerate(hasExist["was_purchased"]) if item["id"] == unit_id), None)
        if index_to_update is None:
            return {"success": False, "message": "Unit ID not found in was_purchased!", "code": 404}
        print(index_to_update)
        collection.update_one(
            hasExist,
            {"$set": {f"was_purchased.{index_to_update}.id": data['updated_unit_id']}}
        )

        return {"success": True, "message": "Successfully update user purchased", "code": 200}

    def delete_user_purchased(self, data):
        collection = self.collection
        scene_id = data['scene_id']
        unit_id = data['unit_id']

        scene_data = collection.find_one({"scene_id": scene_id})

        if not scene_data:
            return {"success": False, "message": "Scene ID is not found!", "code": 404}

        hasExist = collection.find_one({
            "scene_id": scene_id,
            "was_purchased": {
                "$elemMatch": {"id": unit_id}
            }
        })

        if not hasExist:
            return {"success": False, "message": "Unit ID not found!", "code": 404}

        collection.update_one(
            hasExist,
            {"$pull": {"was_purchased": {"id": unit_id}}}
        )

        return {"success": True, "message": "Successfully delete user purchased", "code": 200}
