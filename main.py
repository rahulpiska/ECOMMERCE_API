from fastapi import FastAPI

from routes import users, auth, categories, products, cart

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(cart.router)

