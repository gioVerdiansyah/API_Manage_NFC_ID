from Core.FlaskAPI import api

from Http.Controllers import AuthController
from Http.Controllers import NfcController


# Routes
def __init_api__():
    api.add_resource(AuthController.Login, '/login', endpoint='app.login')
    api.add_resource(NfcController.AddNFCData, '/nfc/add', endpoint='app.nfc.add')
