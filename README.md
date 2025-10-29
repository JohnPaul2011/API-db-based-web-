
# 🌐 DataPulse — Mini API Database

DataPulse is a lightweight API-based data storage service.
Post, fetch, and timestamp your data — instantly ⚡


## 🚀 Features

* 🗂️ Store data per user ID

* ⏰ Automatic timestamps

* 🔍 Retrieve all stored entries

* ⚙️ Fast, memory-only, no database needed

* ☁️ Render-ready with Gevent


## 🧩 API Endpoints

*  Add Data
```
website.com/<id>/post/<data>
```
Example
```
website.com/123/post/HelloWorld
```
Response
```
{
  "status": "saved",
  "unique_id": "a1b2c3d4",
  "data": "HelloWorld",
  "time": "2025-10-27 20:30:00"
}
```

---

* 📦 Get Data
```Ruby
website.com/<id>/get/
```
Example
```Ruby
website.com/123/get/
```
Response
```Ruby
{
  "a1b2c3d4": {
    "data": "HelloWorld",
    "time": "2025-10-27 20:30:00"
  }
}
```
---

### 🧰 Local Setup

Install dependencies
```
pip install flask gevent
```
### Run locally
```
python app.py
```

## ☁️ Render Deployment Ready

connect our or your modified code to Render 🚀

# 💡 Why DataPulse?

A micro “API database” for developers who need
a quick place to drop and fetch data — without any real database setup.


---
