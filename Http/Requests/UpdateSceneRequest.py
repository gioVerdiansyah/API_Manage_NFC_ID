from marshmallow import Schema, fields


class UpdateSceneRequest(Schema):
    id = fields.String(required=True)
    scene_id = fields.String(required=True)
    machine_name = fields.String(required=True)
    is_used = fields.Boolean(required=False, default=False)
