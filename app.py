from flask import Flask, jsonify, request, Response
import time, threading, os
from gevent import pywsgi
from ping3 import ping

app = Flask(__name__)

storage, creds, tokens, ping_log = {}, {}, {}, []

site = os.environ.get("Web")

print(site)

interval = 5  # seconds

def unique_id():
    return hex(time.time_ns())[2:]  # fast unique hex ID

def auto_ping():
    while True:
        latency = ping(site)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        ping_log.append({
            "site": site,
            "latency_ms": None if latency is None else round(latency * 1000, 2),
            "time": timestamp
        })
        print("pinging", site)
        time.sleep(interval)

@app.route('/')
def index():
    return "Status --> OK"

@app.route('/register/', methods=['GET'])
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
    return Response(
        jsonify({"status": "registered", "user": user, "token": token}).data,
        mimetype="application/json"
    )

@app.route('/u/<token>/post/<data>', methods=['GET', 'POST'])
def post_data(token, data):
    if token not in tokens:
        return jsonify({"error": "invalid token"})
    user_id = tokens[token]
    uid = unique_id()[:8]
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    storage[user_id][uid] = {"data": data, "time": timestamp}
    return jsonify({
        "status": "saved",
        "user": user_id,
        "unique_id": uid,
        "data": data,
        "time": timestamp
    })

@app.route('/u/<token>/get', methods=['GET'])
def get_data(token):
    if token not in tokens:
        return jsonify({"error": "invalid token"})
    user_id = tokens[token]
    return jsonify(storage.get(user_id, {}))


if __name__ == '__main__':
    threading.Thread(target=auto_ping, daemon=True).start()
    server = pywsgi.WSGIServer(('0.0.0.0', 10000), app)
    print("Running on port 10000...")
    server.serve_forever()
