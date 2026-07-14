from fastapi import APIRouter,Depends,HTTPException
from database import get_db
from sqlalchemy.orm import Session
import schemas
import services
import auth

from fastapi.security import OAuth2PasswordRequestForm



router =APIRouter(prefix="/user",tags=["u"])

@router.get("/",response_model=list[schemas.UserResponse])
def get_user(db:Session=Depends(get_db)):
    return services.get_user(db)

@router.post("/",response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    return services.create_user(db,user)

@router.put("/{name}",response_model=schemas.UserResponse)
def update_user(name:str,update:schemas.UserCreate,db:Session=Depends(get_db)):
    return services.update_user(db,name,update)

@router.delete("/{name}",response_model=schemas.UserResponse)
def delete_user(name:str,db:Session=Depends(get_db)):
    return services.delete_user(db,name)
#login route

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if services.get_user_by_name(db, user.name):
        raise HTTPException(status_code=400, detail="User already exists")
    return services.create_user(db, user)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = services.get_user_by_name(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = auth.create_access_token({"sub": user.name, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/profile")
def profile(current_user=Depends(services.get_current_user)):
    return{"id":current_user.id,
           "name":current_user.name,
           "email":current_user.email,
           "role":current_user.role
           }