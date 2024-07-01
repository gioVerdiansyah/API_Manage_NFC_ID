from marshmallow import Schema, fields


class AddNFCRequest(Schema):
    nfc_id = fields.String(required=True)
    machine_name = fields.String(required=True)
    is_used = fields.Boolean(required=False, default=False)
