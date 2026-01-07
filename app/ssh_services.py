import paramiko

BLOCKED_COMMANDS = ["rm -rf /", "shutdown", "reboot"]

def execute_ssh_command(host, user, password, command):
    if any(cmd in command for cmd in BLOCKED_COMMANDS):
        return {"error": "Command blocked"}

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=password)

    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()

    ssh.close()

    return {
        "output": output,
        "error": error,
        "status": 0 if not error else 1
    }
