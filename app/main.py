from fastapi import FastAPI
from routers import auth_router, profile_router, server_router, ssh_router
from app.database import engine, Base
from app import models

app = FastAPI(title="Remote Server Manager API")

app.include_router(auth_router.router)
app.include_router(profile_router.router)
app.include_router(server_router.router)
app.include_router(ssh_router.router)

Base.metadata.create_all(bind=engine)