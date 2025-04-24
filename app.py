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
################ A. Create a Health Program ##############################
@app.route('/create_program', methods=['POST'])
def create_program():
    data = request.get_json()
    programs = read_json(PROGRAMS_FILE)
    programs.append(data)
    write_json(programs, PROGRAMS_FILE)
    return jsonify({"message": "Program created!"})
################# B. Register a Client ################################
@app.route('/register_client', methods=['POST'])
def register_client():
    client_data = request.get_json()
    clients = read_json(CLIENTS_FILE)
    clients.append(client_data)
    write_json(clients, CLIENTS_FILE)
    return jsonify({"message": "Client registered!"})

################# C. Search for a Client ################################
@app.route('/search_client/<name>')
def search_client(name):
    clients = read_json(CLIENTS_FILE)
    for client in clients:
        if client['name'].lower() == name.lower():
            return jsonify(client)
    return jsonify({"message": "Client not found"})