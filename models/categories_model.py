from schemas import categories_schema
from sqlalchemy.orm import Session
from database import models

def get_categories(db: Session):
    return db.query(models.Categories).all()

def get_category_by_id(db: Session, category_id: str):
    return db.query(models.Categories).filter(models.Categories.id == category_id).first()

def create_category(db: Session, category: categories_schema.Category):
    new_category = models.Categories(name=category.name,description=category.description)   
    db.add(new_category)
    db.commit()
    return new_category

def delete_category(db: Session, category_id: str):
    category = db.query(models.Categories).filter(models.Categories.id == category_id).first()
    db.delete(category)
    db.commit()
    return category

def update_category(db: Session, category_id: str, category: categories_schema.Category):
    category = db.query(models.Categories).filter(models.Categories.id == category_id).first()
    category.name = category.name
    category.description = category.description
    db.commit()
    return category


