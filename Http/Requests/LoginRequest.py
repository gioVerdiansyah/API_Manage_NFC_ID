from marshmallow import Schema, fields


class LoginRequest(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
