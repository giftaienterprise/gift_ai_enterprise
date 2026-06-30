from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    password: str
    nickname: str | None = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    nickname: str | None = None
    is_active: bool
    is_admin: bool

    model_config = {
        "from_attributes": True
    }