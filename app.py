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

################# Database setup ################################
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize database
with app.app_context():
    db.create_all()

################# Authentication Routes ################################

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid credentials')
    return render_template('login.html')

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('signup'))
            
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Protected Homepage
@app.route('/home')
@login_required
def home():
    return render_template('home.html')


################# Update Existing Features for Database ################################
class HealthProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    programs = db.relationship('HealthProgram', secondary='client_program')

# Association Table
client_program = db.Table('client_program',
    db.Column('client_id', db.Integer, db.ForeignKey('client.id')),
    db.Column('program_id', db.Integer, db.ForeignKey('health_program.id'))
)
#################  ################################
#################  ################################
#################  ################################
#################  ################################
#################  ################################
#################  ################################
#################  ################################
#################  ################################
#################  ################################
#################  ################################
#################  ################################
#################  ################################
#################  ################################
#################  ################################
#################  ################################
#################  ################################
#################  ################################