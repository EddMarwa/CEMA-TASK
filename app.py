from flask import Flask, jsonify, request, render_template
import json
import os

app = Flask(__name__)

# File paths
CLIENTS_FILE = os.path.join('data', 'clients.json')
PROGRAMS_FILE = os.path.join('data', 'programs.json')

# Helper function to read data
def read_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Helper function to write data
def write_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Homepage
@app.route('/')
def home():
    return "Health System Home"

if __name__ == '__main__':
    app.run(debug=True)