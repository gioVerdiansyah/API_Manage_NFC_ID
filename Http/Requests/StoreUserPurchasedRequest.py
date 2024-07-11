from marshmallow import Schema, fields


class StoreUserPurchasedRequest(Schema):
    scene_id = fields.String(required=True)
    unit_id = fields.String(required=True)
