from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class ProfileCreate(BaseModel):
    first_name: str
    last_name: str
    age: int
    phone: str
    photo_url: str | None = None


class ServerCreate(BaseModel):
    name: str
    host: str
    port: int = 22
    username: str
    password: str


class ServerResponse(BaseModel):
    id: int
    name: str
    host: str
    port: int
    username: str
    class Config:
        from_attributes = True


# -------- SSH REQUEST --------
class SSHCommandCreate(BaseModel):
    server_id: int
    command: str


# -------- SSH RESPONSE --------
class SSHCommandResponse(BaseModel):
    server_id: int
    command: str
    stdout: str
    stderr: str
    exit_status: int
    executed_at: datetime

    class Config:
        from_attributes = True