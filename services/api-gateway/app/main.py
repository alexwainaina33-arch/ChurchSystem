from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import church as church_models
from app.routers import churches, branches, members, attendance, giving, projects, messages, dashboard

app = FastAPI(title="Church System API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3002", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "Church System API"}

app.include_router(churches.router, prefix="/api/v1/churches", tags=["Churches"])
app.include_router(branches.router, prefix="/api/v1/branches", tags=["Branches"])
app.include_router(members.router, prefix="/api/v1/members", tags=["Members"])
app.include_router(attendance.router, prefix="/api/v1/attendance", tags=["Attendance"])
app.include_router(giving.router, prefix="/api/v1/giving", tags=["Giving"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(messages.router, prefix="/api/v1/messages", tags=["Messages"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
