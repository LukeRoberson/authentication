"""
Central Authentication Service
    Micro-service to interact with Azure Active Directory.

Relies on the existance and correct formatting of config.yaml
    If this does not exist or is invalid, the web application will not start.
    This contains enough information to start the web application.
    More data is then read from an SQL database.
"""

from flask import Flask, jsonify, request
import os

from config_parse import config
from azure import azure_bp
from jwt_manager import token_required, validate_token


# Check config is valid
if config.config_valid is False or config.config_exists is False:
    print('Config file is invalid. Exiting...')
    exit(1)

# Initialise Flask
app = Flask(__name__)
app.secret_key = os.getenv('api_master_pw')
app.register_blueprint(azure_bp)


# A test route to check if authentication is working
@app.route('/auth/test')
@token_required
def auth_test(decoded_token=None):
    return jsonify(
        {
            "result": "success",
            "details": decoded_token
        }
    ), 200


# Token validation route for external services
@app.route('/auth/validate', methods=['POST'])
def auth_validate():
    token = request.json.get('token')
    if not token:
        return jsonify(
            {
                "result": "failure",
                "message": "Token is missing"
            }
        ), 401

    result = validate_token(token)
    if 'error' in result:
        return jsonify(
            {
                "result": "failure",
                "message": "Token is invalid",
                "details": result['error']
            }
        ), 401

    return jsonify(
        {
            "result": "success",
            "details": result
        }
    ), 200


if __name__ == '__main__':
    app.run(
        host=config.web_ip,
        port=config.web_port,
        debug=config.web_debug
    )
