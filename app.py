from flask import Flask, jsonify, request

app = Flask(__name__)

app.config['DEBUG'] = True

@app.route('/')
def index():
    return jsonify({'message': 'Hello World!'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=1137, debug=True)