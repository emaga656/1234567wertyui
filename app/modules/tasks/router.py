from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Project, Task, User
from app.core.deps import get_current_user
from app.modules.tasks.schemas import TaskCreate, TaskUpdate, TaskOut

router = APIRouter(tags=["Tasks"])
VALID_STATUSES = {"todo", "in_progress", "done"}

def owned_project(db: Session, project_id: int, user_id: int):
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == user_id).first()
    if not project: raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.post("/projects/{project_id}/tasks", response_model=TaskOut, status_code=201)
def create_task(project_id: int, data: TaskCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    owned_project(db, project_id, user.id)
    task = Task(**data.model_dump(), project_id=project_id)
    db.add(task); db.commit(); db.refresh(task)
    return task

@router.get("/projects/{project_id}/tasks", response_model=list[TaskOut])
def list_tasks(project_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    owned_project(db, project_id, user.id)
    return db.query(Task).filter(Task.project_id == project_id).order_by(Task.id.desc()).all()

@router.patch("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    task = db.query(Task).join(Project).filter(Task.id == task_id, Project.owner_id == user.id).first()
    if not task: raise HTTPException(status_code=404, detail="Task not found")
    changes = data.model_dump(exclude_unset=True)
    if "status" in changes and changes["status"] not in VALID_STATUSES:
        raise HTTPException(status_code=422, detail="Status must be todo, in_progress or done")
    for key, value in changes.items(): setattr(task, key, value)
    db.commit(); db.refresh(task)
    return task

@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    task = db.query(Task).join(Project).filter(Task.id == task_id, Project.owner_id == user.id).first()
    if not task: raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task); db.commit()
