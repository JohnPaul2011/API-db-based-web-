from flask import Flask, jsonify
import uuid, time, threading, os
from gevent import pywsgi
from ping3 import ping

app = Flask(__name__)

storage = {}

site = os.environ.get("API_KEY", "0.0.0.0")
interval = 5  # seconds

def auto_ping():
    while True:
        latency = ping(site)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        uid = str(uuid.uuid4())[:8]
        storage.setdefault("ping", {})
        storage["ping"][uid] = {
            "site": site,
            "latency_ms": None if latency is None else round(latency * 1000, 2),
            "time": timestamp
        }
        time.sleep(interval)
        print("pinging")


@app.route('/<user_id>/post/<data>', methods=['GET', 'POST'])
def post_data(user_id, data):
    if user_id not in storage:
        storage[user_id] = {}
    unique_id = str(uuid.uuid4())[:8]
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    storage[user_id][unique_id] = {"data": data, "time": timestamp}
    return jsonify({
        "status": "saved",
        "unique_id": unique_id,
        "data": data,
        "time": timestamp
    })

@app.route('/<user_id>/get/', methods=['GET'])
def get_data(user_id):
    return jsonify(storage.get(user_id, {}))

if __name__ == '__main__':
    threading.Thread(target=auto_ping, daemon=True).start()
    server = pywsgi.WSGIServer(('0.0.0.0', 10000), app)
    print("Running on port 10000...")
    server.serve_forever()
