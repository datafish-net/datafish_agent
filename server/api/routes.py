from fastapi import APIRouter, HTTPException
from api.models import CommandRequest, CommandResponse
from services.terminal import execute_terminal_command

router = APIRouter(prefix="/api")

@router.post("/terminal", response_model=CommandResponse)
async def execute_command(request: CommandRequest):
    """
    Execute a terminal command and return the output
    """
    command = request.command.strip()
    return await execute_terminal_command(command) 