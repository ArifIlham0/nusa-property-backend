import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text

from .config import HOST, PORT, UPLOAD_DIR
from .database import init_db, SessionLocal, get_db
from .seed import seed_database
from .routers import properties, calculator, documents, sp3k, user, admin, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    with SessionLocal() as db:
        seed_database(db)
    yield


app = FastAPI(
    title="Nusa Property API",
    description="Backend service for Nusa Property Android Application & KPR Services",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["ngrok-skip-browser-warning", "Content-Disposition"]
)

app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

app.include_router(auth.router)
app.include_router(properties.router)
app.include_router(calculator.router)
app.include_router(documents.router)
app.include_router(sp3k.router)
app.include_router(user.router)
app.include_router(admin.router)


@app.get("/")
def read_root():
    return {
        "status": "online",
        "app": "Nusa Property Backend",
        "version": "1.0.0",
        "database": "PostgreSQL (nusa_property)",
        "docsUrl": "/docs"
    }


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "ok" if db_status == "healthy" else "error",
        "database": db_status
    }


def main():
    uvicorn.run(
        "nusa_property_backend.main:app",
        host=HOST,
        port=PORT,
        reload=False
    )


if __name__ == "__main__":
    main()