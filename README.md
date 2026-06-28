# 🛒 E-Commerce REST API

A RESTful E-Commerce Backend API built using **FastAPI**, **SQLAlchemy**, **MySQL**, and **JWT Authentication**.

This project simulates the backend of an online shopping application where users can browse products, manage a shopping cart, place orders, and administrators can manage products and categories.

---

# 🚀 Features

## Authentication

* User Registration
* User Login
* JWT Authentication
* Password Hashing using bcrypt
* Get Logged-in User

---

## Authorization

### Customer

* View Categories
* View Products
* Search Products
* Filter Products
* Add Products to Cart
* Manage Cart
* Place Orders
* View Order History
* View Order Details

### Admin

* Create Categories
* Update Categories
* Delete Categories
* Create Products
* Update Products
* Delete Products

---

# 📦 Product Features

* View All Products
* View Product by ID
* Filter Products by Category
* Search Products by Name
* Filter by Minimum Price
* Filter by Maximum Price
* Combine Multiple Filters

Example:

```http
GET /products?category=Shoes&search=nike&min_price=1000&max_price=5000
```

---

# 🛒 Shopping Cart

* Add Product to Cart
* Automatically Increase Quantity if Product Already Exists
* View Cart
* Update Cart Quantity
* Remove Product from Cart
* Automatic Stock Validation

---

# 📋 Orders

* Checkout
* Validate Stock Before Ordering
* Calculate Total Amount
* Create Order
* Create Order Items
* Reduce Product Stock
* Clear Shopping Cart After Checkout
* View Order History
* View Order Details

---

# 🗄 Database Relationships

* User → Cart (One-to-One)
* User → Orders (One-to-Many)
* Category → Products (One-to-Many)
* Cart → CartItems (One-to-Many)
* Product → CartItems (One-to-Many)
* Order → OrderItems (One-to-Many)
* Product → OrderItems (One-to-Many)

---

# 🛠 Tech Stack

* Python
* FastAPI
* SQLAlchemy ORM
* MySQL
* Alembic
* Pydantic
* JWT Authentication
* Passlib (bcrypt)
* Uvicorn

---

# 📂 Project Structure

```
E_COMMERCE_API/
│
├── alembic/
├── routers/
├── database.py
├── models.py
├── schemas.py
├── utils.py
├── main.py
├── requirements.txt
└── .env
```

---

# 🔐 Authentication Flow

1. Register a new user.
2. Login using email and password.
3. Receive a JWT access token.
4. Authorize using the token in Swagger UI.
5. Access protected endpoints.

---

# 🛍 Shopping Workflow

```
Register/Login
      │
      ▼
Browse Categories
      │
      ▼
Browse Products
      │
      ▼
Add Product to Cart
      │
      ▼
Manage Cart
      │
      ▼
Checkout
      │
      ▼
Stock Validation
      │
      ▼
Order Created
      │
      ▼
Inventory Updated
```

---

# 📚 API Endpoints

## Authentication

* POST `/users`
* POST `/auth/login`
* GET `/auth/me`

## Categories

* POST `/categories` *(Admin)*
* GET `/categories`
* PUT `/categories/{id}` *(Admin)*
* DELETE `/categories/{id}` *(Admin)*

## Products

* POST `/products` *(Admin)*
* GET `/products`
* GET `/products/{id}`
* PUT `/products/{id}` *(Admin)*
* DELETE `/products/{id}` *(Admin)*

## Cart

* POST `/cart`
* GET `/cart`
* PUT `/cart/{cart_item_id}`
* DELETE `/cart/{cart_item_id}`

## Orders

* POST `/orders`
* GET `/orders`
* GET `/orders/{order_id}`

---

# 💡 Concepts Implemented

* REST API Design
* JWT Authentication
* Role-Based Authorization
* SQLAlchemy Relationships
* Alembic Database Migrations
* CRUD Operations
* Business Logic Validation
* Shopping Cart Workflow
* Checkout Process
* Dynamic Query Filtering
* Nested API Responses
* Inventory Management
* Transaction Handling

---

# 📖 Future Improvements

* Product Pagination
* Product Images
* Wishlist
* Product Reviews
* Payment Gateway Integration
* Email Notifications
* Docker Deployment
* Unit & Integration Testing

---

# 👨‍💻 Author

**Rahul Piska**
