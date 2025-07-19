from fastapi import FastAPI, Request,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from config import Settings
from app.database import Base, engine
from app.routers import auth, chat, users


def create_app():
    app = FastAPI(title=Settings.PROJECT_NAME, debug=Settings.DEBUG)
    
    # Setup CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=Settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(chat.router)
    
    # Exception handlers
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    
    return app


app = create_app()


@app.on_event("startup")
async def startup():
    # Create database tables
    Base.metadata.create_all(bind=engine)