from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database import get_db

from models import Category

from schemas import(
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.post("",response_model=CategoryResponse)
def create_category(create_category:CategoryCreate,
                    db:Session= Depends(get_db)):
    
    existing_category = db.query(Category).filter(Category.name == create_category.name).first()

    if existing_category:
        raise HTTPException(
            status_code=400,
            detail="Category with this name already exists"
        )
    
    new_category = Category(
        name = create_category.name
    )

    db.add(new_category)

    db.commit()
    db.refresh(new_category)

    return new_category
    
#------------------------------------------------
@router.get("",response_model=list[CategoryResponse])
def get_categories(db:Session = Depends(get_db)):

    return (
        db.query(Category).all()
    )

#-----------------------------------------------------
@router.put("/{id}",response_model=CategoryResponse)
def update_category(id:int,
                    update_category:CategoryUpdate,
                    db:Session = Depends(get_db)):
    
    category = db.query(Category).filter(Category.id == id).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    
    existing_category = (
        db.query(Category).filter(
            Category.name == update_category.name,
            Category.id != category.id).first()
    )
    if existing_category:
        raise HTTPException(
            status_code=400,
            detail="Category already exists"
        )
    
    category.name = update_category.name

    db.commit()
    db.refresh(category)

    return category

#---------------------------------------------------
@router.delete("/{id}")
def delete_category(id: int,
                    db:Session= Depends(get_db)):
    
    category = db.query(Category).filter(Category.id == id).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    
    if category.products:
        raise HTTPException(
            status_code=400,
            detail="Category has products"
        )
    
    db.delete(category)

    db.commit()

    return (
        {"message":"Category deleted successfully"}
    )
    