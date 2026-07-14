from pydantic import BaseModel

class UserCreate(BaseModel):
    id:int
    name:str
    email:str
    password:str
    role:str

class UserResponse(UserCreate):
    id :int
    name:str

    class Config:
        from_attributes=True


class BlogBase(BaseModel):
    title:str
    description:str


class BlogCreate(BlogBase):
    pass

class BlogResponse(BlogBase):
    id: int

    class Config:
        from_attributes = True

