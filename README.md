
---

🌐 DataPulse — Mini API Database

DataPulse is a lightweight API-based data storage service.
Post, fetch, and timestamp your data — instantly ⚡


---

🚀 Features

🗂️ Store data per user ID

⏰ Automatic timestamps

🔍 Retrieve all stored entries

⚙️ Fast, memory-only, no database needed

☁️ Render-ready with Gevent



---

🧩 API Endpoints

➕ Add Data

GET /<id>/post/<data>

Example

/123/post/HelloWorld

Response

{
  "status": "saved",
  "unique_id": "a1b2c3d4",
  "data": "HelloWorld",
  "time": "2025-10-27 20:30:00"
}


---

📦 Get Data

GET /<id>/get/

Example

/123/get/

Response

{
  "a1b2c3d4": {
    "data": "HelloWorld",
    "time": "2025-10-27 20:30:00"
  }
}


---

🧰 Local Setup

Install dependencies

pip install flask gevent

Run locally

python app.py


---

☁️ Render Deployment

Procfile

web: python app.py

requirements.txt

flask
gevent

Then push to GitHub and connect to Render 🚀


---

💡 Why DataPulse?

A micro “API database” for developers who need
a quick place to drop and fetch data — without any real database setup.


---
