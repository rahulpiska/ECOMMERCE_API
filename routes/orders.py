from database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from models import Cart, User, CartItem, Product, Order, OrderItem
from schemas import (
    OrderResponse,
    OrderDetailsResponse
)
from utils import get_current_user

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("",response_model=OrderResponse)
def place_order(current_user: User = Depends(get_current_user),
                db:Session = Depends(get_db)):
    
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()

    if not cart:
        raise HTTPException(
            status_code=400,
            detail="Cart is Empty"
        )
    
    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    
    if not cart_items:
        raise HTTPException(
            status_code=400,
            detail="Cart is Empty"
        )
    
    
    total_amount = 0
    for cart_item in cart_items:


        product = cart_item.product

        if cart_item.quantity > product.stock_quantity:
            raise HTTPException(
                status_code=400,
                detail= "Insufficient stock"
            ) 
        
        subtotal = product.price * cart_item.quantity

        total_amount += subtotal



    order = Order(
        user_id= current_user.id,
        total_amount= total_amount,
        status= "Pending"
    )

    db.add(order)
    db.flush()

    for cart_item in cart_items:

        product = cart_item.product
        
        order_item = OrderItem(
            order_id = order.id,
            product_id = cart_item.product_id,
            quantity = cart_item.quantity,
            price = product.price
        )

        product.stock_quantity -= cart_item.quantity

        db.add(order_item)

        db.delete(cart_item)

    db.commit()
        
    db.refresh(order)

    return order

#-------------------------------------------------------------------------------

@router.get("",response_model=list[OrderResponse])
def get_orders(current_user: User = Depends(get_current_user),
               db:Session = Depends(get_db)):
    
    orders = (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )


    return orders

#------------------------------------------------------------------------------

@router.get("/{order_id}",response_model=OrderDetailsResponse)
def get_order_details(order_id: int,
                      current_user: User= Depends(get_current_user),
                      db:Session = Depends(get_db)):
    
    order = (
        db.query(Order)
        .filter(Order.id == order_id).first())
    
    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )
    

    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden,You are not allowed"
        )
    
    items = []

    for order_item in order.order_items:
        
        product = order_item.product

        items.append(
            {
                "product_name": product.name,
                "price": order_item.price,
                "quantity": order_item.quantity,
                "subtotal": order_item.price * order_item.quantity
            }
        )
        

    return (
        {
            "order_id": order.id,
            "status":order.status,
            "total_amount":order.total_amount,
            "created_at": order.created_at,
            "items":items
        }
    )

    





    
    

