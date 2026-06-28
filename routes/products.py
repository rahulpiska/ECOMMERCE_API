from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Category, Product, User
from utils import get_current_admin

from schemas import(
    ProductCreate,
    ProductResponse,
    ProductUpdate
)

router = APIRouter(
    prefix="/products",
    tags=['Products']
)

@router.post("",response_model=ProductResponse)
def create_product(create_product: ProductCreate,
                   admin: User = Depends(get_current_admin),
                   db:Session= Depends(get_db)):

    
    category = db.query(Category).filter(Category.id == create_product.category_id).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )
    
    if create_product.price <= 0:
        raise HTTPException(
            status_code=400,
            detail="Price must be positive"
        )
    if create_product.stock_quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Stock must be positive"
        )
    
    new_product = Product(
        name = create_product.name,
        description = create_product.description,
        price = create_product.price,
        stock_quantity = create_product.stock_quantity,
        category_id = create_product.category_id
    )

    db.add(new_product)

    db.commit()
    db.refresh(new_product)

    return new_product

#-----------------------------------------------------------------------

@router.get("",response_model=list[ProductResponse]) 
def get_all_products(
    category: str | None = None,
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    db:Session= Depends(get_db)):

    query = db.query(Product)

    if category :
        category_obj= (
            db.query(Category)
            .filter(Category.name.ilike(category))
            .first()     
        ) 
        if not category_obj: 
            raise HTTPException(
                 status_code=404, 
                 detail="Category not exists")
        
        query = query.filter(Product.category_id == category_obj.id)
        
    if search:
        query = (
            query
            .filter(Product.name.ilike(f"%{search}%"))
        )

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
       query = query.filter(Product.price <= max_price)

    return query.all()
    

#--------------------------------------------------------------------------

@router.get("/{id}",response_model=ProductResponse)
def get_product_by_id(id:int,
                      db:Session= Depends(get_db)):

    product = db.query(Product).filter(Product.id == id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

#------------------------------------------------------------------------
@router.put("/{id}",response_model=ProductResponse)
def update_product(id:int,
                   update_product:ProductUpdate,
                   admin: User = Depends(get_current_admin),
                   db:Session= Depends(get_db)):

    product = db.query(Product).filter(Product.id == id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    
    if update_product.category_id is not None:

        category =( 
            db.query(Category).filter(
                Category.id == update_product.category_id).first()
        )
    
        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )
        product.category_id = update_product.category_id


    if update_product.price is not None:
        
       if update_product.price <= 0:
            raise HTTPException(
                status_code=400,
                detail="Price must be positive"
        )
       product.price = update_product.price
    
    
    if update_product.stock_quantity is not None:

        if update_product.stock_quantity <= 0:
            raise HTTPException(
                status_code=400,
                detail="Stock must be positive"
        )
        product.stock_quantity = update_product.stock_quantity

    
    
    if update_product.name is not None:
        product.name = update_product.name
    
    if update_product.description is not None:
        product.description = update_product.description


    db.commit()
    db.refresh(product)

    return product


#----------------------------------------------------------------------

@router.delete("/{id}")
def delete_product(id:int,
                   admin: User = Depends(get_current_admin),
                   db:Session= Depends(get_db)):
    

    product = db.query(Product).filter(Product.id == id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    
    if product.cart_items:
        raise HTTPException(
            status_code=400,
            detail="Product exists in Carts"
        )
    
    if product.order_items:
        raise HTTPException(
            status_code=400,
            detail="Product exists in orders"
        )
    
    db.delete(product)

    db.commit()

    return (
        {"message":"Product deleted successfully"}
    )
    
