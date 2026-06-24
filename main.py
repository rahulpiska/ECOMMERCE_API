from fastapi import FastAPI

from routes import users, auth, categories

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(categories.router)


