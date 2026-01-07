from sqlalchemy import Column, Integer,Text, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    phone = Column(String(20), nullable=False)
    photo_url = Column(String(255), nullable=True)

class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    host = Column(String(100), nullable=False)
    port = Column(Integer, default=22)
    username = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)  # encrypt later
    user_id = Column(Integer, ForeignKey("users.id"))


class SSHCommandLog(Base):
    __tablename__ = "ssh_command_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    server_id = Column(Integer, ForeignKey("servers.id"), nullable=False)
    command = Column(Text, nullable=False)
    stdout = Column(Text)
    stderr = Column(Text)
    exit_status = Column(Integer)
    executed_at = Column(DateTime, default=datetime.utcnow)

