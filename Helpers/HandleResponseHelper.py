from flask import jsonify, make_response


def response(message="Successfully get", data=None, isSuccess=True, statusCode=200):
    if data is None:
        data = {}

    response_payload = {
        "meta": {
            "message": message,
            "isSuccess": isSuccess,
            "statusCode": statusCode
        },
        "data": data
    }

    response = make_response(jsonify(response_payload), statusCode)

    return response
