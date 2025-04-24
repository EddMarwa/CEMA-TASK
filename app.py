from flask import Flask, jsonify, request, render_template
import json
import os

app = Flask(__name__)

# File paths to this project
CLIENTS_FILE = os.path.join('data', 'clients.json')
PROGRAMS_FILE = os.path.join('data', 'programs.json')

# This function helps to read data
def read_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# This function helps to write data
def write_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Homepage
@app.route('/')
def home():
    return "Health System Home"

if __name__ == '__main__':
    app.run(debug=True)