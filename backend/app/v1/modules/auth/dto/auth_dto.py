from pydantic import BaseModel, Field, EmailStr

class LoginDTO(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)