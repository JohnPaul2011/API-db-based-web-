from flask import Flask, jsonify, request, Response
import time, threading, os, requests
from gevent import pywsgi

app = Flask(__name__)

storage, creds, tokens, ping_log = {}, {}, {}, []

site = os.environ.get("Web", "https://your-app.onrender.com")
interval = 5

def unique_id():
    return hex(time.time_ns())[2:]

def auto_ping():
    while True:
        try:
            start = time.time()
            r = requests.get(site, timeout=3)
            latency = (time.time() - start) * 1000
            print("pinging", site, "->", round(latency, 2), "ms")
            ping_log.append({
                "site": site,
                "status": r.status_code,
                "latency_ms": round(latency, 2),
                "time": time.strftime('%Y-%m-%d %H:%M:%S')
            })
        except Exception as e:
            ping_log.append({
                "site": site,
                "error": str(e),
                "time": time.strftime('%Y-%m-%d %H:%M:%S')
            })
        time.sleep(interval)

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

@app.route('/u/<token>/post/<data>')
def post_data(token, data):
    if token not in tokens:
        return jsonify({"error": "invalid token"})
    user = tokens[token]
    uid = unique_id()[:8]
    storage[user][uid] = {"data": data, "time": time.strftime('%Y-%m-%d %H:%M:%S')}
    return jsonify({"status": "saved", "user": user, "unique_id": uid, "data": data})

@app.route('/u/<token>/get')
def get_data(token):
    if token not in tokens:
        return jsonify({"error": "invalid token"})
    user = tokens[token]
    return jsonify(storage.get(user, {}))

@app.route('/pinglog')
def get_ping_log():
    return jsonify(ping_log[-20:])

if __name__ == '__main__':
    threading.Thread(target=auto_ping, daemon=True).start()
    server = pywsgi.WSGIServer(('0.0.0.0', 10000), app)
    print("Running on port 10000...")
    server.serve_forever()
