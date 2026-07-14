from fastapi import APIRouter,Depends,HTTPException
from database import get_db
from sqlalchemy.orm import Session
import schemas
import services
import models

router =APIRouter(prefix="/blog",tags=["b"])

@router.post("/", response_model=schemas.BlogResponse)
def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db), user: models.Users = Depends(services.require_roles(["admin"]))):
    return services.create_blog(db, blog)


@router.get("/", response_model=list[schemas.BlogResponse])
def read_blogs(db: Session = Depends(get_db), user: models.Users = Depends(services.require_roles(["guest","admin"]))):
    return services.get_blogs(db)


@router.get("/{blog_id}", response_model=schemas.BlogResponse)
def read_blog(blog_id: int, db: Session = Depends(get_db), user: models.Users = Depends(services.get_current_user)):
    blog = services.get_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.put("/{blog_id}", response_model=schemas.BlogResponse)
def update_blog(blog_id: int, blog_update: schemas.BlogCreate, db: Session = Depends(get_db), user: models.Users = Depends(services.get_current_user)):
    blog = services.update_blog(db, blog_id, blog_update)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.delete("/{blog_id}")
def delete_blog(blog_id: int, db: Session = Depends(get_db), user: models.Users = Depends(services.get_current_user)):
    blog = services.delete_blog(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"message": "Blog deleted"}