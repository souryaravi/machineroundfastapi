SSH Manager API (FastAPI)

A FastAPI backend REST API service to manage remote Linux servers via SSH, with user authentication, server management, command execution, and email notifications.

Features

## User Authentication

Register & login with hashed passwords (bcrypt)

JWT authentication (planned for production)

## Server Management

Add, list

Store server details securely

## Profile Management

Create, update, view, delete user profile

Profile includes first name, last name, age, phone, and profile photo

## SSH Command Execution

Execute shell commands on registered servers

Block dangerous commands like rm -rf /, shutdown, reboot

Logs each command execution in database and log file

Returns stdout, stderr, exit status

Email Notifications

Send email when commands are executed

Send welcome email on user registration

Configurable SMTP (Gmail, SendGrid, etc.)

## Database

MySQL database using SQLAlchemy ORM

Tables for users, servers, profiles, and command logs

Tech Stack

Python 3.14

FastAPI

SQLAlchemy

MySQL (or MariaDB)

Pydantic

Paramiko (SSH)

Passlib (password hashing)

SMTP (Email notifications)

Uvicorn (ASGI server)

Setup Instructions
1. Clone repository
git clone <your-repo-url>
cd FastApi-SSH-Manager

2. Create virtual environment
python -m venv myenv
myenv\Scripts\activate   # Windows
# or
source myenv/bin/activate  # Linux / Mac

3. Install dependencies
pip install -r requirements.txt

4. Configure environment variables

Create a .env file in the root:

DATABASE_URL=mysql+pymysql://root:password@localhost:3306/fasttask

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM=your_email@gmail.com


Note: For Gmail, generate an App Password and use it for SMTP_PASSWORD.

5. Create database tables

Open Python shell:

python


Then run:

from app.database import Base, engine
from app.models import User, Server, Profile, SSHCommandLog

Base.metadata.create_all(bind=engine)


✅ This will create all required tables in MySQL.

6. Run FastAPI server
uvicorn app.main:app --reload


API docs: http://127.0.0.1:8000/docs

Redoc: http://127.0.0.1:8000/redoc

API Endpoints
Auth
| Method | Endpoint         | Description       |
| ------ | ---------------- | ----------------- |
| POST   | `/auth/register` | Register user     |
| POST   | `/auth/login`    | Login and get JWT |

Profile
| Method | Endpoint    | Description         |
| ------ | ----------- | ------------------- |
| POST   | `/profile/` | Create user profile |
| GET    | `/profile/` | Get profile         |
| PUT    | `/profile/` | Update profile      |
| DELETE | `/profile/` | Delete profile      |

Servers
| Method | Endpoint        | Description      |
| ------ | --------------- | ---------------- |
| POST   | `/servers/`     | Add server       |
| GET    | `/servers/`     | List all servers |


SSH Commands
| Method | Endpoint       | Description                      |
| ------ | -------------- | -------------------------------- |
| POST   | `/ssh/execute` | Execute command on remote server |
| GET    | `/ssh/logs`    | Fetch executed command logs      |

Logging

Command execution logs are saved in app/logs/ssh_commands.log

Logs include user, server, command, timestamp, exit status

Notes

Dangerous commands like rm -rf / are blocked for safety

Currently, user_id is static for testing; replace with JWT for production

Passwords are hashed with bcrypt

Email notifications are sent asynchronously