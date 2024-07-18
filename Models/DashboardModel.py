from Models.main import ModelMain


class DashboardModel(ModelMain):
    def __init__(self):
        super().__init__()
        self.collection = self.mongo_client[self.main_db_name][self.col_2_name]
        self.__setup__()

    def get_data_dashboard(self):
        collection = self.collection

        struct = {
            "total_machine": 0,
            "total_machine_used": 0,
            "latest_machine_used": {
                "name": "-",
                "date": "-"
            },
            "latest_machine_buy": {
                "name": "-",
                "date": "-"
            }
        }

        if collection.count_documents({}) < 1:
            return {"success": True, "data": struct, "code": 200}

        sum_pipeline = [
            {
                "$group": {
                    "_id": None,
                    "totalSum": {"$sum": "$total_used"}
                }
            }
        ]

        search_latest_used_pipeline = [
            {"$unwind": "$was_purchased"},
            {"$match": {"was_purchased.last_used": {"$ne": None}}},
            {"$sort": {"was_purchased.last_used": -1}},
            {"$limit": 1},
            {"$project": {
                "machine_name": 1,
                "last_used": "$was_purchased.last_used"
            }}
        ]

        search_latest_buy_pipeline = [
            {"$unwind": "$was_purchased"},
            {"$sort": {"was_purchased.buy_at": -1}},
            {"$limit": 1},
            {"$project": {"machine_name": 1, "buy_at": "$was_purchased.buy_at"}}
        ]

        machine_total = collection.count_documents({})
        total_machine_used = list(collection.aggregate(sum_pipeline))
        last_machine_used = list(collection.aggregate(search_latest_used_pipeline))
        last_machine_buy = list(collection.aggregate(search_latest_buy_pipeline))

        last_machine_used_struct = {
            "name": "-",
            "date": "-"
        }

        if last_machine_used:
            last_machine_used_struct['name'] = last_machine_used[0].get('machine_name', '-')
            last_machine_used_struct['date'] = last_machine_used[0].get('last_used', '-')

        last_machine_buy_struct = {
            "name": "-",
            "date": "-"
        }

        if last_machine_buy:
            last_machine_buy_struct['name'] = last_machine_buy[0].get('machine_name', '-')
            last_machine_buy_struct['date'] = last_machine_buy[0]['buy_at']

        struct['total_machine'] = machine_total
        struct['total_machine_used'] = total_machine_used[0]['totalSum']
        struct['latest_machine_used'] = last_machine_used_struct
        struct['latest_machine_buy'] = last_machine_buy_struct

        return {"success": True, "data": struct, "code": 200}