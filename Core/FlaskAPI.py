from werkzeug.exceptions import HTTPException
from flask import Flask
from flask_restful import Api
from Helpers.HandleResponseHelper import response

app = Flask(__name__)
api = Api(app, prefix='/api')


@app.errorhandler(404)
def not_found(e):
    return response(message="API path is not found", isSuccess=False, statusCode=404)


@app.errorhandler(HTTPException)
def handle_exception(e):
    return response(message=str(e.name), isSuccess=False, statusCode=e.code, data=str(e.description))


@app.errorhandler(405)
def not_allowed(e):
    return response(message="API method is not allowed", isSuccess=False, statusCode=405)
