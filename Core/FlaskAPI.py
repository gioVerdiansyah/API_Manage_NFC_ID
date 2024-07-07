from werkzeug.exceptions import HTTPException
from flask import Flask
from flask_restful import Api
from Helpers.HandleResponseHelper import response
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
api = Api(app, prefix='/api')


@app.errorhandler(HTTPException)
def handle_exception(e):
    return response(message=str(e.name), isSuccess=False, statusCode=e.code, data=str(e.description))
