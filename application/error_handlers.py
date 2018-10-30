from flask import jsonify



def resource_not_found(error):
    """ handles resource not found"""
    response = jsonify({"error": "The requested resource could not be found on this server, check and try again"})
    response.status_code = 404
    return response


def method_not_allowed(error):
    """handle 405 error."""
    response = jsonify({"error": "Method not allowed, ensure you enter the correct method and try again"})
    response.status_code = 405
    return response

def bad_request(error):
    """handles any 400 error."""
    response = jsonify({"error": "Incorrect data input format,bad request"})
    response.status_code = 400
    return response