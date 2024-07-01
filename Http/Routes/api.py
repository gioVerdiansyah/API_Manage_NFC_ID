from Core.FlaskAPI import api

from Http.Controllers import AuthController
from Http.Controllers import NfcController


# Routes
def __init_api__():
    api.add_resource(AuthController.Login, '/login', endpoint='app.login')
    api.add_resource(NfcController.ShowAllData, '/nfc', endpoint='app.nfc')
    api.add_resource(NfcController.AddNFCData, '/nfc/add', endpoint='app.nfc.add')
    api.add_resource(NfcController.UpdateNFCData, '/nfc/update/<string:id>', endpoint='app.nfc.update')
    api.add_resource(NfcController.DeleteNFCData, '/nfc/delete/<string:id>', endpoint='app.nfc.delete')
