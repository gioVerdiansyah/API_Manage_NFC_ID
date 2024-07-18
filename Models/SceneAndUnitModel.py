import datetime

from Models.main import ModelMain
from Helpers.HandlePaginationHelper import get_paginated_data, get_paginated_data_user_purchased, \
    get_paginate_data_with_search


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
        return get_paginated_data(cursor=data, page=page, per_page=10)

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

    # For Unity
    def check_scene_id(self, data):
        collection = self.collection
        scene_id = data['scene_id']
        unit_id = data['unit_id']

        result = collection.find_one(
            {"scene_id": scene_id, "was_purchased.id": unit_id},
            {"was_purchased.$": 1, "machine_name": 1, "scene_id": 1, 'total_used': 1}
        )

        if not result:
            return {"success": False, "message": "Scene ID or Unit ID not found!", "code": 404}

        purchase_data = result['was_purchased'][0]

        if purchase_data['isUsed']:
            return {"success": False, "message": "Unit ID is already used!", "code": 409}

        updated_data = {
            "isUsed": True,
            "total_used": purchase_data['total_used'] + 1
        }

        collection.update_one(
            {"scene_id": scene_id, "was_purchased.id": unit_id},
            {"$set": {
                "was_purchased.$.isUsed": updated_data["isUsed"],
                "was_purchased.$.total_used": updated_data["total_used"],
                "total_used": result["total_used"] + 1
            }}
        )

        purchase_data.update(updated_data)

        return {
            "success": True,
            "message": "Successfully login unit!",
            "code": 200,
            "data": purchase_data
        }

    def scene_logout(self, data):
        collection = self.collection
        scene_id = data['scene_id']
        unit_id = data['unit_id']

        result = collection.find_one(
            {"scene_id": scene_id, "was_purchased.id": unit_id},
            {"was_purchased.$": 1, "machine_name": 1, "scene_id": 1}
        )

        if not result:
            return {"success": False, "message": "Scene ID or Unit ID not found!", "code": 404}

        purchase_data = result['was_purchased'][0]

        if not purchase_data['isUsed']:
            return {"success": False, "message": "Unit ID has not logged in!", "code": 409}

        updated_data = {
            "isUsed": False,
            "last_used": datetime.datetime.now()
        }

        collection.update_one(
            {"scene_id": scene_id, "was_purchased.id": unit_id},
            {"$set": {"was_purchased.$.isUsed": updated_data["isUsed"],
                      "was_purchased.$.last_used": updated_data["last_used"]}}
        )

        purchase_data.update(updated_data)

        return {
            "success": True,
            "message": "Successfully logout unit!",
            "code": 200,
            "data": purchase_data
        }

    # User Purchased

    def get_all_data_units(self, page=1):
        query = self.collection.find({"was_purchased": {"$exists": True}},
                                     {"machine_name": 1, "scene_id": 1, "was_purchased": 1})

        filtered_data = get_paginated_data_user_purchased(query, per_page=10, page=page)
        return filtered_data

    def search_data_units(self, page=1, search_id=None):
        query = self.collection.find({"was_purchased": {"$exists": True}},
                                     {"machine_name": 1, "scene_id": 1, "was_purchased": 1})

        filtered_data = get_paginate_data_with_search(query, per_page=10, page=page, search_keyword=search_id)
        return filtered_data

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

        return {"success": True, "message": "Successfully add unit purchased", "code": 200}

    def update_user_purchased(self, data):
        collection = self.collection
        scene_id_before = data['scene_id_before']
        scene_id_after = data['scene_id_after']
        unit_id = data['unit_id']
        updated_unit_id = data['updated_unit_id']

        scene_data = collection.find_one({"scene_id": scene_id_before})

        if not scene_data:
            return {"success": False, "message": "Scene ID is not found!", "code": 404}

        hasExist = collection.find_one({
            "scene_id": scene_id_before,
            "was_purchased": {
                "$elemMatch": {"id": unit_id}
            }
        })

        if not hasExist:
            return {"success": False, "message": "Unit ID not found!", "code": 404}

        index_to_update = next((i for i, item in enumerate(hasExist["was_purchased"]) if item["id"] == unit_id), None)
        if index_to_update is None:
            return {"success": False, "message": "Unit ID not found in was_purchased!", "code": 404}

        if scene_id_after != scene_id_before:
            payload_with_old_data = collection.aggregate([
                {"$match": {"scene_id": scene_id_before}},
                {"$project": {
                    "was_purchased": {
                        "$arrayElemAt": ["$was_purchased", index_to_update]
                    }
                }},
                {"$addFields": {
                    "was_purchased.id": updated_unit_id
                }},
                {"$replaceRoot": {
                    "newRoot": "$was_purchased"
                }}
            ]).next()

            if not payload_with_old_data:
                return {"success": False, "message": "Scene ID or index not found!", "code": 404}

            collection.update_one(
                hasExist,
                {"$pull": {"was_purchased": {"id": unit_id}}}
            )

            collection.update_one(
                {"scene_id": scene_id_after},
                {"$push": {"was_purchased": payload_with_old_data}}
            )
        else:
            collection.update_one(
                hasExist,
                {"$set": {f"was_purchased.{index_to_update}.id": updated_unit_id}}
            )

        return {"success": True, "message": "Successfully update unit purchased", "code": 200}

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

        return {"success": True, "message": "Successfully delete unit purchased", "code": 200}
