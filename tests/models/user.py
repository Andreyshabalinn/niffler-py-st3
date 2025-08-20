from pydantic import BaseModel

class UserName(BaseModel):
    username: str