from marshmallow import Schema, fields


class StoreSceneRequest(Schema):
    scene_id = fields.String(required=True)
    machine_name = fields.String(required=True)
    is_used = fields.Boolean(required=False, default=False)
