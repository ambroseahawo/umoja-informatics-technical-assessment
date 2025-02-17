from flask import Blueprint, jsonify
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import HTTPException

error_blueprint = Blueprint("error_handlers", __name__)


@error_blueprint.app_errorhandler(ValidationError)
def handle_marshmallow_validation_error(error):
    """Handles Marshmallow validation errors and returns JSON response."""
    response = {
        "error": "Validation Error",
        "message": error.messages,
        "status_code": 400,
    }
    return jsonify(response), 400


@error_blueprint.app_errorhandler(HTTPException)
def handle_http_exception(error):
    """Handles standard HTTP exceptions."""
    response = {
        "error": error.name,
        "message": error.description,
        "status_code": error.code,
    }
    return jsonify(response), error.code


@error_blueprint.app_errorhandler(Exception)
def handle_unexpected_error(error):
    """Handles unexpected server errors."""
    response = {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred. Please try again later.",
        "status_code": 500,
    }
    return jsonify(response), 500
