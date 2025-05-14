from flask import Flask, request, jsonify
import requests
import base64

app = Flask(__name__)

# بيانات FatSecret
CLIENT_ID = "273df33156734ae4a60a3efbcbb9edde"
CLIENT_SECRET = "c9258b2d8e1c48629c2ae7c97da57985"

# الدالة اللي بتجيب التوكن
def get_access_token():
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_encoded = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_encoded}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    response = requests.post("https://oauth.fatsecret.com/connect/token", headers=headers, data=data)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        return None

# Endpoint: /search-food?query=apple
@app.route("/search-food")
def search_food():
    query = request.args.get("query", "")

    access_token = get_access_token()
    if not access_token:
        return jsonify({"error": "Failed to get access token"}), 500

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    fatsecret_url = "https://platform.fatsecret.com/rest/server.api"
    params = {
        "method": "food.search.v3",
        "search_expression": query,
        "format": "json"
    }

    response = requests.get(fatsecret_url, headers=headers, params=params)

    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
