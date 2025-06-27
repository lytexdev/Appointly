from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from config.database import engine, Base
from config.settings import settings
from routers import slots, admin, auth, tenants, super_admin

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tenants.router, prefix="/api/tenants", tags=["tenants"])
app.include_router(slots.router, prefix="/api", tags=["slots"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(super_admin.router, prefix="/api/super-admin", tags=["super-admin"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

# Special route for tenant booking pages (must be after /api routes)
@app.get("/{username}")
def tenant_page(username: str):
    """Serve tenant booking page"""
    # This will be handled by Vue Router
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")

# Mount static files (Vue frontend)
app.mount("/", StaticFiles(directory="static", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
