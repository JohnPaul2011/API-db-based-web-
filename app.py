from flask import Flask, jsonify, request
import time, os
from gevent import pywsgi

app = Flask(__name__)

storage, creds, tokens = {}, {}, {}
base_url = os.environ.get("Web")

def unique_id():
    return hex(time.time_ns())[2:]

@app.route('/')
def index():
    return "Status --> OK"

@app.route('/register/')
def register_user():
    user = request.args.get('user')
    password = request.args.get('password')
    if not user or not password:
        return jsonify({"error": "missing user or password"})
    if user in creds:
        return jsonify({"status": "user exists"})
    creds[user] = password
    token = unique_id()[:12]
    tokens[token] = user
    storage[user] = {}
    return jsonify({"status": "registered", "user": user, "token": token})

@app.route('/u/<token>/<room_id>/post/<data>')
def post_data(token, room_id, data):
    if token not in tokens:
        return jsonify({"error": "invalid token"})
    user = tokens[token]
    if room_id not in storage[user]:
        storage[user][room_id] = {}
    uid = unique_id()[:8]
    storage[user][room_id][uid] = {"data": data, "time": time.strftime('%Y-%m-%d %H:%M:%S')}
    return jsonify({"status": "saved", "user": user, "room": room_id, "id": uid})

@app.route('/u/<token>/<room_id>/get')
def get_data(token, room_id):
    if token not in tokens:
        return jsonify({"error": "invalid token"})
    user = tokens[token]
    return jsonify(storage[user].get(room_id, {}))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    server = pywsgi.WSGIServer(('0.0.0.0', port), app)
    server.serve_forever()
