"""
Central Authentication Service
    Micro-service to interact with Azure Active Directory.

Relies on the existance and correct formatting of config.yaml
    If this does not exist or is invalid, the web application will not start.
    This contains enough information to start the web application.
    More data is then read from an SQL database.
"""

from flask import Flask
import os

from config_parse import config
from azure import azure_bp


# Check config is valid
if config.config_valid is False or config.config_exists is False:
    print('Config file is invalid. Exiting...')
    exit(1)

# Initialise Flask
app = Flask(__name__)
app.secret_key = os.getenv('api_master_pw')
app.register_blueprint(azure_bp)


if __name__ == '__main__':
    app.run(
        host=config.web_ip,
        port=config.web_port,
        debug=config.web_debug
    )
