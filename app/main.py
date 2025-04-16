
from fastapi import FastAPI
from app.routers import health_router

app = FastAPI(title="System Health Check API")
app.include_router(health_router.router, prefix="/api")


