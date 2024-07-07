from flask import Blueprint
from Http.Middleware.VerifyAPIKey import require_api_key
from Http.Middleware.AdminAuth import require_token
from Core.FlaskAPI import app

need_key_blueprint = Blueprint("lock", __name__)
verify_token = Blueprint("lock_admin_auth", __name__)


@need_key_blueprint.before_request
@require_api_key
def check_api_key():
    pass


@verify_token.before_request
@require_token
def check_token():
    pass


# Registration Middleware
def __init_register_middleware__():
    app.register_blueprint(need_key_blueprint)
    app.register_blueprint(verify_token)
