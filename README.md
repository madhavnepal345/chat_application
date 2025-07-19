# chat_application
Overview
A real-time chat application built with FastAPI, PostgreSQL, and WebSockets featuring:

JWT Authentication

Role-Based Access Control (RBAC)

WebSocket chat rooms

Message persistence

User management

# Features
🔒 Authentication

User registration and login

Password hashing

JWT token generation

👥 User Management

Admin and user roles

User activity tracking

Profile management

💬 Real-time Chat

Multiple chat rooms

Message history

Online presence indicators

Prerequisites
Python 3.9+

PostgreSQL

Redis (optional for production scaling)

Installation
Clone the repository

bash
git clone https://github.com/yourusername/chat-app.git
cd chat-app
Set up virtual environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Database setup

bash
createdb chat_app
createdb chat_app_test
Environment variables
Create .env file:

env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/chat_app
SECRET_KEY=your-secure-secret-key-here
DEBUG=true
ALLOWED_ORIGINS=http://localhost:3000