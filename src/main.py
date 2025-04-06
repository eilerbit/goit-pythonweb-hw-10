from fastapi import FastAPI, Request, status
from src.api import auth, contacts, users
from starlette.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

app = FastAPI(
    title="Contacts API",
    version="1.0.0",
    description="REST API для керування контактами"
)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"error": "Перевищено ліміт запитів. Спробуйте пізніше."},
    )

app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(users.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
