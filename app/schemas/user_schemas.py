from pydantic import BaseModel, constr, EmailStr


class UserPayload(BaseModel):
    username: str
    email: str
    password: constr(min_length=8)


class UserCredentials(BaseModel):
    email: str
    password: constr(min_length=8)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
