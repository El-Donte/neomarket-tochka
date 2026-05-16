from typing import Optional
from pydantic import BaseModel

    
class Error(BaseModel):
    code: int
    message: str
    details: Optional[str]