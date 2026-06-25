from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import (
    CartCreate,
    CartResponse,
    CartItemResponse,
    CartSummaryResponse,
    CartUpdate
)
from models import User, Product, Cart, CartItem

from utils import get_current_user

router = APIRouter(
    prefix="/cart",
    tags=["Carts"]
)

@router.post("",response_model=CartResponse)
def create_cart(create_cart: CartCreate,
                current_user: User = Depends(get_current_user),
                db:Session = Depends(get_db)):
    
    product = db.query(Product).filter(Product.id == create_cart.product_id).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    
    if create_cart.quantity > product.stock_quantity:
        raise HTTPException(
            status_code=400,
            detail="insufficient stock"
        )
  
    cart= db.query(Cart).filter(Cart.user_id == current_user.id).first()

    if not cart:
        cart = Cart(
            user_id = current_user.id
        )
        
        db.add(cart)
        db.commit()
        db.refresh(cart)


    existing_cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == create_cart.product_id
    ).first()

    if existing_cart_item:
        new_quantity = existing_cart_item.quantity + create_cart.quantity

        if new_quantity > product.stock_quantity:
            raise HTTPException(
                status_code=400,
                detail="Insufficient stock"
            )
        existing_cart_item.quantity = new_quantity
        cart_item = existing_cart_item

    else:
        cart_item = CartItem(
        cart_id = cart.id,
        product_id = create_cart.product_id,
        quantity = create_cart.quantity
    )
        
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)

    return cart_item

    
#---------------------------------------------------------------------------
@router.get("",response_model=CartSummaryResponse)
def get_cart_items(current_user: User = Depends(get_current_user),
                   db:Session = Depends(get_db)):
      
      cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
      
      if not cart:
          raise HTTPException(
              status_code=404,
              detail="Cart is Empty"
          )

      cart_items =( 
          db.query(CartItem,Product)
          .join(Product,CartItem.product_id== Product.id)
          .filter(CartItem.cart_id == cart.id).all()
        )
      if not cart_items:
          return {
              "items": [],
              "total_amount": 0
          }
          
      
      items_response = []

      total_amount = 0
      
      for cart_item, product in cart_items:
          
          subtotal = product.price * cart_item.quantity

          total_amount += subtotal

          items_response.append(
              {
              "cart_item_id": cart_item.id,
              "product_id":product.id,
              "product_name":product.name,
              "description":product.description,
              "price":product.price,
              "quantity":cart_item.quantity,
              "stock_available":product.stock_quantity,
              "subtotal":subtotal
          }
        )
          
      return{
          "items":items_response,
          "total_amount":total_amount
      }


#----------------------------------------------------------------------------

@router.put("/{cart_item_id}",response_model=CartResponse)
def update_cart_item(cart_item_id: int,
                    update_cart_item:CartUpdate,
                     current_user: User = Depends(get_current_user),
                     db:Session = Depends(get_db)):

    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )
        
    if cart_item.cart.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden, You are not allowed"
        )
    
    product = cart_item.product

    if update_cart_item.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be positive"
        )

    if  update_cart_item.quantity > product.stock_quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock"
        )
    cart_item.quantity = update_cart_item.quantity

    db.commit()
    db.refresh(cart_item)

    return cart_item

#--------------------------------------------------------------------------------

@router.delete("/{cart_item_id}")
def delete_cart_item(cart_item_id: int,
                     current_user: User = Depends(get_current_user),
                     db:Session = Depends(get_db)):
    
    cart_item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()

    if not cart_item:
        raise HTTPException(
            status_code=404,
            detail="Cart Item not found"
        )
    
    if cart_item.cart.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden, You are not allowed"
        )
    
    db.delete(cart_item)

    db.commit()

    return (
        {"message":"Cart item deleted successfully"}
    )
