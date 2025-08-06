from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    # id: str | None
    id: Optional[str] = None
    username: str
    first_name: str
    last_name: str
    email: str
    age: int