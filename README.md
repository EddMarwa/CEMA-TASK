# CEMA-TASK
# Health Information System (CEMA-TASK)

A Flask-based web application for managing healthcare clients and programs, featuring user authentication, database integration, and an interactive UI. Designed for doctors/administrators to track patient enrollment in health programs (e.g., TB, Malaria).

![Dashboard Preview](https://via.placeholder.com/800x400.png?text=Health+System+Dashboard)

## Features ✨
- **User Authentication**: Secure signup, login, and logout.
- **Health Program Management**: Create, view, and delete health programs.
- **Client Management**:
  - Register new clients.
  - Enroll clients in programs.
  - Search clients by name (real-time AJAX search).
  - Delete clients.
- **Interactive UI**: Built with Bootstrap for responsive design.
- **Database Integration**: SQLite for data persistence.
- **API Endpoints**: Fetch client profiles and program details.

## Technologies 🛠️
- **Backend**: Python, Flask, Flask-SQLAlchemy, Flask-Login
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript (AJAX)
- **Database**: SQLite (with SQLAlchemy ORM)
- **Security**: Werkzeug password hashing, session management

## Installation 💻

### Prerequisites
- Python 3.9+
- pip package manager

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/EddMarwa/CEMA-TASK.git
   cd CEMA-TASK

## Project Structure

CEMA-TASK/
├── app.py                 # Main application logic
├── instance/
│   └── database.db        # SQLite database
├── templates/             # HTML templates
│   ├── base.html          # Base layout
│   ├── home.html          # Dashboard
│   ├── login.html         # Login page
│   ├── signup.html        # Signup page
│   ├── search.html        # Search interface
│   ├── programs.html      # Program management
│   └── client_profile.html# Client details
├── requirements.txt       # Dependencies
└── README.md              # Documentation

## Usage 🚀
Sign Up: Create an account at /signup.

Log In: Authenticate at /login.

Dashboard (/home):

Create Programs: Enter a program name (e.g., "HIV").

Register Clients: Add client names (e.g., "Alice").

Enroll Clients: Link clients to programs using IDs.

Search Clients: Visit /search for real-time client lookup.

Manage Programs: Delete programs at /programs.