from Core.FlaskAPI import app, Api

from Http.Controllers.Admin.Auth.LoginController import Login
from Http.Controllers.Admin.Auth.LogoutController import Logout
from Http.Controllers.Admin.NfcController import NfcController, NfcSearchController
from Http.Controllers.Admin.DashboardController import DashboardController
from Http.Controllers.Unity.NfcScanController import NfcScanController
from Http.Controllers.Unity.NfcLogoutController import NfcLogoutController
from Http.Controllers.TestController import TestController
from Http.Exceptions.ExceptionAPIList import errors

# Middleware prefix names
lk = 'lock'
laa = "lock_admin_auth"

# Routes
def __init_api__():
    # Admin
    admin_api = Api(app, prefix="/api/admin", errors=errors)
    admin_api.add_resource(TestController, '/test')
    admin_api.add_resource(Login, '/login', endpoint=f'{lk}.login')
    # Admin Auth
    admin_api.add_resource(DashboardController, '/dashboard', endpoint=f"{laa}.dashboard")
    admin_api.add_resource(Logout, '/logout', endpoint=f'{laa}.logout')
    admin_api.add_resource(NfcController, '/nfc', endpoint=f'{laa}.nfc')
    admin_api.add_resource(NfcSearchController, '/nfc/search/<string:query>', endpoint=f'{laa}.nfc.search')

    # Unity
    unity_api = Api(app, prefix="/api/unity", errors=errors)
    unity_api.add_resource(NfcScanController, "/nfc/check", endpoint=f'{lk}.scan')
    unity_api.add_resource(NfcLogoutController, "/nfc/logout", endpoint=f'{lk}.logout')