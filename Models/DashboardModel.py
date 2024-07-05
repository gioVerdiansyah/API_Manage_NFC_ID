from Models.main import ModelMain


class DashboardModel(ModelMain):
    def __init__(self):
        super().__init__()
        self.collection = self.mongo_client[self.main_db_name][self.col_2_name]
        self.__setup__()

    def get_data_dashboard(self):
        collection = self.collection

        sum_pipeline = [
            {
                "$group": {
                    "_id": None,
                    "totalSum": {"$sum": "$total_used"}
                }
            }
        ]

        search_latest_date_pipeline = [
            {"$match": {"latest_used": {"$ne": None}}},
            {"$sort": {"latest_used": -1}},
            {"$limit": 1},
            {"$project": {"machine_name": 1, "latest_used": 1}}
        ]

        machine_total = collection.count_documents({})
        total_machine_used = list(collection.aggregate(sum_pipeline))
        last_machine_used = list(collection.aggregate(search_latest_date_pipeline))

        last_machine_used_struct = {
            "name": "-",
            "date": "-"
        }

        if last_machine_used:
            last_machine_used_struct['name'] = last_machine_used[0].get('machine_name', '-')
            last_machine_used_struct['date'] = last_machine_used[0].get('latest_used', '-')

        struct = {
            "total_machine": machine_total,
            "total_machine_used": total_machine_used[0]['totalSum'],
            "last_machine_used": last_machine_used_struct
        }

        return {"success": True, "data": struct, "code": 200}