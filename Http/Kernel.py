from flask import Blueprint
from Http.Middleware.VerifyAPIKey import require_api_key

from Core.FlaskAPI import app

need_key_blueprint = Blueprint("app", __name__)



@need_key_blueprint.before_request
@require_api_key
def check_api_key():
    pass


# Registration Middleware
def __init_register_middleware__():
    app.register_blueprint(need_key_blueprint, url_prefix='/')
