from Core.FlaskAPI import app, Api

from Http.Controllers import AuthController
from Http.Controllers import NfcController

# Middleware prefix names
lk = 'lock'
laa = "lock_admin_auth"

# Routes
def __init_api__():
    # Admin
    admin_api = Api(app, prefix="/api/admin")
    admin_api.add_resource(AuthController.Login, '/login', endpoint=f'{lk}.login')
    # Admin Auth
    admin_api.add_resource(AuthController.Logout, '/logout', endpoint=f'{laa}.logout')
    admin_api.add_resource(NfcController.ShowAllData, '/nfc', endpoint=f'{laa}.nfc')
    admin_api.add_resource(NfcController.AddNFCData, '/nfc/store', endpoint=f'{laa}.nfc.store')
    admin_api.add_resource(NfcController.UpdateNFCData, '/nfc/update/<string:id>', endpoint=f'{laa}.nfc.update')
    admin_api.add_resource(NfcController.DeleteNFCData, '/nfc/delete/<string:id>', endpoint=f'{laa}.nfc.delete')
