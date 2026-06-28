from sqlalchemy import Column,String,ForeignKey,Integer,Float, DateTime, Boolean

from sqlalchemy.orm import relationship

from database import Base

from datetime import datetime

#----------------------------------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(100),nullable=False)
    email = Column(String(225),unique=True,nullable=False)
    password = Column(String(225),nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    cart = relationship(
        "Cart",
        back_populates="user",
        uselist=False
    )

    orders = relationship(
        "Order",
        back_populates="user"
    )

#--------------------------------------------------

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100),nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    products = relationship(
        "Product",
        back_populates="category"
    )

#-------------------------------------------------

class Product(Base):
    __tablename__= "products"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100),nullable=False)
    description = Column(String(225),nullable=False)
    price = Column(Float,nullable=False)
    stock_quantity = Column(Integer,nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"),nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship(
        "Category",
        back_populates="products"
    )

    cart_items = relationship(
        'CartItem',
        back_populates="product"
    )

    order_items = relationship(
        "OrderItem",
        back_populates="product"
    )

#-----------------------------------------------

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship(
        "User",
        back_populates="cart"
    )
    cart_items = relationship(
        "CartItem",
        back_populates="cart"
    )

#----------------------------------------------------

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer,primary_key=True, index=True)
    cart_id = Column(Integer,ForeignKey("carts.id"),nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"),nullable=False)
    quantity = Column(Integer, nullable=False)

    cart = relationship(
        "Cart",
        back_populates="cart_items"
    )

    product = relationship(
        "Product",
        back_populates="cart_items"
    )

#----------------------------------------------------

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship(
        "User",
        back_populates="orders"
    )

    order_items = relationship(
        "OrderItem",
        back_populates="order"
    )

#-------------------------------------------------

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'),nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer,nullable=False)
    price = Column(Float, nullable=False)

    order = relationship(
        "Order",
        back_populates="order_items"
    )

    product = relationship(
        "Product",
        back_populates="order_items"
    )

#--------------------------------------------------