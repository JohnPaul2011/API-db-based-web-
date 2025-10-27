from flask import Flask, jsonify
import uuid, time
from gevent import pywsgi

app = Flask(__name__)

storage = {}

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
    server = pywsgi.WSGIServer(('0.0.0.0', 10000), app)
    print("Running on port 10000...")
    server.serve_forever()
