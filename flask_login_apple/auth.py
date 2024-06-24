import requests
import jwt
import time
from flask import current_app, url_for, redirect, request
import secrets

class AppleLogin:
    def __init__(self, app=None):
        self.client_id = None
        self.team_id = None
        self.key_id = None
        self.private_key_file = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.client_id = app.config.get('APPLE_CLIENT_ID')
        self.team_id = app.config.get('APPLE_TEAM_ID')
        self.key_id = app.config.get('APPLE_KEY_ID')
        self.private_key_file = app.config.get('APPLE_PRIVATE_KEY_FILE')

        if not all([self.client_id, self.team_id, self.key_id, self.private_key_file]):
            raise ValueError("All Apple OAuth configuration variables must be set.")

        app.add_url_rule('/login', 'apple_login_authorize', self.authorize)
        app.add_url_rule('/callback', 'apple_login_callback', self.callback)

    def authorize(self):
        with current_app.app_context():
            redirect_uri = url_for('apple_login_callback', _external=True)
            # Apple requires HTTPS for the redirect URI with TLS 1.2, hence the following line
            redirect_uri = redirect_uri.replace('http://', 'https://')
            url = (
                'https://appleid.apple.com/auth/authorize?'
                f'response_type=code&client_id={self.client_id}&'
                f'response_mode=form_post&state={secrets.token_urlsafe(16)}&'
                f'redirect_uri={redirect_uri}&scope=name email'
            )
            return redirect(url)

    def callback(self):
        code = request.form.get('code')
        state = request.form.get('state')
        if not code or not state:
            return "Error: Missing code or state"

        token_response = self.get_token(code)

        if 'error' in token_response:
            return f"Error in token response: {token_response['error']}"

        return token_response

    def get_token(self, code):
        with current_app.app_context():
            redirect_uri = url_for('apple_login_callback', _external=True)
            # Apple requires HTTPS for the redirect URI with TLS 1.2, hence the following line
            redirect_uri = redirect_uri.replace('http://', 'https://')
            url = 'https://appleid.apple.com/auth/token'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret(),
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': redirect_uri,
            }
            response = requests.post(url, headers=headers, data=data)
            return response.json()

    def client_secret(self):
        headers = {
            'alg': 'ES256',
            'kid': self.key_id
        }

        payload = {
            'iss': self.team_id,
            'iat': int(time.time()),
            'exp': int(time.time()) + 3600,
            'aud': 'https://appleid.apple.com',
            'sub': self.client_id,
        }

        with open(self.private_key_file, 'r') as f:
            private_key = f.read()

        client_secret = jwt.encode(
            payload,
            private_key,
            algorithm='ES256',
            headers=headers
        )

        return client_secret
