from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import List, Optional
from contextlib import asynccontextmanager
import os

# Database setup
DATABASE_URL = "sqlite:///./tasks.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database model
class TaskModel(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool

    class Config:
        from_attributes = True

# Initialize sample data
def init_sample_data():
    db = SessionLocal()
    if db.query(TaskModel).count() == 0:
        sample_tasks = [
            TaskModel(title="Complete project proposal", description="Write and submit the Q4 project proposal document", completed=False),
            TaskModel(title="Review pull requests", description="Review and approve pending PRs from the team", completed=True),
            TaskModel(title="Update documentation", description="Add API documentation for the new endpoints", completed=False),
            TaskModel(title="Team meeting preparation", description="Prepare slides for the weekly team sync", completed=False),
            TaskModel(title="Fix navigation bug", description="Resolve the issue with mobile navigation menu", completed=True),
        ]
        db.add_all(sample_tasks)
        db.commit()
    db.close()

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_sample_data()
    yield

# FastAPI app
app = FastAPI(title="TaskFlow Lite API", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API endpoints
@app.get("/api/tasks", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskModel).all()
    return tasks

@app.get("/api/tasks/stats")
def get_task_stats(db: Session = Depends(get_db)):
    total = db.query(TaskModel).count()
    completed = db.query(TaskModel).filter(TaskModel.completed == True).count()
    pending = total - completed
    return {"total": total, "completed": completed, "pending": pending}

@app.get("/api/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/api/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    if not task.title or len(task.title.strip()) == 0:
        raise HTTPException(status_code=400, detail="Title is required")
    
    db_task = TaskModel(
        title=task.title,
        description=task.description,
        completed=False
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task_update.title is not None:
        if len(task_update.title.strip()) == 0:
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        db_task.title = task_update.title
    if task_update.description is not None:
        db_task.description = task_update.description
    if task_update.completed is not None:
        db_task.completed = task_update.completed
    
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
