import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

JSON_FILE = "q-vercel-python.json"

@app.route('/api')
def api():
    names = request.args.getlist('name')
    marks = []  # Initialize an empty list to store the marks

    if not names:
        return jsonify({"error": "No names provided"}), 400

    try:
        # Load JSON data from the file
        with open(JSON_FILE, 'r') as f:
            students_data = json.load(f)

        for name in names:
            student_found = False
            # Iterate over each student record in the JSON array
            for student in students_data:
                if student.get("name") == name:
                    marks.append(student.get("marks"))
                    student_found = True
                    break
            if not student_found:
                marks.append("Name not found")
    except Exception as e:
        return jsonify({"error": f"Error: {e}"}), 500

    return jsonify({"marks": marks})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
