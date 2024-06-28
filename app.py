import os
from dotenv import load_dotenv
from Core.FlaskAPI import app
from Http.Routes.api import __init_api__
from Http.Kernel import __init_register_middleware__
from Models.main import ModelMain

load_dotenv()

__init_api__()
__init_register_middleware__()
model_setup = ModelMain()
model_setup.__setup__()

if __name__ == "__main__":
    host = os.getenv("APP_HOST")
    port = os.getenv("APP_PORT")
    app.run(debug=True, host=host, port=port)