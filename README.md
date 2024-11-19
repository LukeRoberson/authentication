# Central Authentication Service (CAS)

## Overview

A web based micro-service that manages authentication with the Azure iDP. This is intended to be run as a container that other services can access.

A user can authenticate against an application in Azure, and be presented with a JWT (Java Web Token). This token can be passed as a 'Bearer' token for API requests. The API service can then verify that this token is valid.

## Configuration

The service will only start if there is a correctly formatted 'config.yaml' file.

This need to be formatted in this way:

```
web:
  debug: true
  ip: 0.0.0.0
  port: '5020'
azure:
  app-id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
  app-secret: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  redirect-uri: /getAToken
  tenant-id: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
  admin-group: Network Admins
  helpdesk-group: HelpDesk Team
```

This defines how the web service runs, and how to connect to Azure.

## Authentication

The user goes to '/auth/login' to start the logon process. This generates a URL, returned in a JSON format, that the user can go to to begin authentication.

This may be transparent if the user is already logged into their Azure account, or may present the Azure login screen.

Azure will access the callback URL, as defined in the config file. It will present an authentication code. If authentication is successful, the token is extracted, and presented to the user.

# API Tokens

A decorator called 'token_required' can be added to API URLs. This requires that a Bearer Token is included to authenticate the request.

This will check that the request has a token, and that the token is valid.

# General Usage

1. Send a GET to /auth/login
    This returns a URL
2. Copy the URL, and add it to a web browser
    This will complete authentication and return a token
3. Send a GET to /auth/test
    Include the 'Authorization' header with the bearer
    This will return login information
