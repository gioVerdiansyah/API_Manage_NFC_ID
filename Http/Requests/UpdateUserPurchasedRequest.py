from marshmallow import Schema, fields


class UpdateUserPurchasedRequest(Schema):
    scene_id = fields.String(required=True)
    unit_id = fields.String(required=True)
    updated_unit_id = fields.String(required=True)
