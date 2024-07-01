from marshmallow import Schema, fields


class NeedIDRequest(Schema):
    id = fields.String(required=True)
