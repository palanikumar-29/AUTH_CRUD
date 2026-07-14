from sqlalchemy import Column,Integer,String;
from database import Base;

class Users(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(50),unique=True,index=True)
    email=Column(String(50),unique=True,index=True)
    password=Column(String(100))
    role=Column(String(50),default="guest")


class Blog(Base):
    __tablename__="blogs"

    id =Column(Integer,primary_key=True,index=True)
    title =Column(String(100))
    description =Column(String(250))