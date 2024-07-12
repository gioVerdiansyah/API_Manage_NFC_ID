from Core.FlaskAPI import app, Api

from Http.Controllers.Admin.Auth.LoginController import Login
from Http.Controllers.Admin.Auth.LogoutController import Logout
from Http.Controllers.Admin.SceneController import SceneController, SceneSearchController
from Http.Controllers.Admin.UnitsPurchasedController import UnitsPurchasedController, UnitSearchController
from Http.Controllers.Admin.DashboardController import DashboardController
from Http.Controllers.Unity.SceneScanController import SceneScanController
from Http.Controllers.Unity.SceneLogoutController import SceneLogoutController
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
    admin_api.add_resource(SceneController, '/scene', endpoint=f'{laa}.scene')
    admin_api.add_resource(UnitsPurchasedController, '/units', endpoint=f'{laa}.unit')
    admin_api.add_resource(UnitSearchController, '/units/search/<string:query>', endpoint=f'{laa}.unit.search')
    admin_api.add_resource(SceneSearchController, '/scene/search/<string:query>', endpoint=f'{laa}.scene.search')

    # Unity
    unity_api = Api(app, prefix="/api/unity", errors=errors)
    unity_api.add_resource(SceneScanController, "/scene/check", endpoint=f'{lk}.scan')
    unity_api.add_resource(SceneLogoutController, "/scene/logout", endpoint=f'{lk}.logout')