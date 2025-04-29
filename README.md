# CEMA-TASK
# Health Information System

A system to manage clients and health programs.

## Features
- Create programs
- Register clients
- Search clients

## How to Run
1. Install Python and Flask.
2. Run `python app.py`.

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