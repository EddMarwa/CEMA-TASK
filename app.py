from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import re
import os

# Flask App Initializing
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#  Database and Login Manager
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

#------------------- Database Models -------------------#
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

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

#------------------- Authentication Routes -------------------#
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        

        if user and check_password_hash (user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Password validation rules
        if len(password) < 8:
            flash("Password must be at least 8 characters long.")
            return redirect(url_for('signup'))
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            flash("Password must contain at least one special character.")
            return redirect(url_for('signup'))
        if not re.search(r"\d", password):
            flash("Password must contain at least one number.")
            return redirect(url_for('signup'))

        # Check for existing username before Auth
        if User.query.filter_by(username=username).first():
            flash("Username already exists.")
            return redirect(url_for('signup'))

        # Hashing passwords before storage in db
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please log in.")
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
#------------------- Protected Routes -------------------#
@app.route('/home')
@login_required
def home():
    clients = Client.query.all() 
    return render_template('home.html', clients=clients)

@app.route('/search')
@login_required
def search():
    return render_template('search.html')
#------------------- Health Program & Client Routes -------------------#
@app.route('/create_program', methods=['POST'])
@login_required
def create_program():
    program_name = request.form.get('name')
    
    # Checks if program already exists
    if HealthProgram.query.filter_by(name=program_name).first():
        return jsonify({"error": "Program already exists!"}), 400
    
    # Adds to database
    new_program = HealthProgram(name=program_name)
    db.session.add(new_program)
    db.session.commit()
    
    return jsonify({"message": f"Program '{program_name}' created!"})

@app.route('/register_client', methods=['POST'])
@login_required
def register_client():
    client_name = request.form.get('name')
    
    # Create new client
    new_client = Client(name=client_name)
    db.session.add(new_client)
    db.session.commit()
    
    return jsonify({"message": f"Client '{client_name}' registered!"})

@app.route('/enroll_client', methods=['POST'])
@login_required
def enroll_client():
    client_id = request.form.get('client_id')
    program_id = request.form.get('program_id')
    
    client = Client.query.get(client_id)
    program = HealthProgram.query.get(program_id)
    
    if not client or not program:
        return jsonify({"error": "Client or Program not found!"}), 404
    
    # Add program to client's enrollment
    client.programs.append(program)
    db.session.commit()
    
    return jsonify({"message": f"Client enrolled in {program.name}!"})

@app.route('/search_client/<name>')
@login_required
def search_client(name):
    client = Client.query.filter_by(name=name).first()
    if client:
        # Get enrolled programs
        programs = [program.name for program in client.programs]
        return jsonify({
            "name": client.name,
            "programs": programs
        })
    return jsonify({"message": "Client not found"}), 404

@app.route('/clients')
@login_required
def list_clients():
    clients = Client.query.all()
    return jsonify([{"id": c.id, "name": c.name} for c in clients])

@app.route('/programs')
@login_required
def list_programs():
    programs = HealthProgram.query.all()
    return jsonify([{"id": p.id, "name": p.name} for p in programs])

# Client Profile Route
@app.route('/client_profile/<int:client_id>')
@login_required
def client_profile(client_id):
    client = Client.query.get_or_404(client_id)
    programs = HealthProgram.query.all()
    return render_template('client_profile.html', client=client, all_programs=programs)

# AJAX: Search Clients
@app.route('/search_clients_ajax')
@login_required
def search_clients_ajax():
    query = request.args.get('q')
    clients = Client.query.filter(Client.name.ilike(f'%{query}%')).all()
    return jsonify([{'id': c.id, 'name': c.name} for c in clients])

# AJAX: Enroll Client
@app.route('/enroll_client_ajax', methods=['POST'])
@login_required
def enroll_client_ajax():
    data = request.get_json()
    client = Client.query.get(data['client_id'])
    program = HealthProgram.query.get(data['program_id'])
    
    if not client or not program:
        return jsonify({'success': False, 'error': 'Invalid client/program'})
    
    client.programs.append(program)
    db.session.commit()
    return jsonify({'success': True})

# Delete Route
@app.route('/delete_client/<int:client_id>', methods=['DELETE'])
@login_required
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/delete_program/<int:program_id>', methods=['DELETE'])
@login_required
def delete_program(program_id):
    program = HealthProgram.query.get_or_404(program_id)
    db.session.delete(program)
    db.session.commit()
    return jsonify({'success': True})



#------------------- Database  Initializing -------------------#
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)