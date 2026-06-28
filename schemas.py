from pydantic import BaseModel, EmailStr, ConfigDict, Field

from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_admin: bool
    created_at: datetime

    model_config= ConfigDict(
        from_attributes=True
    )

#---------------------------------------------

class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    model_config= ConfigDict(
        from_attributes=True
    )

#---------------------------------------------------

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock_quantity: int
    category_id: int

class ProductUpdate(BaseModel):
    name: str | None=None
    description: str | None=None
    price: float | None=None
    stock_quantity: int | None=None
    category_id: int | None=None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock_quantity: int
    category_id: int
    created_at: datetime

    model_config= ConfigDict(
        from_attributes=True
    )

#-------------------------------------------

class CartCreate(BaseModel):
    product_id: int
    quantity: int = Field(default=1, gt=0)

class CartResponse(BaseModel):
    id: int
    cart_id: int
    product_id: int
    quantity: int

    model_config= ConfigDict(
        from_attributes=True
    )

class CartItemResponse(BaseModel):
    cart_item_id: int
    product_id: int
    product_name: str
    description: str
    price: float
    quantity: int
    stock_available: int
    subtotal: float 

class CartSummaryResponse(BaseModel):
    items: list[CartItemResponse]
    total_amount: float

    model_config= ConfigDict(
        from_attributes=True
    )

class CartUpdate(BaseModel):
    quantity: int

#-------------------------------------------

class OrderResponse(BaseModel):
    id:int
    total_amount: float
    status: str
    created_at: datetime

    model_config= ConfigDict(
        from_attributes=True
    )

class OrderItemResponse(BaseModel):
    product_name: str
    price: float
    quantity: int
    subtotal: float


class OrderDetailsResponse(BaseModel):
    order_id: int
    status: str
    total_amount: float
    created_at: datetime
    items: list[OrderItemResponse]