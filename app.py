import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

KV_URL = os.environ.get("KV_URL")  # Get the KV URL from environment variables

if not KV_URL:  # Handle the case where KV_URL is not set
    print("Error: KV_URL environment variable is not set!")
    exit(1)  # Exit the application if KV_URL is not set

@app.route('/api')
def api():
    names = request.args.getlist('name')
    results = {}

    if not names:
        return jsonify({"error": "No names provided"}), 400

    for name in names:
        try:
            response = requests.get(f"{KV_URL}/{name}")  # Make a GET request to KV
            response.raise_for_status()  # Check for HTTP errors (4xx or 5xx)
            data = response.json()
            mark = data.get("value")  # Extract the value from the JSON response

            if mark:
                try:
                    mark = int(mark)
                    results[name] = mark
                except ValueError:
                    results[name] = f"Invalid mark for {name} (not an integer)"
            else:
                results[name] = "Name not found"

        except requests.exceptions.RequestException as e:
            results[name] = f"Error retrieving mark for {name}: {e}"

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)