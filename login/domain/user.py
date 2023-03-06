from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str

def user_schema(data: dict) -> dict:
    return {"email": data["email"], "password": data["password"]}

class Token:
    def __init__(self, access_token: str, token_type: str):
        self.access_token = access_token
        self.token_type = token_type
