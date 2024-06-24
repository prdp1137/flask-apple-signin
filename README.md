# Flask Apple Login

A Flask extension for integrating Apple OAuth login seamlessly into your Flask applications.

## Overview

**Flask Apple Login** is a simple and easy-to-use Flask extension that enables Apple OAuth login for your Flask applications. This extension handles the OAuth flow, token retrieval, and user authentication using Apple's secure authentication system.

## Features

- Easy integration with Flask applications
- Secure OAuth flow with Apple
- Configurable settings for client ID, team ID, key ID, and private key file
- Automatically handles the token retrieval process

## Installation

Install Flask Apple Login using pip:

```bash
pip install flask-apple-login
```

## Usage
### Quick Start
**1. Initialize your Flask application:**
```python
from flask import Flask, jsonify, request, session, redirect, url_for
from flask_login_apple import AppleLogin

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SECRET_KEY'] = 'your-secret-key'
app.config['APPLE_CLIENT_ID'] = 'your-client-id'
app.config['APPLE_TEAM_ID'] = 'your-team-id'
app.config['APPLE_KEY_ID'] = 'your-key-id'
app.config['APPLE_PRIVATE_KEY_FILE'] = '/path/to/your/private_key.pem'

apple_login = AppleLogin(app)

@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})

@app.route('/login')
def login():
    return apple_login.authorize()

@app.route('/callback', methods=['GET', 'POST'])
def callback():
    token = apple_login.callback()
    return f'Logged in with token: {token}'
```

**2. Run your Flask application:**
```bash
flask run
```

## Configuration
Add the following configuration variables to your Flask app:

- **APPLE_CLIENT_ID**: Your Apple client ID.
- **APPLE_TEAM_ID**: Your Apple team ID.
- **APPLE_KEY_ID**: Your Apple key ID.
- **APPLE_PRIVATE_KEY_FILE**: Path to your private key file.
