from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Project, User
from app.core.deps import get_current_user, require_admin
from app.modules.projects.schemas import ProjectCreate, ProjectOut
from app.tasks import create_project_notification

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("", response_model=ProjectOut, status_code=201)
def create_project(data: ProjectCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = Project(**data.model_dump(), owner_id=user.id)
    db.add(project); db.commit(); db.refresh(project)
    create_project_notification.delay(user.id, project.name)
    return project

@router.get("", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Project).filter(Project.owner_id == user.id).order_by(Project.id.desc()).all()

@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == user.id).first()
    if not project: raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    project = db.get(Project, project_id)
    if not project: raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project); db.commit()
