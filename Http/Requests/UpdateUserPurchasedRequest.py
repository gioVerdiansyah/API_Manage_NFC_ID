from marshmallow import Schema, fields


class UpdateUserPurchasedRequest(Schema):
    scene_id_before = fields.String(required=True)
    scene_id_after = fields.String(required=True)
    unit_id = fields.String(required=True)
    updated_unit_id = fields.String(required=True)
