from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Server, SSHCommandLog, User
from app.schemas import SSHCommandCreate, SSHCommandResponse
import paramiko
import logging
from app.utils.email import send_email


router = APIRouter(prefix="/ssh", tags=["SSH"])

# -------- FILE LOGGING --------
logging.basicConfig(
    filename="app/logs/ssh_commands.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s"
)

# -------- BLOCKED COMMANDS --------
BLOCKED_COMMANDS = [
    "rm -rf /",
    "rm -rf *",
    "shutdown",
    "reboot",
    "mkfs",
    "dd",
    ":(){ :|:& };:"
]

# -------- EXECUTE SSH COMMAND --------
@router.post("/execute", response_model=SSHCommandResponse)
def execute_command(
    data: SSHCommandCreate,
    db: Session = Depends(get_db),
    user_id: int = 1  # JWT later
):
    # Block dangerous commands
    for bad_cmd in BLOCKED_COMMANDS:
        if bad_cmd in data.command.lower():
            raise HTTPException(
                status_code=400,
                detail="This command is not allowed"
            )

    # Fetch server
    server = db.query(Server).filter(
        Server.id == data.server_id,
        Server.user_id == user_id
    ).first()

    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    # Execute SSH
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
            hostname=server.host,
            port=server.port,
            username=server.username,
            password=server.password,
            timeout=10
        )

        stdin, stdout, stderr = ssh.exec_command(data.command)

        out = stdout.read().decode()
        err = stderr.read().decode()
        exit_status = stdout.channel.recv_exit_status()

        ssh.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Save log in DB
    log = SSHCommandLog(
        user_id=user_id,
        server_id=server.id,
        command=data.command,
        stdout=out,
        stderr=err,
        exit_status=exit_status
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    # Save log in file
    logging.info(
        f"user={user_id} | server={server.host} | cmd={data.command} | exit={exit_status}"
    )

    # 6️⃣ Fetch user email
    user = db.query(User).filter(User.id == user_id).first()

    # 7️⃣ Send email notification
    if user:
        send_email(
            to_email=user.email,
            subject="SSH Command Executed",
            body=f"""
Hello,

SSH command executed successfully.

Server: {server.name}
Host: {server.host}

Command:
{data.command}

Exit Status: {exit_status}
"""
)

    # Response
    return {
        "server_id": server.id,
        "command": data.command,
        "stdout": out,
        "stderr": err,
        "exit_status": exit_status,
        "executed_at": log.executed_at
    }

