from flask import Flask, jsonify, request
import time, os
from gevent import pywsgi

app = Flask(__name__)

storage = {}

def unique_id():
    return hex(time.time_ns())[2:]

@app.route('/')
def index():
    return "Status --> OK"

@app.route('/u/<user>/<room_id>/post/<data>')
def post_data(user, room_id, data):
    if user not in storage:
        storage[user] = {}

    if room_id not in storage[user]:
        storage[user][room_id] = {}

    uid = unique_id()[:8]
    storage[user][room_id][uid] = {
        "data": data,
        "time": time.strftime('%Y-%m-%d %H:%M:%S')
    }

    return jsonify({"status": "saved", "user": user, "room": room_id, "id": uid})

@app.route('/u/<user>/<room_id>/get')
def get_data(user, room_id):
    return jsonify(storage.get(user, {}).get(room_id, {}))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    server = pywsgi.WSGIServer(('0.0.0.0', port), app)
    server.serve_forever()
