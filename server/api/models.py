from pydantic import BaseModel

class CommandRequest(BaseModel):
    command: str

class CommandResponse(BaseModel):
    output: str
    status: int = 0 