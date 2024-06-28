from Core.FlaskAPI import api

from Http.Controllers import AuthController


# Routes
def __init_api__():
    api.add_resource(AuthController.Login, '/login', endpoint='app.login')
