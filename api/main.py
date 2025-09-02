# Main FastAPI app with CORS middleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import summarize, tasks, diagrams

# Initialize FastAPI
app = FastAPI(title="TaskFlowAI Demo")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes for demo features
app.include_router(summarize.router, prefix="/summarize")
app.include_router(diagrams.router, prefix="/diagrams")
app.include_router(tasks.router, prefix="/tasks")


# Root endpoint to confirm API is running
@app.get("/")
async def root():
    return {"message": "TaskFlowAI Demo API"}