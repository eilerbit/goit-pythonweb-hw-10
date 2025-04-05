﻿from fastapi import FastAPI
from src.api import auth, contacts

app = FastAPI(
    title="Contacts API",
    version="1.0.0",
    description="REST API для керування контактами"
)

app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
