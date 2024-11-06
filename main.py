from fastapi import FastAPI
from router import users, items
from authorization import auth

app = FastAPI()

# Include the routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)
