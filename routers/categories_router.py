from fastapi import APIRouter,Depends, HTTPException
from database import models
from schemas import categories_schema
from database.database import SessionLocal, engine
from sqlalchemy.orm import Session
from services import categories_service

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/categories",tags=["categories"], response_model=list[categories_schema.Category])
def get_categories(db: Session= Depends(get_db)):
    categories = categories_service.get_categories(db=db)
    if categories is not None:
        return categories
    else:
        raise HTTPException(status_code=404, detail="Categories not found")
    
@router.get("/categories/{category_id}",tags=["categories"], response_model=categories_schema.Category)
def get_category(category_id: str,db: Session= Depends(get_db)):
    category = categories_service.get_category_by_id(db=db, category_id=category_id)
    if category is not None:
        return category
    else:
        raise HTTPException(status_code=404, detail="Category not found")
    
@router.post("/categories",tags=["categories"])
def add_category(category: categories_schema.Category,db: Session= Depends(get_db)):
    new_category = categories_service.create_category(db=db, category=category)
    if new_category is not None:
        raise HTTPException(status_code=200, detail="Category created successfully")
    else:
        raise HTTPException(status_code=500, detail="Error creating category")

@router.delete("/categories/{category_id}",tags=["categories"])
def delete_category(category_id: str,db: Session= Depends(get_db)):
    category = categories_service.delete_category(db=db, category_id=category_id)
    if category is not None:
        raise HTTPException(status_code=200, detail="Category deleted successfully")
    else:
        raise HTTPException(status_code=500, detail="Error deleting category")
    
@router.put("/categories/{category_id}",tags=["categories"])
def update_category(category_id: str, category: categories_schema.Category,db: Session= Depends(get_db)):
    category = categories_service.update_category(db=db, category_id=category_id, category=category)
    if category is not None:
        raise HTTPException(status_code=200, detail="Category updated successfully")
    else:
        raise HTTPException(status_code=500, detail="Error updating category")
