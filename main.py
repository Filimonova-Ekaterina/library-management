from fastapi import FastAPI
from contextlib import asynccontextmanager
from config.database import engine, Base, get_db
from config.data_loader import DataLoader
from controllers import book_controller, author_controller, user_controller
import models

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    
    from config.database import SessionLocal
    db = SessionLocal()
    try:
        data_loader = DataLoader(db)
        data_loader.load_test_data()
    finally:
        db.close()
    
    yield

app = FastAPI(
    title="Library Management System",
    description="Spring Boot-like library management API built with FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(book_controller.router)
app.include_router(author_controller.router)

@app.get("/")
def read_root():
    return {"message": "Library Management System is running!"}

@app.get("/health")
def health_check():
    return {"status": "UP", "service": "library-management"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)