import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE_FILE = "students.db"

@app.route('/api')
def api():
    names = request.args.getlist('name')
    marks = []  # Initialize an empty list to store the marks

    if not names:
        return jsonify({"error": "No names provided"}), 400

    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        for name in names:
            cursor.execute("SELECT mark FROM students WHERE name=?", (name,))
            result = cursor.fetchone()
            if result:
                marks.append(result[0])  # Append the mark to the list
            else:
                marks.append("Name not found")  # Append "Name not found" to the list
        conn.close()
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500

    return jsonify({"marks": marks})  # Return the list of marks in the "marks" key

if __name__ == '__main__':
    app.run(debug=True, port=5000)
