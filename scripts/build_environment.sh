#!/bin/bash

pip install django

# needed for twisted
pip install oauth
pip install twisted

# clone oauth-proxy twisted plugin
git clone https://github.com/mojodna/oauth-proxy

# needed for oauth_client.py
pip install oauth2
