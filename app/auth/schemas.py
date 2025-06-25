from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    phone_number: str
    password: str
