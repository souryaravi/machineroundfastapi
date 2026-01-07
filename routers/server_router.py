from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Server
from app.schemas import ServerCreate, ServerResponse

router = APIRouter(prefix="/servers", tags=["Servers"])

# ADD SERVER 
@router.post("/")
def add_server(server: ServerCreate, db: Session = Depends(get_db)):
    db_server = Server(
        name=server.name,
        host=server.host,
        port=server.port,
        username=server.username,
        password=server.password
    )
    db.add(db_server)
    db.commit()
    db.refresh(db_server)
    return {"msg": "Server added", "server_id": db_server.id}

#  LIST SERVERS 
@router.get("/", response_model=List[ServerResponse])
def list_servers(db: Session = Depends(get_db)):
    servers = db.query(Server).all()
    return servers
