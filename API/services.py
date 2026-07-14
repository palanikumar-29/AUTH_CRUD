from sqlalchemy.orm import Session
from models import Users,Blog
from schemas import UserCreate,BlogCreate
import auth

def create_user(db:Session,user:UserCreate):
     hashed = auth.hash_password(user.password)
     new_user=Users(name=user.name,email=user.email,password=hashed,role=user.role)
     db.add(new_user)
     db.commit()
     db.refresh(new_user)
     return new_user 

def get_user(db:Session):
     return db.query(Users).all()

def get_user_by_name(db:Session,name:str):
     return db.query(Users).filter(Users.name==name).first()


#update and delete 

def update_user(db: Session, name: str, update: UserCreate):
    db_user = get_user_by_name(db, name)

    if db_user:
        db_user.name = update.name
        db_user.email = update.email
        db_user.password = auth.hash_password(update.password)
        db_user.role = update.role

        db.commit()
        db.refresh(db_user)

    return db_user

def delete_user(db:Session,name:str):
    db_user=get_user_by_name(db,name)

    if db_user is None:
        raise HTTPException(status_code=404,detail="user not found")
    db.delete(db_user)
    db.commit()

    return db_user


#token authentication

from fastapi.security import OAuth2PasswordBearer
from database import get_db
from jose import jwt, JWTError
import models
from fastapi import HTTPException,Depends


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/u1/user/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, auth.SECRET_KEY,
        algorithms=[auth.ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
        user = get_user_by_name(db, username)

        if user is None:
         raise HTTPException(
        status_code=401,
        detail="User not found"
        )

        user.role = role
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

def require_roles(allowed_roles: list):
    def role_checker(user: models.Users = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(    
                status_code=403,
                detail="You are not authorized for this action"
            )
        return user
    return role_checker


#blogs

def create_blog(db: Session, blog: BlogCreate):
    db_blog = Blog(title=blog.title, description=blog.description)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog


def get_blogs(db: Session):
    return db.query(Blog).all()


def get_blog(db: Session, blog_id: int):
    return db.query(Blog).filter(Blog.id == blog_id).first()


def delete_blog(db: Session, blog_id: int):
    blog = get_blog(db, blog_id)
    if blog:
        db.delete(blog)
        db.commit()
    return blog

def update_blog(db: Session, blog_id: int, blog_update: BlogCreate):
    blog = get_blog(db, blog_id)
    if blog:
        blog.title = blog_update.title
        blog.description = blog_update.description
        db.commit()
        db.refresh(blog)
    return blog